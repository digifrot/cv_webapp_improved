#!/bin/bash

# Quick fix script for systemd service issue
# Run this on your VPS to fix the service startup

set -e

APP_DIR="/var/www/cv_webapp"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=========================================="
echo "CV Webapp Service Fix Script"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Creating .env file if it doesn't exist...${NC}"
if [ ! -f "$APP_DIR/.env" ]; then
    cat > "$APP_DIR/.env" << 'EOF'
# Temporary placeholder - UPDATE THESE VALUES!
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
USER_NAME=
USER_PHONE=
USER_EMAIL=
LINKEDIN_PROFILE=
EOF
    chown www-data:www-data "$APP_DIR/.env"
    chmod 600 "$APP_DIR/.env"
    echo -e "${GREEN}✓ Created placeholder .env file${NC}"
    echo -e "${YELLOW}⚠ IMPORTANT: Update API keys in .env file!${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

echo -e "${YELLOW}Step 2: Updating systemd service file...${NC}"
# Pull latest service file from repo
cd "$APP_DIR"
git pull origin master

# Copy updated service file
cp "$APP_DIR/deployment/cv-webapp.service" /etc/systemd/system/cv-webapp.service

echo -e "${GREEN}✓ Service file updated${NC}"

echo -e "${YELLOW}Step 3: Reloading systemd and restarting service...${NC}"
systemctl daemon-reload
systemctl restart cv-webapp

echo -e "${GREEN}✓ Service restarted${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}Fix Applied!${NC}"
echo "=========================================="
echo ""

# Check service status
if systemctl is-active --quiet cv-webapp; then
    echo -e "${GREEN}✓ Service is running!${NC}"
    systemctl status cv-webapp --no-pager -l
else
    echo -e "${RED}✗ Service is not running${NC}"
    echo ""
    echo "Checking logs..."
    journalctl -u cv-webapp -n 30 --no-pager
    echo ""
    echo -e "${YELLOW}Troubleshooting tips:${NC}"
    echo "1. Check .env file: sudo cat $APP_DIR/.env"
    echo "2. Check permissions: ls -la $APP_DIR/.env"
    echo "3. View full logs: sudo journalctl -u cv-webapp -f"
    exit 1
fi

echo ""
echo "Next steps:"
echo "1. Update API keys: sudo nano $APP_DIR/.env"
echo "2. Restart service: sudo systemctl restart cv-webapp"
echo "3. View logs: sudo journalctl -u cv-webapp -f"
echo ""
