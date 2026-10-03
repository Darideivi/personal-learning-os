# DavidLab helper scripts

Run these on **DavidLab, inside WSL Ubuntu**. Never on the work laptop or the cloud sandbox.

| Script | What it does | When to run |
|---|---|---|
| `setup-tools.sh` | Checks WSL, git, curl, build-essential and Docker, then installs nvm + Node 24, bun 1.4.2, uv and graphifyy. Prints all versions. Needs no sudo. | Once, before PHASE0_PLAN goal 1. Safe to re-run. |
| `backup-db.sh` | `pg_dump` of the `learnhouse-db-dev` container to `~/backups/learnhouse/learnhouse-YYYYmmdd-HHMM.sql.gz`, verified with `gzip -t`, newest 14 kept. | After LearnHouse is running; then regularly (cron line is in the script header). |

## Usage

```bash
bash scripts/davidlab/setup-tools.sh
source ~/.bashrc            # new shells need this for nvm/bun/uv on PATH

bash scripts/davidlab/backup-db.sh
BACKUP_DIR=/mnt/d/backups KEEP=30 bash scripts/davidlab/backup-db.sh
```

If `setup-tools.sh` reports missing packages, run the `sudo apt ...` line it prints, then re-run it.
Restore instructions (which overwrite data) are in the `backup-db.sh` header.
