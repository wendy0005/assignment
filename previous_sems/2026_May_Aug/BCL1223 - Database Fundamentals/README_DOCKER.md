# BCL1223 Database Fundamentals - Docker Setup

## Prerequisites

- Docker Desktop installed
- ~10GB disk space for Oracle XE image
- Accept Oracle license (automatic at first pull)

## Quick Start

```bash
# 1. Start Oracle XE container
cd "/Users/jingyichan/PycharmProjects/assignment/current_sem/BCL1223 - Database Fundamentals"
docker-compose up -d

# 2. Wait for Oracle to be ready (~10-15 minutes first time)
docker-compose logs -f oracle-db
# Look for: "Database is ready to use"

# 3. Run setup script (in another terminal)
chmod +x setup.sh
./setup.sh
```

## Usage

```bash
# Connect via SQL*Plus (from host)
sqlplus bcl1223/bcl1223@localhost:1521/XEPDB1

# Or connect inside container
docker exec -it bcl1223_oracle sqlplus bcl1223/bcl1223@XEPDB1
```

## Connection Details

| Parameter | Value |
|-----------|-------|
| Host | localhost |
| Port | 1521 |
| Service | XEPDB1 |
| Username | bcl1223 |
| Password | bcl1223 |
| Sysdba | system / OraclePass123 |

## Sample Queries

```sql
ALTER SESSION SET NLS_DATE_FORMAT = 'DD-MON-YYYY';

-- Task 3.1 - Student phone list
SELECT DISTINCT s.student_id, s.student_name, s.phone_number
FROM bcl1223.student s
JOIN bcl1223.membership m ON m.student_id = s.student_id
ORDER BY s.student_name;

-- Task 3.2 - Advisors with multiple clubs
SELECT a.advisor_name, COUNT(c.club_id) AS number_of_clubs,
       LISTAGG(c.club_name, '; ') WITHIN GROUP (ORDER BY c.club_name) AS assigned_clubs
FROM bcl1223.advisor a
JOIN bcl1223.club c ON c.advisor_id = a.advisor_id
GROUP BY a.advisor_id, a.advisor_name
HAVING COUNT(c.club_id) > 1;

-- Row counts
SELECT table_name, num_rows FROM user_tables ORDER BY table_name;
```

## Useful Commands

```bash
# View logs
docker-compose logs -f oracle-db

# Stop
docker-compose down

# Clean slate (removes all data)
docker-compose down -v

# Restart
docker-compose restart
```

## Files

- `docker-compose.yml` - Container orchestration
- `Dockerfile` - Oracle XE 21c image config
- `init.sql` - Schema + seed data
- `setup.sh` - Setup script to run after container starts
