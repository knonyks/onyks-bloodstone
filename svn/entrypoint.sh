#!/bin/bash
set -e

echo "--- START ENTRYPOINT ---"

echo "Waiting for database to be ready..."
export PGPASSWORD=$POSTGRES_PASSWORD

until psql -h database -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1 FROM private.users LIMIT 1;" > /dev/null 2>&1; do
  echo "Database or table private.users not ready yet... waiting 2s..."
  sleep 2
done

echo "Database is ready, table private.users found!"

if [ ! -f "/var/svn/$SVN_REPO_NAME/format" ]; then
    mkdir -p "/var/svn/$SVN_REPO_NAME"
    svnadmin create "/var/svn/$SVN_REPO_NAME"
fi

chown -R www-data:www-data /var/svn

envsubst '\$POSTGRES_USER \$POSTGRES_PASSWORD \$POSTGRES_DB \$SVN_REPO_NAME' \
    < /usr/local/apache2/conf/httpd.conf.template \
    > /usr/local/apache2/conf/httpd.conf

echo "Configuration ready. Installing SVN hook and starting Apache."

HOOKS_DIR="/var/svn/$SVN_REPO_NAME/hooks"

mkdir -p "$HOOKS_DIR"

cp /opt/post-commit "$HOOKS_DIR/post-commit"
chmod +x "$HOOKS_DIR/post-commit"

chown www-data:www-data "$HOOKS_DIR/post-commit"

echo "Fetching the latest revision from the repository..."
YOUNGEST_REV=$(svnlook youngest "/var/svn/$SVN_REPO_NAME")

echo "Running post-commit hook for revision ($YOUNGEST_REV)..."
/usr/bin/env python3 "$HOOKS_DIR/post-commit" "/var/svn/$SVN_REPO_NAME" "$YOUNGEST_REV"

exec "$@"