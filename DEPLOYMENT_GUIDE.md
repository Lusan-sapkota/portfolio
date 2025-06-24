# 🚀 Lusan Sapkota Portfolio - Complete Production Deployment Guide

<div align="center">
  
  ![Deployment](https://img.shields.io/badge/Deployment-Oracle%20Cloud-red)
  ![CDN](https://img.shields.io/badge/CDN-Cloudflare-orange)
  ![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
  ![Server](https://img.shields.io/badge/Server-Gunicorn-green)
  
  <h3>Complete setup guide for Oracle Cloud + Cloudflare production deployment</h3>
</div>

---

## 📋 Table of Contents

1. [Server Setup (Oracle Cloud)](#1-server-setup-oracle-cloud)
2. [Python & Dependencies Installation](#2-python--dependencies-installation)
3. [PostgreSQL Database Setup](#3-postgresql-database-setup)
4. [Application Deployment](#4-application-deployment)
5. [Nginx Configuration](#5-nginx-configuration)
6. [SSL Setup (Let's Encrypt)](#6-ssl-setup-lets-encrypt)
7. [Cloudflare Configuration](#7-cloudflare-configuration)
8. [Environment Configuration](#8-environment-configuration)
9. [Database Population & SEO](#9-database-population--seo)
10. [Systemd Services](#10-systemd-services)
11. [Auto-deployment with GitHub](#11-auto-deployment-with-github)
12. [Subdomain Setup (Ngrok Alternative)](#12-subdomain-setup-ngrok-alternative)
13. [Files to Delete/Keep](#13-files-to-deletekeep)
14. [Monitoring & Maintenance](#14-monitoring--maintenance)
15. [Security Hardening](#15-security-hardening)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. Server Setup (Oracle Cloud)

### 1.1 Create Oracle Cloud Instance

```bash
# Create Always Free VM instance (AMD or ARM based)
# Choose Ubuntu 22.04 LTS
# Configure:
# - Memory: 1GB (Free tier) or 6GB (ARM)
# - Storage: 50GB+ recommended
# - Bandwidth: 10TB free per month
```

### 1.2 Initial Server Configuration

```bash
# Connect to your server
ssh -i ~/.ssh/oracle_key ubuntu@YOUR_SERVER_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git unzip vim htop tree software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# Create portfolio user
sudo adduser portfolio
sudo usermod -aG sudo portfolio

# Configure SSH for portfolio user
sudo mkdir -p /home/portfolio/.ssh
sudo cp ~/.ssh/authorized_keys /home/portfolio/.ssh/
sudo chown -R portfolio:portfolio /home/portfolio/.ssh
sudo chmod 700 /home/portfolio/.ssh
sudo chmod 600 /home/portfolio/.ssh/authorized_keys

# Switch to portfolio user
sudo su - portfolio
```

### 1.3 Configure Firewall

```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp  # For testing
sudo ufw status
```

---

## 2. Python & Dependencies Installation

### 2.1 Install Python 3.11+

```bash
# Add deadsnakes PPA for latest Python
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Set Python 3.11 as default (optional)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo update-alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3 1

# Verify installation
python3 --version  # Should show Python 3.11.x
pip3 --version
```

### 2.2 Install System Dependencies

```bash
# Install build dependencies
sudo apt install -y build-essential libssl-dev libffi-dev python3.11-distutils

# Install PostgreSQL client libraries
sudo apt install -y libpq-dev

# Install Nginx
sudo apt install -y nginx

# Install Redis
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

---

## 3. PostgreSQL Database Setup

### 3.1 Install PostgreSQL

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check status
sudo systemctl status postgresql
```

### 3.2 Configure PostgreSQL

```bash
# Switch to postgres user
sudo -i -u postgres

# Create database and user
createdb portfolio
createuser --interactive portfolio
# Answer: y (superuser for development, or n and grant specific permissions)

# Set password for portfolio user
psql
ALTER USER portfolio PASSWORD 'your_secure_database_password';
GRANT ALL PRIVILEGES ON DATABASE portfolio TO portfolio;
\q
exit

# Test connection
psql -U portfolio -d portfolio -h localhost
# Enter password when prompted
\q
```

### 3.3 Configure PostgreSQL for Production

```bash
# Edit PostgreSQL configuration
sudo vim /etc/postgresql/14/main/postgresql.conf

# Add/modify these settings:
listen_addresses = 'localhost'
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100

# Edit pg_hba.conf for authentication
sudo vim /etc/postgresql/14/main/pg_hba.conf

# Add this line for local connections:
local   portfolio   portfolio                     md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## 4. Application Deployment

### 4.1 Clone Repository

```bash
# Navigate to home directory
cd /home/portfolio

# Clone your repository
git clone https://github.com/yourusername/portfolio.git
cd portfolio

# Or upload files directly
# Use scp, rsync, or upload via GitHub
```

### 4.2 Create Python Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install additional production packages
pip install gunicorn supervisor
```

### 4.3 Create Environment Configuration

```bash
# Create production .env file
vim .env
```

Add the following content to `.env`:

```bash
# Database Configuration
DATABASE_URL=postgresql://portfolio:your_secure_database_password@localhost/portfolio

# Flask Configuration
SECRET_KEY=your_super_secret_key_here_minimum_32_characters
DEBUG=False
FLASK_ENV=production

# Server Configuration
SERVER_NAME=lusansapkota.com.np
APP_HOST=0.0.0.0
APP_PORT=8000

# Email Configuration (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
FROM_NAME=Lusan Sapkota
ADMIN_EMAIL=contact@lusansapkota.com.np

# GitHub Integration
GITHUB_TOKEN=your_github_personal_access_token

# Rate Limiting
REDIS_URL=redis://localhost:6379/0

# Security Headers
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Analytics (Optional)
GOOGLE_ANALYTICS_ID=your_ga_id
```

### 4.4 Secure the Environment File

```bash
# Set proper permissions
chmod 600 .env
```

---

## 5. Nginx Configuration

### 5.1 Create Nginx Site Configuration

```bash
# Create site configuration
sudo vim /etc/nginx/sites-available/lusansapkota
```

Add the following configuration:

```nginx
# Main domain and subdomains configuration
server {
    listen 80;
    server_name lusansapkota.com.np www.lusansapkota.com.np wiki.lusansapkota.com.np git.lusansapkota.com.np donation.lusansapkota.com.np store.lusansapkota.com.np;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name lusansapkota.com.np www.lusansapkota.com.np;
    
    # SSL certificates (will be added by certbot)
    ssl_certificate /etc/letsencrypt/live/lusansapkota.com.np/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lusansapkota.com.np/privkey.pem;
    
    # SSL security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self';" always;
    
    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Static files
    location /static {
        alias /home/portfolio/portfolio/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Robots and sitemap
    location /robots.txt {
        alias /home/portfolio/portfolio/static/robots.txt;
    }
    
    location /sitemap.xml {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Main application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeout settings
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
}

# Subdomain configurations
server {
    listen 443 ssl http2;
    server_name wiki.lusansapkota.com.np;
    
    ssl_certificate /etc/letsencrypt/live/lusansapkota.com.np/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lusansapkota.com.np/privkey.pem;
    
    include /etc/nginx/snippets/ssl-security.conf;
    include /etc/nginx/snippets/security-headers.conf;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 443 ssl http2;
    server_name git.lusansapkota.com.np;
    
    ssl_certificate /etc/letsencrypt/live/lusansapkota.com.np/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lusansapkota.com.np/privkey.pem;
    
    include /etc/nginx/snippets/ssl-security.conf;
    include /etc/nginx/snippets/security-headers.conf;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 443 ssl http2;
    server_name donation.lusansapkota.com.np;
    
    ssl_certificate /etc/letsencrypt/live/lusansapkota.com.np/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lusansapkota.com.np/privkey.pem;
    
    include /etc/nginx/snippets/ssl-security.conf;
    include /etc/nginx/snippets/security-headers.conf;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 443 ssl http2;
    server_name store.lusansapkota.com.np;
    
    ssl_certificate /etc/letsencrypt/live/lusansapkota.com.np/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lusansapkota.com.np/privkey.pem;
    
    include /etc/nginx/snippets/ssl-security.conf;
    include /etc/nginx/snippets/security-headers.conf;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5.2 Create Nginx Snippets

```bash
# Create SSL security snippet
sudo vim /etc/nginx/snippets/ssl-security.conf
```

Add:

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers off;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_stapling on;
ssl_stapling_verify on;
```

```bash
# Create security headers snippet
sudo vim /etc/nginx/snippets/security-headers.conf
```

Add:

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options DENY always;
add_header X-Content-Type-Options nosniff always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

### 5.3 Enable Site

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/lusansapkota /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Start and enable Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

## 6. SSL Setup (Let's Encrypt)

### 6.1 Install Certbot

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Stop nginx temporarily
sudo systemctl stop nginx
```

### 6.2 Obtain SSL Certificates

```bash
# Get certificates for all domains
sudo certbot certonly --standalone -d lusansapkota.com.np -d www.lusansapkota.com.np -d wiki.lusansapkota.com.np -d git.lusansapkota.com.np -d donation.lusansapkota.com.np -d store.lusansapkota.com.np

# Start nginx
sudo systemctl start nginx

# Setup auto-renewal
sudo crontab -e

# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet && systemctl reload nginx
```

---

## 7. Cloudflare Configuration

### 7.1 Domain Setup

1. **Add Domain to Cloudflare**:
   - Go to Cloudflare dashboard
   - Add `lusansapkota.com.np`
   - Change nameservers at your domain registrar

2. **DNS Records**:
```
Type    Name                Value               Proxy
A       @                   YOUR_SERVER_IP      ✅ Proxied
A       www                 YOUR_SERVER_IP      ✅ Proxied
A       wiki                YOUR_SERVER_IP      ✅ Proxied
A       git                 YOUR_SERVER_IP      ✅ Proxied
A       donation            YOUR_SERVER_IP      ✅ Proxied
A       store               YOUR_SERVER_IP      ✅ Proxied
CNAME   *.lusansapkota     lusansapkota.com.np  ✅ Proxied
```

### 7.2 Cloudflare Settings

**SSL/TLS Settings**:
- Encryption mode: "Full (strict)"
- Always Use HTTPS: ✅ Enabled
- HTTP Strict Transport Security (HSTS): ✅ Enabled

**Speed Settings**:
- Auto Minify: ✅ JavaScript, CSS, HTML
- Brotli: ✅ Enabled
- Early Hints: ✅ Enabled

**Caching**:
- Caching Level: Standard
- Browser Cache TTL: 1 year
- Always Online: ✅ Enabled

**Security**:
- Security Level: Medium
- Bot Fight Mode: ✅ Enabled
- Rate Limiting: Configure as needed

**Page Rules**:
```
1. *.lusansapkota.com.np/static/*
   Cache Level: Cache Everything
   Browser Cache TTL: 1 year
   Edge Cache TTL: 1 month

2. lusansapkota.com.np/admin/*
   Security Level: High
   Cache Level: Bypass

3. lusansapkota.com.np/api/*
   Cache Level: Bypass
```

---

## 8. Environment Configuration

### 8.1 Update Environment Variables

Edit `/home/portfolio/portfolio/.env`:

```bash
# Production Database URL
DATABASE_URL=postgresql://portfolio:your_secure_password@localhost/portfolio

# Production Secret Key (generate new one)
SECRET_KEY=your_production_secret_key_32_chars_minimum

# Production Mode
DEBUG=False
FLASK_ENV=production

# Server Configuration for Production
SERVER_NAME=lusansapkota.com.np
APP_HOST=0.0.0.0
APP_PORT=8000

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
FROM_NAME=Lusan Sapkota
ADMIN_EMAIL=contact@lusansapkota.com.np

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Redis for Production
REDIS_URL=redis://localhost:6379/0

# GitHub API
GITHUB_TOKEN=your_github_token

# Analytics (Optional)
GOOGLE_ANALYTICS_ID=your_analytics_id
```

---

## 9. Database Population & SEO

### 9.1 Initialize Database

```bash
# Navigate to project directory
cd /home/portfolio/portfolio

# Activate virtual environment
source venv/bin/activate

# Create database tables
python create_database.py

# Create admin user
python create_admin.py

# Populate with sample data
python populate_sample_data.py

# Optimize SEO
python optimize_seo.py

# Populate portfolio data
python populate_portfolio_data.py

# Setup donation system
python migrate_donation_system.py

# Add wiki sample data
python populate_wiki_sample_data.py

# Add git sample data
python populate_git_sample_data.py
```

### 9.2 Verify Database Setup

```bash
# Test database connection
python -c "
from app import app
from database import db
from models import User, Project, SeoSettings
with app.app_context():
    print('Database tables:', db.engine.table_names())
    print('Admin users:', User.query.filter_by(is_admin=True).count())
    print('Projects:', Project.query.count())
    print('SEO settings:', SeoSettings.query.count())
"
```

---

## 10. Systemd Services

### 10.1 Create Gunicorn Service

```bash
# Create service file
sudo vim /etc/systemd/system/portfolio.service
```

Add:

```ini
[Unit]
Description=Lusan Sapkota Portfolio Application
After=network.target postgresql.service redis.service

[Service]
User=portfolio
Group=portfolio
WorkingDirectory=/home/portfolio/portfolio
Environment=PATH=/home/portfolio/portfolio/venv/bin
ExecStart=/home/portfolio/portfolio/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 50 app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/home/portfolio/portfolio

[Install]
WantedBy=multi-user.target
```

### 10.2 Create Backup Service

```bash
# Create backup script
vim /home/portfolio/backup.sh
```

Add:

```bash
#!/bin/bash
# Portfolio Backup Script

BACKUP_DIR="/home/portfolio/backups"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/home/portfolio/portfolio"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U portfolio -h localhost portfolio > "$BACKUP_DIR/db_backup_$DATE.sql"

# Application files backup
tar -czf "$BACKUP_DIR/app_backup_$DATE.tar.gz" -C /home/portfolio portfolio

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# Make executable
chmod +x /home/portfolio/backup.sh

# Create backup service
sudo vim /etc/systemd/system/portfolio-backup.service
```

Add:

```ini
[Unit]
Description=Portfolio Backup Service

[Service]
Type=oneshot
User=portfolio
ExecStart=/home/portfolio/backup.sh
```

```bash
# Create backup timer
sudo vim /etc/systemd/system/portfolio-backup.timer
```

Add:

```ini
[Unit]
Description=Portfolio Backup Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

### 10.3 Enable Services

```bash
# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable portfolio.service
sudo systemctl start portfolio.service

# Enable backup timer
sudo systemctl enable portfolio-backup.timer
sudo systemctl start portfolio-backup.timer

# Check status
sudo systemctl status portfolio.service
sudo systemctl status portfolio-backup.timer
```

---

## 11. Auto-deployment with GitHub

### 11.1 Create Deployment Script

```bash
# Create deployment script
vim /home/portfolio/deploy.sh
```

Add:

```bash
#!/bin/bash
# Auto-deployment script for Portfolio

set -e

APP_DIR="/home/portfolio/portfolio"
LOG_FILE="/home/portfolio/deploy.log"

echo "$(date): Starting deployment..." >> $LOG_FILE

cd $APP_DIR

# Pull latest changes
echo "$(date): Pulling latest changes..." >> $LOG_FILE
git pull origin main >> $LOG_FILE 2>&1

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "$(date): Installing dependencies..." >> $LOG_FILE
pip install -r requirements.txt >> $LOG_FILE 2>&1

# Run database migrations if any
echo "$(date): Running database migrations..." >> $LOG_FILE
# Add migration commands here if using Flask-Migrate

# Collect static files (if needed)
# python manage.py collectstatic --noinput

# Restart application
echo "$(date): Restarting application..." >> $LOG_FILE
sudo systemctl restart portfolio.service

# Test if application is running
sleep 5
if curl -f http://localhost:8000 > /dev/null 2>&1; then
    echo "$(date): Deployment successful!" >> $LOG_FILE
else
    echo "$(date): Deployment failed - application not responding!" >> $LOG_FILE
    exit 1
fi

echo "$(date): Deployment completed successfully." >> $LOG_FILE
```

```bash
# Make executable
chmod +x /home/portfolio/deploy.sh
```

### 11.2 Setup GitHub Webhook (Optional)

Create webhook endpoint in your Flask app or use GitHub Actions:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: portfolio
        key: ${{ secrets.PRIVATE_KEY }}
        script: |
          cd /home/portfolio/portfolio
          ./deploy.sh
```

### 11.3 Setup Cron Job for Auto-pull

```bash
# Edit crontab
crontab -e

# Add this line to pull changes every 30 minutes
*/30 * * * * cd /home/portfolio/portfolio && git pull origin main > /dev/null 2>&1 && ./deploy.sh > /dev/null 2>&1
```

---

## 12. Subdomain Setup (Ngrok Alternative)

### 12.1 Production Subdomain Configuration

Your Flask app is already configured for subdomains. The configuration in `app.py` handles:

- Main domain: `lusansapkota.com.np`
- Wiki: `wiki.lusansapkota.com.np`
- Git: `git.lusansapkota.com.np`
- Donation: `donation.lusansapkota.com.np`
- Store: `store.lusansapkota.com.np`

### 12.2 Test Subdomain Routing

```bash
# Test subdomain routing
curl -H "Host: wiki.lusansapkota.com.np" http://localhost:8000/
curl -H "Host: git.lusansapkota.com.np" http://localhost:8000/
curl -H "Host: donation.lusansapkota.com.np" http://localhost:8000/
curl -H "Host: store.lusansapkota.com.np" http://localhost:8000/
```

---

## 13. Files to Delete/Keep

### 13.1 Files to DELETE in Production

```bash
# Navigate to project directory
cd /home/portfolio/portfolio

# Delete development files
rm -f requirements-dev.txt
rm -f .env.example
rm -f .gitignore

# Delete test files
rm -f test_*.py
rm -f *_test.py

# Delete documentation that's not needed in production
rm -f README.md
rm -f ADMIN_CMS_README.md
rm -f CMS_IMPLEMENTATION_STATUS.md
rm -f BACKEND_INTEGRATION_SUMMARY.md
rm -f DONATION_SYSTEM_SUMMARY.md
rm -f ADMIN_SECURITY_SUMMARY.md
rm -f GITHUB_CACHING.md
rm -f SEO_OPTIMIZATION_COMPLETE.md

# Delete development scripts
rm -f verify_newsletter_fix.py
rm -f test_admin_login.py
rm -f test_all_features.py
rm -f test_backend.py
rm -f test_new_features.py
rm -f test_subdomain_seo.py

# Delete sample data scripts (optional, keep if you want to repopulate)
# rm -f populate_sample_data.py
# rm -f populate_portfolio_data.py
# rm -f populate_wiki_sample_data.py
# rm -f populate_git_sample_data.py
# rm -f populate_donation_sample_data.py

# Delete __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
```

### 13.2 Files to KEEP in Production

**Essential Application Files:**
- `app.py` - Main application
- `models.py` - Database models
- `database.py` - Database configuration
- `config.py` - Application configuration
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (secure this file!)

**Blueprint Modules:**
- `admin/` - Admin panel
- `wiki/` - Wiki subdomain
- `git/` - Git subdomain
- `donation/` - Donation subdomain
- `store/` - Store subdomain

**Templates and Static Files:**
- `templates/` - All templates
- `static/` - CSS, JS, images

**Database and Migration Files:**
- `migrations/` - Database migrations
- `create_database.py` - Database creation script
- `create_admin.py` - Admin user creation

**Utility Scripts (Recommended to Keep):**
- `email_service.py` - Email functionality
- `github_service.py` - GitHub integration
- `commands.py` - CLI commands
- `secure_admin.py` - Admin security setup
- `seo_audit.py` - SEO auditing
- `optimize_seo.py` - SEO optimization

**Migration Scripts (Keep for updates):**
- `migrate_*.py` - Database migration scripts
- `add_*.py` - Database addition scripts

---

## 14. Monitoring & Maintenance

### 14.1 Log Configuration

```bash
# Create log directory
mkdir -p /home/portfolio/logs

# Create log rotation configuration
sudo vim /etc/logrotate.d/portfolio
```

Add:

```
/home/portfolio/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 0644 portfolio portfolio
    postrotate
        systemctl reload portfolio
    endscript
}
```

### 14.2 Monitoring Script

```bash
# Create monitoring script
vim /home/portfolio/monitor.sh
```

Add:

```bash
#!/bin/bash
# Portfolio Monitoring Script

LOG_FILE="/home/portfolio/monitor.log"
APP_URL="https://lusansapkota.com.np"

# Check if application is responding
if curl -f -s $APP_URL > /dev/null; then
    echo "$(date): Application is running" >> $LOG_FILE
else
    echo "$(date): Application is down! Attempting restart..." >> $LOG_FILE
    sudo systemctl restart portfolio.service
    sleep 10
    if curl -f -s $APP_URL > /dev/null; then
        echo "$(date): Application restarted successfully" >> $LOG_FILE
    else
        echo "$(date): Failed to restart application!" >> $LOG_FILE
        # Send alert email here if configured
    fi
fi

# Check database connectivity
if python3 -c "from app import app; from database import db; app.app_context().push(); db.engine.execute('SELECT 1')" 2>/dev/null; then
    echo "$(date): Database is accessible" >> $LOG_FILE
else
    echo "$(date): Database connection failed!" >> $LOG_FILE
fi

# Check disk space
DISK_USAGE=$(df -h /home/portfolio | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$(date): Warning: Disk usage is at ${DISK_USAGE}%" >> $LOG_FILE
fi
```

```bash
# Make executable
chmod +x /home/portfolio/monitor.sh

# Add to crontab to run every 5 minutes
crontab -e

# Add:
*/5 * * * * /home/portfolio/monitor.sh
```

### 14.3 Performance Monitoring

```bash
# Install htop for system monitoring
sudo apt install -y htop iotop

# Create performance check script
vim /home/portfolio/performance_check.sh
```

Add:

```bash
#!/bin/bash
# Performance monitoring

LOG_FILE="/home/portfolio/performance.log"

echo "$(date): Performance Check" >> $LOG_FILE
echo "Memory Usage:" >> $LOG_FILE
free -h >> $LOG_FILE
echo "CPU Usage:" >> $LOG_FILE
top -bn1 | grep "Cpu(s)" >> $LOG_FILE
echo "Disk Usage:" >> $LOG_FILE
df -h >> $LOG_FILE
echo "Application Process:" >> $LOG_FILE
ps aux | grep gunicorn >> $LOG_FILE
echo "---" >> $LOG_FILE
```

---

## 15. Security Hardening

### 15.1 SSH Hardening

```bash
# Edit SSH configuration
sudo vim /etc/ssh/sshd_config
```

Add/modify:

```
# Disable root login
PermitRootLogin no

# Use key-based authentication only
PasswordAuthentication no
PubkeyAuthentication yes

# Limit users
AllowUsers portfolio

# Change default port (optional)
Port 2222

# Disable unused features
X11Forwarding no
AllowTcpForwarding no
```

```bash
# Restart SSH service
sudo systemctl restart ssh
```

### 15.2 Fail2Ban Setup

```bash
# Install fail2ban
sudo apt install -y fail2ban

# Create jail configuration
sudo vim /etc/fail2ban/jail.local
```

Add:

```ini
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
logpath = /var/log/nginx/error.log

[nginx-req-limit]
enabled = true
filter = nginx-req-limit
logpath = /var/log/nginx/error.log
```

```bash
# Start and enable fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 15.3 Application Security

```bash
# Set proper file permissions
chmod 755 /home/portfolio/portfolio
chmod -R 644 /home/portfolio/portfolio/templates
chmod -R 644 /home/portfolio/portfolio/static
chmod 600 /home/portfolio/portfolio/.env
chmod +x /home/portfolio/portfolio/app.py

# Create secure directories
mkdir -p /home/portfolio/portfolio/logs
chmod 755 /home/portfolio/portfolio/logs

# Secure database credentials
sudo -u postgres psql
ALTER USER portfolio WITH PASSWORD 'new_super_secure_password';
\q
```

---

## 16. Troubleshooting

### 16.1 Common Issues and Solutions

**Application won't start:**
```bash
# Check logs
sudo journalctl -u portfolio.service -f

# Check Python environment
source /home/portfolio/portfolio/venv/bin/activate
python app.py

# Check dependencies
pip check
```

**Database connection issues:**
```bash
# Test database connection
psql -U portfolio -d portfolio -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql

# Check logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

**Nginx configuration issues:**
```bash
# Test configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

**SSL certificate issues:**
```bash
# Check certificate status
sudo certbot certificates

# Renew certificates
sudo certbot renew --dry-run

# Check SSL configuration
openssl s_client -connect lusansapkota.com.np:443
```

### 16.2 Performance Issues

**High memory usage:**
```bash
# Check Gunicorn workers
ps aux | grep gunicorn

# Restart application
sudo systemctl restart portfolio.service

# Optimize Gunicorn configuration
# Edit worker count in service file
```

**Slow database queries:**
```bash
# Enable PostgreSQL logging
sudo vim /etc/postgresql/14/main/postgresql.conf

# Add:
log_statement = 'all'
log_min_duration_statement = 1000

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### 16.3 Backup and Recovery

**Emergency backup:**
```bash
# Quick database backup
pg_dump -U portfolio portfolio > emergency_backup.sql

# Quick file backup
tar -czf emergency_files.tar.gz /home/portfolio/portfolio
```

**Recovery from backup:**
```bash
# Restore database
dropdb -U portfolio portfolio
createdb -U portfolio portfolio
psql -U portfolio portfolio < backup.sql

# Restore files
tar -xzf backup_files.tar.gz
```

---

## 🎯 Final Production Checklist

### Before Going Live:

- [ ] Server setup completed
- [ ] Python 3.11+ installed
- [ ] PostgreSQL configured and secured
- [ ] Virtual environment created and activated
- [ ] All dependencies installed from requirements.txt
- [ ] Environment variables configured in .env
- [ ] Database tables created
- [ ] Admin user created and tested
- [ ] Sample data populated (optional)
- [ ] SEO optimization completed
- [ ] Nginx configured and tested
- [ ] SSL certificates obtained and configured
- [ ] Cloudflare DNS configured
- [ ] Systemd services created and enabled
- [ ] Firewall configured
- [ ] Security hardening completed
- [ ] Monitoring scripts set up
- [ ] Backup system configured
- [ ] Auto-deployment configured
- [ ] All test files removed
- [ ] File permissions secured
- [ ] Performance tested
- [ ] All subdomains tested
- [ ] Email functionality tested

### Post-Deployment:

- [ ] Monitor application logs
- [ ] Check SSL certificate auto-renewal
- [ ] Verify backup system is working
- [ ] Test all subdomains
- [ ] Run SEO audit
- [ ] Set up Google Analytics (optional)
- [ ] Submit sitemap to Google Search Console
- [ ] Monitor server performance
- [ ] Test contact forms and newsletter
- [ ] Verify admin panel access
- [ ] Document any custom configurations

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks:

**Daily:**
- Check application status
- Monitor error logs
- Verify backup completion

**Weekly:**
- Review security logs
- Check disk space
- Update dependencies (if needed)

**Monthly:**
- Review SSL certificate status
- Analyze performance metrics
- Update system packages
- Review and clean logs

**Quarterly:**
- Security audit
- Performance optimization
- Backup testing
- Documentation updates

---

## 🚀 Deployment Complete!

Your Lusan Sapkota Portfolio is now ready for production with:

✅ **High-performance Oracle Cloud hosting**
✅ **Global CDN via Cloudflare**
✅ **SSL encryption for all domains**
✅ **Automated backups and monitoring**
✅ **Security hardening implemented**
✅ **SEO optimization (100/100 score)**
✅ **Multi-subdomain support**
✅ **Auto-deployment pipeline**
✅ **Professional admin panel**
✅ **Email integration**
✅ **Database optimization**

Your portfolio is now enterprise-ready and can handle production traffic! 🎉

---

**Note**: Remember to update passwords, tokens, and sensitive information with your actual production values. Keep your `.env` file secure and never commit it to version control.
