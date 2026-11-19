import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "backend"))
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    load_dotenv(project_root / ".env")
except ImportError:
    pass

import asyncio
import contextvars
import logging
import os
import re
import secrets
import sqlite3
import struct
import time
from dataclasses import dataclass, field
from datetime import datetime

from datetime import timezone
from sqlalchemy import select

from database import AsyncSessionLocal
from backend.models import Element, Supplier, Table, User


ODBC_HOST = os.getenv("ODBC_HOST", "0.0.0.0")
ODBC_PORT = int(os.getenv("ODBC_PORT", "5433"))
ODBC_DATABASE = os.getenv("ODBC_DATABASE", "bloodstone")
REFRESH_SECONDS = float(os.getenv("ODBC_REFRESH", "30"))
AUTH_FAIL_DELAY = 1.0

ELEMENT_COLUMNS = {
    "uuid": "uuid",
    "part_name": "part_name",
    "manufacturer": "manufacturer",
    "description": "description",
    "value": "value",
    "availability": "availability",
    "library_reference": "library_reference",
    "library_path": "library_path",
    "footprint_reference_1": "footprint_reference_1",
    "footprint_path_1": "footprint_path_1",
    "footprint_reference_2": "footprint_reference_2",
    "footprint_path_2": "footprint_path_2",
    "footprint_reference_3": "footprint_reference_3",
    "footprint_path_3": "footprint_path_3"
}

SUPPLIER_CELL_ATTR = os.getenv("ODBC_SUPPLIER_CELL", "value")

log = logging.getLogger("altium_odbc")
CURRENT_USER: contextvars.ContextVar[str] = contextvars.ContextVar("current_user", default="")

def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    try:
        if hashed.startswith(("$2a$", "$2b$", "$2y$")):
            import bcrypt
            return bcrypt.checkpw(plain.encode(), hashed.encode())
        if hashed.startswith("$argon2"):
            from argon2 import PasswordHasher
            from argon2.exceptions import VerificationError, InvalidHashError
            try:
                return PasswordHasher().verify(hashed, plain)
            except (VerificationError, InvalidHashError):
                return False
        try:
            from passlib.context import CryptContext
            return CryptContext(schemes=["pbkdf2_sha256", "sha512_crypt", "sha256_crypt"]).verify(plain, hashed)
        except ImportError:
            pass
    except ValueError:
        return False
    log.error("Password hash format unknown - adjust verify_password()") 
    return False


async def authenticate(username: str, password: str) -> str | None:
    async with AsyncSessionLocal() as session:
        user = (await session.execute(select(User).where(User.username == username))).scalar_one_or_none()
    if user is None:
        await asyncio.sleep(AUTH_FAIL_DELAY)
        return f'password authentication failed for user "{username}"'
    ok = await asyncio.to_thread(verify_password, password, user.password)
    if not ok:
        await asyncio.sleep(AUTH_FAIL_DELAY)
        return f'password authentication failed for user "{username}"'
    expires = user.expiration_time
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires <= datetime.now(timezone.utc):
        return f'konto "{username}" wygasło {expires:%Y-%m-%d %H:%M} UTC'
    return None

def _to_text(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


async def fetch_rows() -> tuple[list[str], dict[str, list[tuple]]]:
    async with AsyncSessionLocal() as session:
        tables = (await session.execute(select(Table.name).order_by(Table.name))).scalars().all()
        suppliers = (await session.execute(select(Supplier).order_by(Supplier.id))).scalars().all()
        elements = (await session.execute(select(Element).order_by(Element.part_name))).scalars().all()

        supplier_ids = [s.id for s in suppliers]
        rows: dict[str, list[tuple]] = {t: [] for t in tables}
        for el in elements:
            row = [_to_text(getattr(el, attr)) for attr in ELEMENT_COLUMNS.values()]
            row.append(", ".join(el.tags or []))
            cells = {es.supplierId: _to_text(getattr(es, SUPPLIER_CELL_ATTR)) for es in el.suppliers}
            row.extend(cells.get(sid) for sid in supplier_ids)
            rows.setdefault(el.table, []).append(tuple(row))

    columns = list(ELEMENT_COLUMNS) + ["tags"] + [f"supplier_{sid}" for sid in supplier_ids]
    return columns, rows

@dataclass
class Snapshot:
    tables: list[str]
    columns: list[str]
    widths: dict[str, int]
    db: sqlite3.Connection
    loaded_at: float = field(default_factory=time.monotonic)

class Store:
    def __init__(self):
        self.snapshot: Snapshot | None = None
        self._lock = asyncio.Lock()

    async def get(self) -> Snapshot:
        if self.snapshot is None or time.monotonic() - self.snapshot.loaded_at > REFRESH_SECONDS:
            async with self._lock:
                if self.snapshot is None or time.monotonic() - self.snapshot.loaded_at > REFRESH_SECONDS:
                    try:
                        self.snapshot = await self._load()
                    except Exception:
                        if self.snapshot is None:
                            raise
                        log.exception("Refreshing went wrong, last version is still available") 
                        self.snapshot.loaded_at = time.monotonic()
        return self.snapshot

    @staticmethod
    async def _load() -> Snapshot:
        columns, tables = await fetch_rows()
        db = sqlite3.connect(":memory:", check_same_thread=False)
        db.create_function("version", 0, lambda: "PostgreSQL 14.0 (Altium ODBC bridge)")
        cols_sql = ", ".join(f'"{c}" TEXT' for c in columns)
        placeholders = ", ".join("?" * len(columns))
        all_rows = []
        for name, rows in tables.items():
            q = '"' + name.replace('"', '""') + '"'
            db.execute(f"CREATE TABLE {q} ({cols_sql})")
            db.executemany(f"INSERT INTO {q} VALUES ({placeholders})", rows)
            all_rows += rows
        db.commit()
        widths = {c: max([len(r[i] or "") for r in all_rows] + [255]) for i, c in enumerate(columns)}
        log.info("Loaded %d elements in %d tables (%s), %d columns",
                 len(all_rows), len(tables), ", ".join(tables), len(columns))
        return Snapshot(list(tables), columns, widths, db)


STORE = Store()

OID_BOOL, OID_INT2, OID_INT4, OID_OID, OID_TEXT, OID_NAME, OID_VARCHAR = 16, 21, 23, 26, 25, 19, 1043
TABLE_OID = 16384
TYPE_SIZE = {OID_BOOL: 1, OID_INT2: 2, OID_INT4: 4, OID_OID: 4, OID_NAME: 64}

@dataclass
class Col:
    name: str
    oid: int = OID_TEXT
    typmod: int = -1
    table_oid: int = 0
    attnum: int = 0

@dataclass
class Result:
    tag: str
    columns: list[Col] | None = None
    rows: list[tuple] = field(default_factory=list)

class QueryError(Exception):
    def __init__(self, message, code="42601"):
        super().__init__(message)
        self.code = code

def _rows(names_types, rows, tag=None) -> Result:
    cols = [Col(n, t) for n, t in names_types]
    return Result(tag or f"SELECT {len(rows)}", cols, rows)

def _strip_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    return re.sub(r"--[^\n]*", " ", sql)

def split_statements(sql: str) -> list[str]:
    out, buf, quote = [], [], None
    for ch in sql:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
            buf.append(ch)
        elif ch == ";":
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    out.append("".join(buf))
    return [s for s in out if s.strip()]

def substitute_params(sql: str, params: list[str | None]) -> str:
    def repl(m):
        i = int(m.group(1)) - 1
        if i >= len(params) or params[i] is None:
            return "NULL"
        return "'" + params[i].replace("'", "''") + "'"
    return re.sub(r"\$(\d+)", repl, sql)

SHOW_VALUES = {
    "transaction_isolation": "read committed",
    "transaction isolation level": "read committed",
    "server_version": "14.0",
    "server_encoding": "UTF8",
    "client_encoding": "UTF8",
    "standard_conforming_strings": "on",
    "max_identifier_length": "63",
    "datestyle": "ISO, MDY",
    "timezone": "UTC",
}

def _like_match(pattern: str | None, value: str) -> bool:
    if pattern is None:
        return True
    regex = "".join(".*" if c == "%" else "." if c == "_" else re.escape(c)
                    for c in re.sub(r"\\(.)", r"\1", pattern))
    return re.fullmatch(regex, value, flags=re.I) is not None

def _filter_value(sql: str, column: str) -> str | None:
    m = re.search(rf"\b{re.escape(column)}\s*(?:=|like|ilike)\s*E?'((?:[^']|'')*)'", sql, re.I)
    return m.group(1).replace("''", "'") if m else None

def _matching_tables(sql: str, snap: Snapshot, column: str) -> list[tuple[int, str]]:
    pattern = _filter_value(sql, column)
    return [(i, t) for i, t in enumerate(snap.tables) if _like_match(pattern, t)]

def catalog_tables(sql: str, snap: Snapshot) -> Result:
    names = [("TABLE_QUALIFIER", OID_NAME), ("TABLE_OWNER", OID_NAME), ("TABLE_NAME", OID_NAME),
             ("TABLE_TYPE", OID_TEXT), ("REMARKS", OID_TEXT)]
    if re.search(r"select\s+relname\s*,\s*nspname\s*,\s*relkind", sql, re.I):
        rows = []
        if _like_match(_filter_value(sql, "nspname"), "public"):
            rows = [(t, "public", "r") for _, t in _matching_tables(sql, snap, "relname")]
        return _rows([("relname", OID_NAME), ("nspname", OID_NAME), ("relkind", OID_TEXT)], rows)
    rows = [(ODBC_DATABASE, "public", t, "TABLE", None) for t in snap.tables]
    return _rows(names, rows)

def catalog_columns(sql: str, snap: Snapshot) -> Result:
    cols = [("nspname", OID_NAME), ("relname", OID_NAME), ("attname", OID_NAME), ("atttypid", OID_OID),
            ("typname", OID_NAME), ("attnum", OID_INT2), ("attlen", OID_INT2), ("atttypmod", OID_INT4),
            ("attnotnull", OID_BOOL), ("relhasrules", OID_BOOL), ("relkind", OID_TEXT), ("oid", OID_OID),
            ("pg_get_expr", OID_TEXT), ("case", OID_INT4), ("attidentity", OID_TEXT), ("attgenerated", OID_TEXT)]
    if not _like_match(_filter_value(sql, "n.nspname"), "public"):
        return _rows(cols, [])
    attname = _filter_value(sql, "a.attname")
    rows = []
    for t_idx, table in _matching_tables(sql, snap, "c.relname"):
        for i, c in enumerate(snap.columns, start=1):
            if _like_match(attname, c):
                rows.append(("public", table, c, str(OID_VARCHAR), "varchar", str(i), "-1",
                             str(snap.widths[c] + 4), "f", "f", "r", str(TABLE_OID + t_idx), None, "0", "", ""))
    return _rows(cols, rows)


def catalog_query(sql: str, low: str, snap: Snapshot) -> Result:
    if "pg_attribute" in low and ("attname" in low or "attnum" in low) and "indkey" not in low \
            and "pg_index" not in low and "pg_constraint" not in low:
        return catalog_columns(sql, snap)
    if "pg_class" in low and "relkind" in low and "pg_attribute" not in low and "pg_index" not in low:
        return catalog_tables(sql, snap)
    if "typname" in low and "'lo'" in low:
        return _rows([("oid", OID_OID), ("typbasetype", OID_OID)], [])
    if "current_schema" in low:
        return _rows([("current_schema", OID_NAME)], [("public",)])
    if "pg_namespace" in low and "nspname" in low and "pg_class" not in low:
        return _rows([("nspname", OID_NAME)], [("public",)])
    if "pg_encoding_to_char" in low or "getdatabaseencoding" in low:
        return _rows([("encoding", OID_NAME)], [("UTF8",)])
    log.debug("Empty result for query: %s", sql) 
    return _rows([("dummy", OID_TEXT)], [])

def to_sqlite(sql: str) -> str:
    sql = re.sub(r'\b(?:"?public"?|"?pg_catalog"?)\s*\.\s*', "", sql, flags=re.I)
    sql = re.sub(r"::\s*\"?\w+\"?(?:\s*\(\s*\d+\s*\))?(?:\[\])?", "", sql)
    sql = re.sub(r"\bilike\b", "LIKE", sql, flags=re.I)
    sql = re.sub(r"\bE'", "'", sql)
    sql = re.sub(r"\bfor\s+(?:update|share|read\s+only)\b.*$", "", sql, flags=re.I | re.S)
    return sql

async def execute(sql: str) -> Result | None:
    sql = _strip_comments(sql).strip()
    if not sql:
        return None
    low = re.sub(r"\s+", " ", sql.lower())
    word = low.split(" ", 1)[0]

    if word in ("begin", "start"):
        return Result("BEGIN")
    if word in ("commit", "end"):
        return Result("COMMIT")
    if word in ("rollback", "abort"):
        return Result("ROLLBACK")
    if word in ("set", "reset", "savepoint", "release", "deallocate", "discard", "listen", "unlisten", "close"):
        return Result(word.upper() if word != "release" else "RELEASE")
    if word == "show":
        name = low[5:].strip().strip('"')
        value = SHOW_VALUES.get(name, "")
        return _rows([(name.split()[-1], OID_TEXT)], [(value,)], "SHOW")
    if word in ("insert", "update", "delete", "create", "drop", "alter", "truncate", "copy", "grant"):
        raise QueryError("Altium ODBC bridge jest tylko do odczytu", "25006")
    if word not in ("select", "with", "values"):
        raise QueryError(f"Wrong command: {word}", "0A000")

    snap = await STORE.get()
    if re.fullmatch(r"select (version\(\)|current_database\(\)|current_user|current_schema\(\)|1)", low):
        val = {"select version()": "PostgreSQL 14.0 (Altium ODBC bridge)",
               "select current_database()": ODBC_DATABASE, "select current_user": CURRENT_USER.get(),
               "select current_schema()": "public", "select 1": "1"}[low]
        return _rows([(low.split(" ", 1)[1].rstrip("()"), OID_TEXT)], [(val,)])
    if re.search(r"\b(pg_\w+|information_schema)\b", low):
        return catalog_query(sql, low, snap)

    m = re.search(r'\bfrom\s+(?:"((?:[^"]|"")+)"|(\w+))', sql, re.I)
    source = (m.group(1).replace('""', '"') if m.group(1) else m.group(2)).lower() if m else ""
    table_oid = next((TABLE_OID + i for i, t in enumerate(snap.tables) if t.lower() == source), 0)
    try:
        cur = snap.db.execute(to_sqlite(sql))
    except sqlite3.Error as exc:
        raise QueryError(f"{exc} (zapytanie: {sql})")
    rows = [tuple(None if v is None else str(v) for v in r) for r in cur.fetchall()]
    cols = []
    for d in cur.description or []:
        name = d[0]
        if name in snap.widths:
            cols.append(Col(name, OID_VARCHAR, snap.widths[name] + 4, table_oid,
                            snap.columns.index(name) + 1))
        else:
            cols.append(Col(name, OID_TEXT))
    return Result(f"SELECT {len(rows)}", cols, rows)

def msg(kind: bytes, payload: bytes = b"") -> bytes:
    return kind + struct.pack("!I", len(payload) + 4) + payload

def cstr(s: str) -> bytes:
    return s.encode() + b"\0"

def row_description(cols: list[Col]) -> bytes:
    body = struct.pack("!H", len(cols))
    for c in cols:
        body += cstr(c.name) + struct.pack("!IhIhih", c.table_oid, c.attnum, c.oid,
                                           TYPE_SIZE.get(c.oid, -1), c.typmod, 0)
    return msg(b"T", body)

def data_row(row: tuple) -> bytes:
    body = struct.pack("!H", len(row))
    for v in row:
        if v is None:
            body += struct.pack("!i", -1)
        else:
            b = str(v).encode()
            body += struct.pack("!i", len(b)) + b
    return msg(b"D", body)

def error_response(message: str, code: str = "XX000") -> bytes:
    return msg(b"E", b"SERROR\0VERROR\0C" + cstr(code) + b"M" + cstr(message) + b"\0")

class Session:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.r, self.w = reader, writer
        self.in_tx = False
        self.statements: dict[str, tuple[str, int]] = {}
        self.portals: dict[str, dict] = {}
        self.peer = writer.get_extra_info("peername")

    def ready(self) -> bytes:
        return msg(b"Z", b"T" if self.in_tx else b"I")

    def _track_tx(self, tag: str):
        if tag == "BEGIN":
            self.in_tx = True
        elif tag in ("COMMIT", "ROLLBACK"):
            self.in_tx = False

    async def read_msg(self) -> tuple[bytes, bytes]:
        head = await self.r.readexactly(5)
        kind, length = head[:1], struct.unpack("!I", head[1:])[0]
        return kind, await self.r.readexactly(length - 4)

    async def startup(self) -> bool:
        while True:
            length = struct.unpack("!I", await self.r.readexactly(4))[0]
            body = await self.r.readexactly(length - 4)
            code = struct.unpack("!I", body[:4])[0]
            if code in (80877103, 80877104):
                self.w.write(b"N")
                await self.w.drain()
                continue
            if code == 80877102:
                return False
            if code != 196608:
                self.w.write(error_response("Nieobsługiwana wersja protokołu", "0A000"))
                return False
            parts = body[4:].split(b"\0")
            params = {parts[i].decode(): parts[i + 1].decode() for i in range(0, len(parts) - 1, 2) if parts[i]}
            break

        user = params.get("user", "")
        self.w.write(msg(b"R", struct.pack("!I", 3)))
        await self.w.drain()
        kind, payload = await self.read_msg()
        password = payload.rstrip(b"\0").decode(errors="replace") if kind == b"p" else ""
        error = await authenticate(user, password) if user and password else "brak loginu lub hasła"
        if error:
            log.warning("Login went wrong from %s as %r: %s", self.peer, user, error)
            self.w.write(error_response(error, "28P01"))
            await self.w.drain()
            return False
        CURRENT_USER.set(user)

        out = msg(b"R", struct.pack("!I", 0))
        for k, v in {"server_version": "14.0", "server_encoding": "UTF8", "client_encoding": "UTF8",
                     "DateStyle": "ISO, MDY", "integer_datetimes": "on", "TimeZone": "UTC",
                     "standard_conforming_strings": "on", "is_superuser": "off",
                     "session_authorization": user, "application_name": params.get("application_name", "")}.items():
            out += msg(b"S", cstr(k) + cstr(v))
        out += msg(b"K", struct.pack("!II", os.getpid() & 0x7FFFFFFF, secrets.randbits(31)))
        self.w.write(out + self.ready())
        await self.w.drain()
        log.info("Connected: %s (%s)", self.peer, user)
        return True

    async def simple_query(self, payload: bytes):
        sql = payload.rstrip(b"\0").decode()
        log.debug("Q: %s", sql)
        out = b""
        statements = split_statements(sql)
        if not statements:
            out += msg(b"I")
        for stmt in statements:
            try:
                res = await execute(stmt)
            except QueryError as exc:
                out += error_response(str(exc), exc.code)
                break
            except Exception as exc:
                log.exception("Error query")
                out += error_response(str(exc))
                break
            if res is None:
                out += msg(b"I")
                continue
            self._track_tx(res.tag)
            if res.columns is not None:
                out += row_description(res.columns) + b"".join(data_row(r) for r in res.rows)
            out += msg(b"C", cstr(res.tag))
        self.w.write(out + self.ready())

    async def extended(self, kind: bytes, payload: bytes) -> bytes:
        if kind == b"P":
            name, rest = payload.split(b"\0", 1)
            query, rest = rest.split(b"\0", 1)
            n_params = struct.unpack("!H", rest[:2])[0]
            q = query.decode()
            log.debug("P: %s", q)
            self.statements[name.decode()] = (q, n_params or len(set(re.findall(r"\$(\d+)", q))))
            return msg(b"1")
        if kind == b"B":
            portal, rest = payload.split(b"\0", 1)
            stmt, rest = rest.split(b"\0", 1)
            pos = 0
            nfmt = struct.unpack_from("!H", rest, pos)[0]; pos += 2
            fmts = struct.unpack_from(f"!{nfmt}H", rest, pos); pos += 2 * nfmt
            nparams = struct.unpack_from("!H", rest, pos)[0]; pos += 2
            params = []
            for i in range(nparams):
                ln = struct.unpack_from("!i", rest, pos)[0]; pos += 4
                if ln < 0:
                    params.append(None)
                    continue
                raw = rest[pos:pos + ln]; pos += ln
                fmt = fmts[i] if len(fmts) > 1 else (fmts[0] if fmts else 0)
                if fmt == 1 and ln in (2, 4, 8):
                    params.append(str(int.from_bytes(raw, "big", signed=True)))
                else:
                    params.append(raw.decode())
            query, _ = self.statements[stmt.decode()]
            self.portals[portal.decode()] = {"sql": substitute_params(query, params), "result": None, "sent": 0}
            return msg(b"2")
        if kind == b"D":
            target, name = payload[:1], payload[1:].rstrip(b"\0").decode()
            if target == b"S":
                query, n = self.statements[name]
                out = msg(b"t", struct.pack("!H", n) + struct.pack(f"!{n}I", *([OID_TEXT] * n)))
                res = await self._safe_describe(substitute_params(query, []))
            else:
                portal = self.portals[name]
                if portal["result"] is None:
                    portal["result"] = await self._run(portal["sql"])
                res, out = portal["result"], b""
            return out + (row_description(res.columns) if res and res.columns is not None else msg(b"n"))
        if kind == b"E":
            name = payload.split(b"\0", 1)[0].decode()
            max_rows = struct.unpack("!I", payload.split(b"\0", 1)[1][:4])[0]
            portal = self.portals[name]
            if portal["result"] is None:
                portal["result"] = await self._run(portal["sql"])
            res = portal["result"]
            if res is None:
                return msg(b"I")
            rows = res.rows[portal["sent"]:]
            if max_rows and len(rows) > max_rows:
                portal["sent"] += max_rows
                return b"".join(data_row(r) for r in rows[:max_rows]) + msg(b"s")
            portal["sent"] = len(res.rows)
            return b"".join(data_row(r) for r in rows) + msg(b"C", cstr(res.tag))
        if kind == b"C":
            target, name = payload[:1], payload[1:].rstrip(b"\0").decode()
            (self.statements if target == b"S" else self.portals).pop(name, None)
            return msg(b"3")
        return b""

    async def _run(self, sql: str) -> Result | None:
        log.debug("E: %s", sql)
        res = await execute(sql)
        if res:
            self._track_tx(res.tag)
        return res

    async def _safe_describe(self, sql: str) -> Result | None:
        low = sql.strip().lower()
        if not low.startswith(("select", "with", "values", "show")):
            return None
        try:
            return await execute(sql)
        except QueryError:
            return None

    async def run(self):
        try:
            if not await self.startup():
                return
            failed = False
            while True:
                kind, payload = await self.read_msg()
                if kind == b"X":
                    return
                if kind == b"Q":
                    failed = False
                    await self.simple_query(payload)
                elif kind == b"S":
                    failed = False
                    self.w.write(self.ready())
                elif kind == b"H":
                    pass
                elif failed:
                    continue
                else:
                    try:
                        self.w.write(await self.extended(kind, payload))
                    except QueryError as exc:
                        self.w.write(error_response(str(exc), exc.code))
                        failed = True
                    except Exception as exc:
                        log.exception("Error in extended protocol")
                        self.w.write(error_response(str(exc)))
                        failed = True
                await self.w.drain()
        except (asyncio.IncompleteReadError, ConnectionResetError):
            pass
        finally:
            self.w.close()


async def main():
    logging.basicConfig(level=os.getenv("ALTIUM_ODBC_LOG", "INFO"),
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    await STORE.get()
    server = await asyncio.start_server(lambda r, w: Session(r, w).run(), ODBC_HOST, ODBC_PORT)
    log.info("Altium ODBC bridge listens to %s:%d (db: %s)", ODBC_HOST, ODBC_PORT, ODBC_DATABASE)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())