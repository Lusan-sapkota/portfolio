#!/bin/bash
# Production Cleanup Script - Strict Mode
# Removes ALL unnecessary development, testing, and documentation files
# WARNING: This script permanently deletes files - use with caution!

set -e  # Exit on any error

echo "🧹 Production Cleanup Script - Lusan Sapkota Portfolio"
echo "====================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
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

print_delete() {
    echo -e "${PURPLE}[DELETE]${NC} $1"
}

print_keep() {
    echo -e "${CYAN}[KEEP]${NC} $1"
}

# Check if running as portfolio user
if [ "$USER" != "portfolio" ] && [ "$USER" != "lusan" ]; then
    print_warning "Consider running as 'portfolio' user for production deployment"
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    print_error "app.py not found. Make sure you're in the portfolio directory"
    exit 1
fi

print_info "Starting production cleanup process..."
echo ""

# Confirmation prompt
print_warning "This script will PERMANENTLY DELETE development and test files!"
print_warning "Make sure you have a backup before proceeding."
echo ""
read -p "Are you sure you want to continue? Type 'YES' to confirm: " confirm

if [ "$confirm" != "YES" ]; then
    print_info "Cleanup cancelled by user"
    exit 0
fi

echo ""
print_info "Proceeding with cleanup..."
echo ""

# Counter for deleted files
deleted_count=0
deleted_size=0

# Function to safely delete file/directory
safe_delete() {
    local path="$1"
    local description="$2"
    
    if [ -e "$path" ]; then
        # Calculate size before deletion
        if [ -f "$path" ]; then
            size=$(stat -f%z "$path" 2>/dev/null || stat -c%s "$path" 2>/dev/null || echo "0")
        elif [ -d "$path" ]; then
            size=$(du -sb "$path" 2>/dev/null | cut -f1 || echo "0")
        else
            size=0
        fi
        
        rm -rf "$path"
        print_delete "$description: $path"
        deleted_count=$((deleted_count + 1))
        deleted_size=$((deleted_size + size))
        return 0
    else
        print_info "Not found (already clean): $path"
        return 1
    fi
}

echo "🗂️  REMOVING DEVELOPMENT DOCUMENTATION:"
echo "========================================"

# Remove development documentation files
safe_delete "ADMIN_CMS_README.md" "Admin CMS documentation"
safe_delete "BACKEND_INTEGRATION_SUMMARY.md" "Backend integration summary"
safe_delete "DONATION_SYSTEM_SUMMARY.md" "Donation system summary"
safe_delete "ADMIN_SECURITY_SUMMARY.md" "Admin security summary"
safe_delete "CMS_IMPLEMENTATION_STATUS.md" "CMS implementation status"
safe_delete "SEO_OPTIMIZATION_COMPLETE.md" "SEO optimization documentation"
safe_delete "GITHUB_CACHING.md" "GitHub caching documentation"
safe_delete "ADMIN_CREDENTIALS.txt" "Admin credentials file"

echo ""
echo "🧪 REMOVING TEST FILES:"
echo "======================="

# Remove all test files
safe_delete "test_subdomain_seo.py" "Subdomain SEO test"
safe_delete "test_backend.py" "Backend test script"
safe_delete "test_new_features.py" "New features test"
safe_delete "test_all_features.py" "All features test"
safe_delete "test_admin_login.py" "Admin login test"
safe_delete "verify_newsletter_fix.py" "Newsletter verification test"

echo ""
echo "📊 REMOVING SAMPLE DATA SCRIPTS (Optional - can be kept for re-population):"
echo "==========================================================================="

read -p "Remove sample data population scripts? (y/N): " remove_samples
if [[ $remove_samples =~ ^[Yy]$ ]]; then
    safe_delete "populate_sample_data.py" "Sample data population script"
    safe_delete "populate_portfolio_data.py" "Portfolio data population script"
    safe_delete "populate_wiki_sample_data.py" "Wiki sample data script"
    safe_delete "populate_donation_sample_data.py" "Donation sample data script"
    safe_delete "populate_git_sample_data.py" "Git sample data script"
    safe_delete "populate_seo_data.py" "SEO data population script"
else
    print_keep "Sample data scripts (for re-population if needed)"
fi

echo ""
echo "🔧 REMOVING DEVELOPMENT DEPENDENCIES:"
echo "===================================="

# Remove development requirements file
if [ -f "requirements.txt" ] && [ -f "requirements-prod.txt" ]; then
    print_info "Found both requirements.txt and requirements-prod.txt"
    
    # Check if requirements.txt contains livereload (development dependency)
    if grep -q "livereload" requirements.txt 2>/dev/null; then
        safe_delete "requirements.txt" "Development requirements file"
        mv requirements-prod.txt requirements.txt
        print_success "Renamed requirements-prod.txt to requirements.txt"
    else
        safe_delete "requirements-prod.txt" "Duplicate production requirements"
        print_keep "requirements.txt (already production-ready)"
    fi
else
    print_keep "requirements.txt (only version found)"
fi

echo ""
echo "🗃️  REMOVING PYTHON CACHE FILES:"
echo "================================"

# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name "*.pyd" -delete 2>/dev/null || true
find . -name ".DS_Store" -delete 2>/dev/null || true

cache_cleaned=$(find . -name "__pycache__" -o -name "*.pyc" -o -name "*.pyo" | wc -l)
if [ "$cache_cleaned" -eq 0 ]; then
    print_success "Python cache files cleaned"
else
    print_delete "Removed $cache_cleaned cache files"
fi

echo ""
echo "📁 REMOVING TEMPORARY AND LOG FILES:"
echo "===================================="

# Remove temporary files
safe_delete ".pytest_cache" "Pytest cache directory"
safe_delete ".coverage" "Coverage report file"
safe_delete "htmlcov" "HTML coverage directory"
safe_delete "*.log" "Log files"
safe_delete "*.tmp" "Temporary files"
safe_delete ".env.example" "Example environment file"
safe_delete ".env.local" "Local environment file"
safe_delete ".env.development" "Development environment file"

echo ""
echo "🔍 CHECKING FOR ADDITIONAL CLEANUP OPPORTUNITIES:"
echo "================================================="

# Check for Git files (optional removal)
if [ -d ".git" ]; then
    read -p "Remove .git directory? (This will remove version control history) (y/N): " remove_git
    if [[ $remove_git =~ ^[Yy]$ ]]; then
        safe_delete ".git" "Git repository directory"
        safe_delete ".gitignore" "Git ignore file"
    else
        print_keep ".git directory (version control preserved)"
    fi
fi

# Check for IDE/Editor files
safe_delete ".vscode" "VS Code settings directory"
safe_delete ".idea" "PyCharm/IntelliJ settings directory"
safe_delete "*.swp" "Vim swap files"
safe_delete "*.swo" "Vim swap files"
safe_delete ".vim" "Vim configuration"

# Check for system files
safe_delete "Thumbs.db" "Windows thumbnail cache"
safe_delete "desktop.ini" "Windows desktop settings"

echo ""
echo "📋 OPTIMIZING REMAINING FILES:"
echo "=============================="

# Optimize remaining Python files (remove debug prints, comments, etc.)
print_info "Checking for development-specific code patterns..."

# Check for debug prints in Python files
debug_files=$(grep -r "print(" --include="*.py" . | grep -v "__pycache__" | wc -l)
if [ "$debug_files" -gt 0 ]; then
    print_warning "Found $debug_files debug print statements in Python files"
    print_info "Consider reviewing and removing debug prints manually"
fi

# Check for development environment checks
dev_checks=$(grep -r "DEBUG.*True" --include="*.py" . | wc -l)
if [ "$dev_checks" -gt 0 ]; then
    print_warning "Found $dev_checks potential development environment checks"
    print_info "Ensure DEBUG=False in production environment"
fi

echo ""
echo "✅ PRODUCTION CLEANUP COMPLETE!"
echo "==============================="

# Convert bytes to human readable
if [ "$deleted_size" -gt 1073741824 ]; then
    size_display="$(echo "scale=2; $deleted_size/1073741824" | bc)GB"
elif [ "$deleted_size" -gt 1048576 ]; then
    size_display="$(echo "scale=2; $deleted_size/1048576" | bc)MB"
elif [ "$deleted_size" -gt 1024 ]; then
    size_display="$(echo "scale=2; $deleted_size/1024" | bc)KB"
else
    size_display="${deleted_size}B"
fi

echo ""
print_success "Cleanup Summary:"
echo "• Files/directories removed: $deleted_count"
echo "• Space freed: $size_display"
echo ""

echo "📦 REMAINING ESSENTIAL FILES:"
echo "============================"
print_keep "Core application files:"
print_keep "  • app.py - Main application"
print_keep "  • models.py - Database models"
print_keep "  • database.py - Database configuration"
print_keep "  • config.py - Application configuration"
print_keep "  • requirements.txt - Python dependencies"
print_keep "  • .env - Environment variables (SECURE THIS!)"

print_keep "Blueprint modules:"
print_keep "  • admin/ - Admin panel"
print_keep "  • wiki/ - Wiki subdomain"
print_keep "  • git/ - Git subdomain"
print_keep "  • donation/ - Donation subdomain"
print_keep "  • store/ - Store subdomain"

print_keep "Templates and static files:"
print_keep "  • templates/ - All templates"
print_keep "  • static/ - CSS, JS, images"

print_keep "Essential utilities:"
print_keep "  • email_service.py - Email functionality"
print_keep "  • github_service.py - GitHub integration"
print_keep "  • create_database.py - Database creation"
print_keep "  • create_admin.py - Admin user creation"
print_keep "  • secure_admin.py - Admin security"
print_keep "  • optimize_seo.py - SEO optimization"
print_keep "  • seo_audit.py - SEO auditing"

print_keep "Deployment files:"
print_keep "  • Procfile - Process configuration"
print_keep "  • quick_deploy.sh - Deployment script"
print_keep "  • setup_cron_jobs.sh - Automation setup"
print_keep "  • DEPLOYMENT_GUIDE.md - Production guide"
print_keep "  • README.md - Project documentation"

echo ""
echo "🔒 SECURITY REMINDERS:"
echo "====================="
print_warning "Before deployment, ensure:"
print_warning "1. .env file contains production values"
print_warning "2. DEBUG=False in environment"
print_warning "3. Strong SECRET_KEY is set"
print_warning "4. Database credentials are secure"
print_warning "5. File permissions are properly set (chmod 600 .env)"

echo ""
echo "🚀 NEXT STEPS:"
echo "=============="
print_info "1. Review remaining files for any missed development code"
print_info "2. Test the application: python app.py"
print_info "3. Run deployment: ./quick_deploy.sh"
print_info "4. Set up automation: ./setup_cron_jobs.sh"
print_info "5. Follow DEPLOYMENT_GUIDE.md for full production setup"

echo ""
print_success "Your portfolio is now production-ready! 🎉"
print_info "The application is optimized for deployment with minimal footprint."

# Final file count
total_files=$(find . -type f | wc -l)
echo ""
print_info "Total remaining files: $total_files"
print_success "Production cleanup completed successfully!"
