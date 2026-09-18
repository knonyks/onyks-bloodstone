#!/bin/bash
set -e

echo "--- START ENTRYPOINT ---"

# 1. Wait for PostgreSQL and the specific table to be ready
echo "Czekam na pełną gotowość bazy danych i tabel..."
export PGPASSWORD=$POSTGRES_PASSWORD

until psql -h database -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1 FROM private.users LIMIT 1;" > /dev/null 2>&1; do
  echo "Baza danych lub tabela private.users jeszcze nie istnieje... czekam 2s..."
  sleep 2
done

echo "Baza danych jest w pełni gotowa, tabela private.users znaleziona!"

# 2. Create SVN repository if it doesn't exist
if [ ! -f "/var/svn/$SVN_REPO_NAME/format" ]; then
    mkdir -p "/var/svn/$SVN_REPO_NAME"
    svnadmin create "/var/svn/$SVN_REPO_NAME"
fi

chown -R www-data:www-data /var/svn

# 3. Generate Apache config from template
envsubst '\$POSTGRES_USER \$POSTGRES_PASSWORD \$POSTGRES_DB \$SVN_REPO_NAME' \
    < /usr/local/apache2/conf/httpd.conf.template \
    > /usr/local/apache2/conf/httpd.conf

# 4. Loop for syncing authz file from PostgreSQL
sync_authz_file() {
    echo "Uruchamiam proces synchronizacji uprawnień w tle..."
    
    # Infinite loop for syncing authz file every 10 seconds
    while true; do
        # Create a temporary file with the header
        echo "[/]" > /tmp/svn-authz.tmp
        
        export PGPASSWORD=$POSTGRES_PASSWORD
        
        # Download login and rank from PostgreSQL and append to the temp authz file
        # If the query fails (e.g. database is down), we skip this iteration and try again in 10 seconds
        if psql "host=database dbname=$POSTGRES_DB user=$POSTGRES_USER" -Atc \
           "SELECT login, rank FROM private.users;" >> /tmp/svn-authz.tmp 2>/dev/null; then
           
           # Process the downloaded data to convert ranks to permissions
           # Here we read the temp file line by line, convert ranks to permissions, and write to another temp file
           # We use a case statement to map ranks to permissions (admin and editor get rw, user gets r)
           
           # Clean up the tmp file to only have login and rank
           psql "host=database dbname=$POSTGRES_DB user=$POSTGRES_USER" -Atc \
           "SELECT login, rank FROM private.users;" | while IFS='|' read login rank; do
                case $rank in
                    server) echo "$login = rw" ;;
                    admin) echo "$login = rw" ;;
                    editor) echo "$login = rw" ;;
                    user) echo "$login = r" ;;
                esac
           done > /tmp/svn-perms.tmp

           # Concat the header and permissions into the final authz file
           echo "[/]" > /tmp/svn-authz.final
           cat /tmp/svn-perms.tmp >> /tmp/svn-authz.final

           # Replace the main authz file if there are changes
           if ! cmp -s /tmp/svn-authz.final /etc/svn-authz; then
               cp /tmp/svn-authz.final /etc/svn-authz
               chown www-data:www-data /etc/svn-authz
               chmod 640 /etc/svn-authz
               echo "$(date) - Zaktualizowano uprawnienia SVN z bazy."
           fi
        fi
        
        # Wait for 10 seconds before next sync
        sleep 10
    done
}

# Run the sync_authz_file function in the background
sync_authz_file &

# =================================================================

echo "Konfiguracja gotowa. Instaluję SVN hook i uruchamiam Apache."

# 1. Definiujemy poprawną ścieżkę do katalogu hooks wewnątrz Twojego repozytorium
HOOKS_DIR="/var/svn/$SVN_REPO_NAME/hooks"

# 2. Upewniamy się, że folder istnieje (svnadmin create powinien go założyć, ale dla pewności)
mkdir -p "$HOOKS_DIR"

# 3. Kopiujemy hooka i nadajemy uprawnienia do wykonywania (+x jest krytyczne)
cp /opt/post-commit "$HOOKS_DIR/post-commit"
chmod +x "$HOOKS_DIR/post-commit"

# 4. Nadajemy uprawnienia własnościowe (używamy www-data, tak jak zrobiłeś to w kroku 2)
chown www-data:www-data "$HOOKS_DIR/post-commit"

echo "Pobieram najnowszą rewizję z repozytorium..."
YOUNGEST_REV=$(svnlook youngest "/var/svn/$SVN_REPO_NAME")

echo "Uruchamiam skrypt post-commit dla rewizji początkowej ($YOUNGEST_REV)..."
# Uruchamiamy skrypt ręcznie, podając mu ścieżkę i najnowszą rewizję
/usr/bin/env python3 "$HOOKS_DIR/post-commit" "/var/svn/$SVN_REPO_NAME" "$YOUNGEST_REV"

exec "$@"