#!/bin/bash

# CV Webapp Update Script
# Run this after pushing changes to GitHub

set -e

APP_DIR="/var/www/cv_webapp"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "CV Webapp Update Script"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

echo -e "${YELLOW}Step 1: Pulling latest code from GitHub...${NC}"
cd "$APP_DIR"
git fetch origin
git reset --hard origin/master
echo -e "${GREEN}✓ Code updated${NC}"

echo -e "${YELLOW}Step 2: Updating Python dependencies...${NC}"
source "$APP_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"
echo -e "${GREEN}✓ Dependencies updated${NC}"

echo -e "${YELLOW}Step 3: Setting permissions...${NC}"
chown -R www-data:www-data "$APP_DIR"
chmod -R 755 "$APP_DIR"
chmod 600 "$APP_DIR/.env" 2>/dev/null || true
echo -e "${GREEN}✓ Permissions set${NC}"

echo -e "${YELLOW}Step 4: Restarting application...${NC}"
systemctl restart cv-webapp
echo -e "${GREEN}✓ Application restarted${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}Update Complete!${NC}"
echo "=========================================="
echo ""
echo "Application status:"
systemctl status cv-webapp --no-pager -l
echo ""
echo "View logs: sudo journalctl -u cv-webapp -f"
echo "Visit: https://cv.go-live.app"
echo ""
