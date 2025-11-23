#!/bin/bash

# Environment Setup Script
# Run this script to create/update the .env file on your VPS

APP_DIR="/var/www/cv_webapp"

echo "=========================================="
echo "CV Webapp Environment Setup"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "This script will help you create the .env file with your API keys."
echo ""

# Prompt for API keys
read -p "Enter your OpenAI API Key: " OPENAI_KEY
read -p "Enter your Anthropic API Key: " ANTHROPIC_KEY

echo ""
echo "Optional: Default user profile (leave empty to set via web form)"
read -p "Your Name (optional): " USER_NAME
read -p "Your Phone (optional): " USER_PHONE
read -p "Your Email (optional): " USER_EMAIL
read -p "Your LinkedIn URL (optional): " LINKEDIN_URL

# Create .env file
cat > "$APP_DIR/.env" << EOF
# API Keys (Required)
OPENAI_API_KEY=$OPENAI_KEY
ANTHROPIC_API_KEY=$ANTHROPIC_KEY

# User Profile (Optional - can be set per-generation via web form)
USER_NAME=$USER_NAME
USER_PHONE=$USER_PHONE
USER_EMAIL=$USER_EMAIL
LINKEDIN_PROFILE=$LINKEDIN_URL
EOF

# Set permissions
chown www-data:www-data "$APP_DIR/.env"
chmod 600 "$APP_DIR/.env"

echo ""
echo "✓ Environment file created at: $APP_DIR/.env"
echo "✓ Permissions set (600, owned by www-data)"
echo ""
echo "Restarting application..."
systemctl restart cv-webapp

echo "✓ Application restarted"
echo ""
echo "Check status: systemctl status cv-webapp"
echo ""
