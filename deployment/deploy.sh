#!/bin/bash

# CV Webapp Deployment Script for VPS
# This script deploys the Flask application to your VPS

set -e  # Exit on any error

echo "=========================================="
echo "CV Webapp Deployment Script"
echo "=========================================="

# Configuration
APP_DIR="/var/www/cv_webapp"
REPO_URL="https://github.com/yourusername/cv_webapp_improved.git"  # UPDATE THIS
BRANCH="master"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

echo -e "${YELLOW}Step 1: Installing system dependencies...${NC}"
apt-get update
apt-get install -y python3 python3-pip python3-venv nginx git ufw certbot python3-certbot-nginx

echo -e "${GREEN}✓ System dependencies installed${NC}"

echo -e "${YELLOW}Step 2: Setting up application directory...${NC}"
# Create app directory if it doesn't exist
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "$APP_DIR"
    echo "Created $APP_DIR"
fi

# Clone or pull repository
if [ -d "$APP_DIR/.git" ]; then
    echo "Updating existing repository..."
    cd "$APP_DIR"
    git fetch origin
    git reset --hard origin/$BRANCH
else
    echo "Cloning repository..."
    git clone -b $BRANCH "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

echo -e "${GREEN}✓ Application code updated${NC}"

echo -e "${YELLOW}Step 3: Setting up Python virtual environment...${NC}"
if [ ! -d "$APP_DIR/venv" ]; then
    python3 -m venv "$APP_DIR/venv"
    echo "Created virtual environment"
fi

source "$APP_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"

echo -e "${GREEN}✓ Python dependencies installed${NC}"

echo -e "${YELLOW}Step 4: Creating data directories...${NC}"
mkdir -p "$APP_DIR/data"
mkdir -p "$APP_DIR/outputs"
mkdir -p "$APP_DIR/static"

echo -e "${GREEN}✓ Directories created${NC}"

echo -e "${YELLOW}Step 5: Setting permissions...${NC}"
chown -R www-data:www-data "$APP_DIR"
chmod -R 755 "$APP_DIR"

echo -e "${GREEN}✓ Permissions set${NC}"

echo -e "${YELLOW}Step 6: Setting up systemd service...${NC}"
cp "$APP_DIR/deployment/cv-webapp.service" /etc/systemd/system/cv-webapp.service
systemctl daemon-reload
systemctl enable cv-webapp
systemctl restart cv-webapp

echo -e "${GREEN}✓ Systemd service configured${NC}"

echo -e "${YELLOW}Step 7: Configuring Nginx...${NC}"
if [ ! -f /etc/nginx/sites-available/cv-webapp ]; then
    cp "$APP_DIR/deployment/nginx-cv-webapp.conf" /etc/nginx/sites-available/cv-webapp
    ln -s /etc/nginx/sites-available/cv-webapp /etc/nginx/sites-enabled/
    echo "Nginx configuration created"
else
    echo "Nginx configuration already exists"
fi

# Test Nginx configuration
nginx -t

# Restart Nginx
systemctl restart nginx

echo -e "${GREEN}✓ Nginx configured${NC}"

echo -e "${YELLOW}Step 8: Configuring firewall...${NC}"
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw --force enable

echo -e "${GREEN}✓ Firewall configured${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create .env file: nano $APP_DIR/.env"
echo "2. Add your API keys and configuration"
echo "3. Update domain in Nginx config: nano /etc/nginx/sites-available/cv-webapp"
echo "4. Get SSL certificate: certbot --nginx -d yourdomain.com -d www.yourdomain.com"
echo "5. Check application status: systemctl status cv-webapp"
echo "6. View logs: journalctl -u cv-webapp -f"
echo ""
echo "Application should be running on: http://YOUR_SERVER_IP"
echo ""
