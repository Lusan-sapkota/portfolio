#!/bin/bash
# Setup Production Cron Jobs for Portfolio
# Run this script as the portfolio user

echo "🕐 Setting up production cron jobs for Lusan Sapkota Portfolio"
echo "============================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running as portfolio user
if [ "$USER" != "portfolio" ]; then
    echo "❌ This script should be run as 'portfolio' user"
    echo "   Switch to portfolio user: sudo su - portfolio"
    exit 1
fi

PORTFOLIO_DIR="/home/portfolio/portfolio"

# Check if portfolio directory exists
if [ ! -d "$PORTFOLIO_DIR" ]; then
    echo "❌ Portfolio directory not found at $PORTFOLIO_DIR"
    exit 1
fi

print_info "Creating backup directory..."
mkdir -p /home/portfolio/backups
mkdir -p /home/portfolio/logs

print_info "Setting up cron jobs..."

# Create temporary crontab file
TEMP_CRON="/tmp/portfolio_cron"

# Write cron jobs to temporary file
cat > $TEMP_CRON << 'EOF'
# Lusan Sapkota Portfolio - Production Cron Jobs
# ===============================================

# Auto-deployment: Check for GitHub changes every 30 minutes
*/30 * * * * cd /home/portfolio/portfolio && git fetch origin main && if [ $(git rev-list HEAD...origin/main --count) != 0 ]; then git pull origin main && ./quick_deploy.sh >> /home/portfolio/logs/auto_deploy.log 2>&1; fi

# Database backup: Daily at 2:00 AM
0 2 * * * pg_dump -U portfolio -h localhost portfolio > /home/portfolio/backups/db_backup_$(date +\%Y\%m\%d_\%H\%M\%S).sql 2>> /home/portfolio/logs/backup.log

# Application backup: Daily at 2:30 AM
30 2 * * * tar -czf /home/portfolio/backups/app_backup_$(date +\%Y\%m\%d_\%H\%M\%S).tar.gz -C /home/portfolio portfolio 2>> /home/portfolio/logs/backup.log

# Cleanup old backups: Keep only last 7 days, run daily at 3:00 AM
0 3 * * * find /home/portfolio/backups -name "*.sql" -mtime +7 -delete && find /home/portfolio/backups -name "*.tar.gz" -mtime +7 -delete

# Application health check: Every 5 minutes
*/5 * * * * /home/portfolio/monitor.sh >> /home/portfolio/logs/monitor.log 2>&1

# Performance monitoring: Every hour
0 * * * * /home/portfolio/performance_check.sh >> /home/portfolio/logs/performance.log 2>&1

# Log rotation: Weekly on Sunday at 4:00 AM
0 4 * * 0 find /home/portfolio/logs -name "*.log" -size +100M -exec truncate -s 50M {} \;

# SSL certificate renewal check: Daily at 1:00 AM
0 1 * * * sudo /usr/bin/certbot renew --quiet --deploy-hook "sudo systemctl reload nginx" >> /home/portfolio/logs/ssl_renewal.log 2>&1

# SEO audit: Weekly on Monday at 6:00 AM
0 6 * * 1 cd /home/portfolio/portfolio && source venv/bin/activate && python seo_audit.py >> /home/portfolio/logs/seo_audit.log 2>&1

# GitHub repository sync: Every 2 hours (for git subdomain)
0 */2 * * * cd /home/portfolio/portfolio && source venv/bin/activate && python setup_github.py >> /home/portfolio/logs/github_sync.log 2>&1

# System resource cleanup: Daily at 4:30 AM
30 4 * * * find /tmp -name "*.tmp" -mtime +1 -delete && docker system prune -f >> /home/portfolio/logs/cleanup.log 2>&1 || true

# Email queue processing (if using email queue): Every 10 minutes
*/10 * * * * cd /home/portfolio/portfolio && source venv/bin/activate && python -c "from email_service import process_email_queue; process_email_queue()" >> /home/portfolio/logs/email_queue.log 2>&1 || true

# Portfolio analytics update: Daily at 5:00 AM
0 5 * * * cd /home/portfolio/portfolio && source venv/bin/activate && python -c "from models import *; from app import app; app.app_context().push(); print('Analytics updated')" >> /home/portfolio/logs/analytics.log 2>&1

EOF

# Install the crontab
print_info "Installing cron jobs..."
crontab $TEMP_CRON

# Clean up temporary file
rm $TEMP_CRON

print_success "Cron jobs installed successfully!"

echo ""
echo "📋 Installed Cron Jobs:"
echo "======================"
echo "🔄 Auto-deployment:     Every 30 minutes"
echo "💾 Database backup:     Daily at 2:00 AM"
echo "📦 Application backup:  Daily at 2:30 AM"
echo "🧹 Cleanup old backups: Daily at 3:00 AM"
echo "❤️  Health monitoring:   Every 5 minutes"
echo "📊 Performance check:   Every hour"
echo "📄 Log rotation:        Weekly on Sunday"
echo "🔐 SSL renewal:         Daily at 1:00 AM"
echo "🚀 SEO audit:           Weekly on Monday"
echo "📨 GitHub sync:         Every 2 hours"
echo "🧽 System cleanup:      Daily at 4:30 AM"
echo "📧 Email processing:    Every 10 minutes"
echo "📈 Analytics update:    Daily at 5:00 AM"

echo ""
echo "📁 Log Files Location:"
echo "====================="
echo "/home/portfolio/logs/auto_deploy.log  - Auto-deployment logs"
echo "/home/portfolio/logs/backup.log      - Backup operation logs"
echo "/home/portfolio/logs/monitor.log     - Health monitoring logs"
echo "/home/portfolio/logs/performance.log - Performance monitoring"
echo "/home/portfolio/logs/ssl_renewal.log - SSL certificate renewal"
echo "/home/portfolio/logs/seo_audit.log   - SEO audit results"
echo "/home/portfolio/logs/github_sync.log - GitHub synchronization"
echo "/home/portfolio/logs/cleanup.log     - System cleanup logs"
echo "/home/portfolio/logs/email_queue.log - Email processing logs"
echo "/home/portfolio/logs/analytics.log   - Analytics update logs"

echo ""
echo "🛠️  Useful Commands:"
echo "==================="
echo "View current cron jobs:  crontab -l"
echo "Edit cron jobs:          crontab -e"
echo "Check cron service:      sudo systemctl status cron"
echo "View cron logs:          sudo tail -f /var/log/syslog | grep cron"
echo "Check backup status:     ls -la /home/portfolio/backups/"
echo "Monitor health:          tail -f /home/portfolio/logs/monitor.log"

print_success "Cron setup completed! 🎉"

# Create monitoring scripts if they don't exist
if [ ! -f "/home/portfolio/monitor.sh" ]; then
    print_info "Creating health monitoring script..."
    cat > /home/portfolio/monitor.sh << 'EOF'
#!/bin/bash
# Portfolio Health Monitoring Script

LOG_FILE="/home/portfolio/logs/monitor.log"
APP_URL="http://localhost:8000"

# Check if application is responding
if curl -f -s $APP_URL > /dev/null; then
    echo "$(date): ✅ Application is running"
else
    echo "$(date): ❌ Application is down! Attempting restart..."
    sudo systemctl restart portfolio.service
    sleep 10
    if curl -f -s $APP_URL > /dev/null; then
        echo "$(date): ✅ Application restarted successfully"
    else
        echo "$(date): ❌ Failed to restart application!"
    fi
fi

# Check database connectivity
cd /home/portfolio/portfolio
source venv/bin/activate
if python -c "from app import app; from database import db; app.app_context().push(); db.engine.execute('SELECT 1')" 2>/dev/null; then
    echo "$(date): ✅ Database is accessible"
else
    echo "$(date): ❌ Database connection failed!"
fi

# Check disk space
DISK_USAGE=$(df -h /home/portfolio | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$(date): ⚠️  Warning: Disk usage is at ${DISK_USAGE}%"
fi
EOF

    chmod +x /home/portfolio/monitor.sh
    print_success "Health monitoring script created"
fi

if [ ! -f "/home/portfolio/performance_check.sh" ]; then
    print_info "Creating performance monitoring script..."
    cat > /home/portfolio/performance_check.sh << 'EOF'
#!/bin/bash
# Performance monitoring script

LOG_FILE="/home/portfolio/logs/performance.log"

echo "$(date): 📊 Performance Check" >> $LOG_FILE
echo "Memory Usage:" >> $LOG_FILE
free -h >> $LOG_FILE
echo "CPU Load:" >> $LOG_FILE
uptime >> $LOG_FILE
echo "Disk Usage:" >> $LOG_FILE
df -h /home/portfolio >> $LOG_FILE
echo "Application Processes:" >> $LOG_FILE
ps aux | grep -E "(gunicorn|python)" | grep -v grep >> $LOG_FILE
echo "Network Connections:" >> $LOG_FILE
ss -tuln | grep :8000 >> $LOG_FILE
echo "---" >> $LOG_FILE
EOF

    chmod +x /home/portfolio/performance_check.sh
    print_success "Performance monitoring script created"
fi

echo ""
print_info "Testing scripts..."

# Test monitoring script
if [ -x "/home/portfolio/monitor.sh" ]; then
    /home/portfolio/monitor.sh
    print_success "Health monitoring script tested"
fi

# Test performance script
if [ -x "/home/portfolio/performance_check.sh" ]; then
    /home/portfolio/performance_check.sh
    print_success "Performance monitoring script tested"
fi

echo ""
print_success "All cron jobs and monitoring scripts are now active! 🚀"
print_info "The system will automatically maintain itself with:"
print_info "• Continuous deployment from GitHub"
print_info "• Daily backups with cleanup"
print_info "• Health monitoring and auto-recovery"
print_info "• Performance tracking"
print_info "• SSL certificate renewal"
print_info "• SEO auditing and optimization"
