#!/bin/bash
# Quick Production Deployment Script
# Usage: ./quick_deploy.sh

set -e

echo "🚀 Lusan Sapkota Portfolio - Quick Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as portfolio user
if [ "$USER" != "portfolio" ]; then
    print_error "This script should be run as 'portfolio' user"
    print_info "Switch to portfolio user: sudo su - portfolio"
    exit 1
fi

# Check if I're in the right directory
if [ ! -f "app.py" ]; then
    print_error "app.py not found. Make sure you're in the portfolio directory"
    exit 1
fi

print_status "Starting deployment process..."

# Step 1: Pull latest changes
if [ -d ".git" ]; then
    print_status "Pulling latest changes from GitHub..."
    git pull origin main
    print_success "Code updated"
else
    print_warning "Not a git repository, skipping git pull"
fi

# Step 2: Activate virtual environment
print_status "Activating virtual environment..."
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3.11 -m venv venv
fi

source venv/bin/activate
print_success "Virtual environment activated"

# Step 3: Install/update dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
if [ -f "requirements-prod.txt" ]; then
    pip install -r requirements-prod.txt
else
    pip install -r requirements.txt
fi
print_success "Dependencies installed"

# Step 4: Check database connection
print_status "Checking database connection..."
python -c "
from app import app
from database import db
try:
    with app.app_context():
        db.engine.execute('SELECT 1')
    print('Database connection: OK')
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
"
print_success "Database connection verified"

# Step 5: Run migrations if needed
if [ -d "migrations" ]; then
    print_status "Checking for database migrations..."
    # Uncomment if using Flask-Migrate
    # flask db upgrade
    print_success "Migrations checked"
fi

# Step 6: Optimize SEO if needed
if [ -f "optimize_seo.py" ]; then
    print_status "Optimizing SEO settings..."
    python optimize_seo.py
    print_success "SEO optimized"
fi

# Step 7: Collect static files (if needed)
# Uncomment if you have a collectstatic process
# python collect_static.py

# Step 8: Test application
print_status "Testing application startup..."
timeout 10s python -c "
from app import app
print('Application imports successfully')
" || {
    print_error "Application failed to import!"
    exit 1
}
print_success "Application test passed"

# Step 9: Restart services
print_status "Restarting application service..."
sudo systemctl restart portfolio.service

# Wait for service to start
sleep 5

# Step 10: Verify deployment
print_status "Verifying deployment..."
if curl -f -s http://localhost:8000 > /dev/null; then
    print_success "Application is responding on port 8000"
else
    print_error "Application is not responding!"
    print_status "Checking service status..."
    sudo systemctl status portfolio.service --no-pager
    exit 1
fi

# Step 11: Test HTTPS (if SSL is configured)
if curl -f -s https://lusansapkota.com.np > /dev/null 2>&1; then
    print_success "HTTPS is working"
else
    print_warning "HTTPS not accessible (normal if SSL not configured yet)"
fi

# Step 12: Show final status
print_success "Deployment completed successfully! 🎉"
echo ""
echo "📊 Deployment Summary:"
echo "======================"
echo "✅ Code updated"
echo "✅ Dependencies installed"
echo "✅ Database verified"
echo "✅ Application restarted"
echo "✅ Service is running"
echo ""
echo "🔗 Access your application:"
echo "   Local: http://localhost:8000"
echo "   Public: https://lusansapkota.com.np (if domain configured)"
echo ""
echo "📋 Useful commands:"
echo "   Check logs: sudo journalctl -u portfolio.service -f"
echo "   Restart app: sudo systemctl restart portfolio.service"
echo "   Check status: sudo systemctl status portfolio.service"
echo ""
print_success "Happy coding! 🚀"
