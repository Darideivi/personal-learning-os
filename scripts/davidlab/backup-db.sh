#!/usr/bin/env bash
# backup-db.sh - dump the LearnHouse dev database to a gzipped SQL file.
#
# Usage:
#   bash scripts/davidlab/backup-db.sh
#   BACKUP_DIR=/mnt/d/backups KEEP=30 bash scripts/davidlab/backup-db.sh
#
# Defaults: BACKUP_DIR=~/backups/learnhouse, KEEP=14 (newest files kept).
#
# Nightly at 02:30 (add with `crontab -e`; use your real path):
#   30 2 * * * bash $HOME/dev/personal-learning-os/scripts/davidlab/backup-db.sh >> $HOME/backups/learnhouse/backup.log 2>&1
#
# RESTORE (WARNING: this overwrites existing data in the database; stop the
# API first and back up the current state before restoring):
#   gunzip -c ~/backups/learnhouse/learnhouse-YYYYmmdd-HHMM.sql.gz | docker exec -i learnhouse-db-dev psql -U learnhouse -d learnhouse

set -euo pipefail

CONTAINER="learnhouse-db-dev"
BACKUP_DIR="${BACKUP_DIR:-$HOME/backups/learnhouse}"
KEEP="${KEEP:-14}"

fail() { echo "ERROR: $1" >&2; exit 1; }

# The container must be running (docker inspect prints "true" or "false").
[ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null || true)" = "true" ] \
  || fail "container $CONTAINER is not running (start it with: npx learnhouse dev)"

mkdir -p "$BACKUP_DIR"
file="$BACKUP_DIR/learnhouse-$(date +%Y%m%d-%H%M).sql.gz"

# pipefail makes this fail if pg_dump fails, not just gzip. Remove partial files on failure.
if ! docker exec "$CONTAINER" pg_dump -U learnhouse -d learnhouse | gzip > "$file"; then
  rm -f "$file"
  fail "pg_dump failed"
fi

# Verify: archive is valid and the dump has content.
gzip -t "$file" || { rm -f "$file"; fail "gzip test failed, backup removed"; }
[ -n "$(gunzip -c "$file" | head -c 1)" ] || { rm -f "$file"; fail "dump is empty, backup removed"; }

# Keep only the newest $KEEP backups (names sort by date).
ls -1 "$BACKUP_DIR"/learnhouse-*.sql.gz | sort -r | tail -n +"$((KEEP + 1))" | xargs -r rm -f --

echo "OK: $file ($(du -h "$file" | cut -f1))"
