# Cloud Server Deployment Guide

This guide will help you deploy the ISP Payment Recovery System on a cloud server.

## Prerequisites

- Cloud server (AWS EC2, DigitalOcean, Linode, Azure, etc.)
- Docker and Docker Compose installed on the server
- SSH access to your server
- Domain name (optional, for production)

## Quick Deployment

### 1. Connect to Your Cloud Server

```bash
ssh user@your-server-ip
```

### 2. Install Docker and Docker Compose

If not already installed:

```bash
# Update system
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin -y

# Add user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
```

### 3. Clone the Repository

```bash
git clone https://github.com/mashhoudrajput/lucky-nework.git
cd lucky-nework
```

### 4. Create Data Directory

```bash
mkdir -p data
chmod 755 data
```

### 5. Configure Environment (Optional)

Create a `.env` file for custom configuration:

```bash
nano .env
```

Add:
```
PORT=5000
DATABASE_PATH=/app/data/isp_recovery.db
FLASK_ENV=production
```

### 6. Start the Application

**Option A: Using Docker Compose (Recommended)**

```bash
docker-compose up -d --build
```

**Option B: Using Production Compose File**

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### 7. Check Container Status

```bash
docker-compose ps
docker-compose logs -f
```

### 8. Access the Application

- **Without domain**: `http://YOUR_SERVER_IP:5000`
- **With domain**: `http://your-domain.com` (after setting up reverse proxy)

## Reverse Proxy Setup (Nginx)

For production with a domain name, set up Nginx as a reverse proxy:

### 1. Install Nginx

```bash
sudo apt-get install nginx -y
```

### 2. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/isp-recovery
```

Add:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

### 3. Enable and Test Configuration

```bash
sudo ln -s /etc/nginx/sites-available/isp-recovery /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Set Up SSL with Let's Encrypt (Recommended)

```bash
sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Security Configuration

### 1. Firewall Setup (UFW)

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Update Docker Compose for Security

Make sure to:
- Use environment variables for sensitive data
- Keep volumes secure
- Regularly update Docker images

## Managing the Application

### View Logs

```bash
docker-compose logs -f
```

### Stop Application

```bash
docker-compose down
```

### Restart Application

```bash
docker-compose restart
```

### Update Application

```bash
git pull
docker-compose up -d --build
```

### Backup Database

```bash
# Create backup
cp data/isp_recovery.db data/isp_recovery.db.backup.$(date +%Y%m%d)

# Or copy to local machine
scp user@server:/path/to/lucky-nework/data/isp_recovery.db ./backup.db
```

## Monitoring

### Check Container Health

```bash
docker-compose ps
docker stats isp-payment-recovery
```

### Check Application Health

```bash
curl http://localhost:5000/
```

## Troubleshooting

### Container Won't Start

```bash
docker-compose logs
docker-compose down
docker-compose up -d --build
```

### Port Already in Use

Edit `docker-compose.yml` and change port mapping:
```yaml
ports:
  - "8080:5000"  # Change 5000 to 8080
```

### Database Permissions

```bash
sudo chown -R $USER:$USER data/
chmod 755 data/
```

### Out of Memory

Reduce workers in Dockerfile:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", ...]
```

## Cloud Provider Specific Notes

### AWS EC2

1. Configure Security Groups to allow:
   - Port 22 (SSH)
   - Port 80 (HTTP)
   - Port 443 (HTTPS)

2. Use Elastic IP for static IP address

3. Consider using AWS ECS for container orchestration

### DigitalOcean

1. Create a Droplet with Docker pre-installed
2. Use Load Balancer for high availability
3. Enable monitoring and alerts

### Azure

1. Use Azure Container Instances
2. Or deploy to Azure App Service with Docker support
3. Configure Application Gateway for HTTPS

## Production Checklist

- [ ] Domain name configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Database backups scheduled
- [ ] Monitoring set up
- [ ] Logs configured
- [ ] Environment variables set
- [ ] Container health checks working
- [ ] Auto-restart on failure enabled

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Check container status: `docker-compose ps`
3. Review this documentation
4. Check GitHub issues

