#!/bin/bash
# Auto-deployment script for Portfolio

set -e

APP_DIR="/home/ubuntu/portfolio"
LOG_FILE="/home/ubuntu/portfolio/deploy.log"

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
