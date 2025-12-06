# Docker Setup Guide

Quick guide for running ISP Payment Recovery System with Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (usually included with Docker Desktop)

## Quick Start

1. **Build and Start**
   ```bash
   docker-compose up -d
   ```

2. **Access Application**
   - Local: http://localhost:5000
   - Network: http://YOUR_IP:5000

3. **Stop Application**
   ```bash
   docker-compose down
   ```

## Docker Commands

### Start in foreground (see logs)
```bash
docker-compose up
```

### Start in background (detached)
```bash
docker-compose up -d
```

### Stop application
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### Rebuild after code changes
```bash
docker-compose up -d --build
```

### Add sample data (if needed)
```bash
docker-compose exec isp-recovery python add_sample_data.py
```

## Data Persistence

- Database file (`isp_recovery.db`) is stored in the project folder
- Data persists even after stopping/removing containers
- To backup: Copy `isp_recovery.db` file from project folder

## Troubleshooting

**Port already in use:**
- Change port in `docker-compose.yml`: `"5001:5000"` (change first number)

**Container won't start:**
```bash
docker-compose logs
```

**Reset everything (removes data!):**
```bash
docker-compose down -v
rm isp_recovery.db
docker-compose up -d
```

