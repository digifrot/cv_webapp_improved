# VPS Deployment Guide

Complete guide to deploy the CV Webapp on your own VPS (Ubuntu/Debian).

## Prerequisites

- VPS running Ubuntu 20.04+ or Debian 11+
- Root or sudo access
- Domain name pointed to your VPS IP
- GitHub repository (public or private with SSH key)

---

## Quick Start (Automated Deployment)

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Add VPS deployment configuration"
git push origin master
```

### Step 2: Update Deployment Script

Edit `deployment/deploy.sh` and update:
```bash
REPO_URL="https://github.com/yourusername/cv_webapp_improved.git"
```

### Step 3: SSH into Your VPS

```bash
ssh root@your-server-ip
```

### Step 4: Run Automated Deployment

```bash
# Download and run the deployment script
curl -o deploy.sh https://raw.githubusercontent.com/yourusername/cv_webapp_improved/master/deployment/deploy.sh
chmod +x deploy.sh
sudo ./deploy.sh
```

The script will automatically:
- Install all system dependencies (Python, Nginx, Certbot)
- Clone your repository
- Set up virtual environment
- Install Python packages
- Configure systemd service
- Set up Nginx reverse proxy
- Configure firewall

### Step 5: Configure Environment Variables

```bash
sudo nano /var/www/cv_webapp/.env
```

Add your API keys:
```env
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional defaults
USER_NAME=
USER_PHONE=
USER_EMAIL=
LINKEDIN_PROFILE=
```

Or use the interactive setup script:
```bash
sudo /var/www/cv_webapp/deployment/setup-env.sh
```

### Step 6: Update Your Domain in Nginx

```bash
sudo nano /etc/nginx/sites-available/cv-webapp
```

Replace `yourdomain.com` with your actual domain:
```nginx
server_name yourdomain.com www.yourdomain.com;
```

Reload Nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Step 7: Get SSL Certificate (HTTPS)

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts. Certbot will automatically:
- Generate SSL certificate
- Update Nginx configuration
- Set up auto-renewal

---

## Manual Deployment (Step-by-Step)

If you prefer manual control or the automated script fails:

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx git ufw certbot python3-certbot-nginx
```

### 2. Create Application Directory

```bash
sudo mkdir -p /var/www/cv_webapp
cd /var/www/cv_webapp
```

### 3. Clone Repository

```bash
sudo git clone https://github.com/yourusername/cv_webapp_improved.git .
```

### 4. Set Up Python Virtual Environment

```bash
sudo python3 -m venv venv
source venv/bin/activate
sudo venv/bin/pip install -r requirements.txt
```

### 5. Create Data Directories

```bash
sudo mkdir -p data outputs static
```

### 6. Create .env File

```bash
sudo nano .env
```

Add:
```env
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
USER_NAME=
USER_PHONE=
USER_EMAIL=
LINKEDIN_PROFILE=
```

### 7. Set Permissions

```bash
sudo chown -R www-data:www-data /var/www/cv_webapp
sudo chmod -R 755 /var/www/cv_webapp
sudo chmod 600 /var/www/cv_webapp/.env
```

### 8. Set Up Systemd Service

```bash
sudo cp deployment/cv-webapp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cv-webapp
sudo systemctl start cv-webapp
```

Check status:
```bash
sudo systemctl status cv-webapp
```

### 9. Configure Nginx

```bash
sudo cp deployment/nginx-cv-webapp.conf /etc/nginx/sites-available/cv-webapp
sudo ln -s /etc/nginx/sites-available/cv-webapp /etc/nginx/sites-enabled/
```

Update domain name:
```bash
sudo nano /etc/nginx/sites-available/cv-webapp
```

Test and reload:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 10. Configure Firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 11. Get SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Post-Deployment

### Verify Application is Running

```bash
# Check service status
sudo systemctl status cv-webapp

# View application logs
sudo journalctl -u cv-webapp -f

# Check Nginx logs
sudo tail -f /var/log/nginx/cv_webapp_access.log
sudo tail -f /var/log/nginx/cv_webapp_error.log
```

### Test the Application

Visit: `https://yourdomain.com`

You should see the CV Generator form.

---

## Updating the Application

### Method 1: Automated Update Script

Create `deployment/update.sh`:
```bash
#!/bin/bash
cd /var/www/cv_webapp
sudo git pull origin master
source venv/bin/activate
sudo venv/bin/pip install -r requirements.txt
sudo systemctl restart cv-webapp
echo "✓ Application updated and restarted"
```

Run:
```bash
sudo /var/www/cv_webapp/deployment/update.sh
```

### Method 2: Manual Update

```bash
cd /var/www/cv_webapp
sudo git pull origin master
source venv/bin/activate
sudo venv/bin/pip install -r requirements.txt
sudo systemctl restart cv-webapp
```

---

## Troubleshooting

### Application Won't Start

```bash
# Check service status
sudo systemctl status cv-webapp

# View detailed logs
sudo journalctl -u cv-webapp -n 100

# Check if port is in use
sudo netstat -tlnp | grep 5000
```

### Nginx 502 Bad Gateway

```bash
# Check if Gunicorn is running
sudo systemctl status cv-webapp

# Check Nginx error logs
sudo tail -f /var/log/nginx/cv_webapp_error.log

# Restart both services
sudo systemctl restart cv-webapp
sudo systemctl restart nginx
```

### Permission Errors

```bash
# Reset permissions
sudo chown -R www-data:www-data /var/www/cv_webapp
sudo chmod -R 755 /var/www/cv_webapp
sudo chmod 600 /var/www/cv_webapp/.env
```

### SSL Certificate Issues

```bash
# Test certificate renewal
sudo certbot renew --dry-run

# Force renew
sudo certbot renew --force-renewal
```

---

## DNS Configuration

Point your domain to your VPS:

### A Records
```
Type: A
Name: @
Value: YOUR_VPS_IP
TTL: 3600
```

```
Type: A
Name: www
Value: YOUR_VPS_IP
TTL: 3600
```

Wait 5-30 minutes for DNS propagation.

Check DNS:
```bash
nslookup yourdomain.com
```

---

## Maintenance

### View Logs

```bash
# Application logs
sudo journalctl -u cv-webapp -f

# Nginx access logs
sudo tail -f /var/log/nginx/cv_webapp_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/cv_webapp_error.log
```

### Restart Services

```bash
# Restart application
sudo systemctl restart cv-webapp

# Restart Nginx
sudo systemctl restart nginx

# Restart both
sudo systemctl restart cv-webapp nginx
```

### Backup Data

```bash
# Backup data directory
sudo tar -czf cv_webapp_backup_$(date +%Y%m%d).tar.gz /var/www/cv_webapp/data

# Download to local machine
scp root@your-server-ip:/var/www/cv_webapp/cv_webapp_backup_*.tar.gz .
```

### Monitor Resources

```bash
# Check disk space
df -h

# Check memory
free -m

# Check CPU
top
```

---

## Security Recommendations

1. **Keep system updated:**
   ```bash
   sudo apt-get update && sudo apt-get upgrade
   ```

2. **Use SSH keys instead of passwords**

3. **Change SSH port from default 22**

4. **Install fail2ban:**
   ```bash
   sudo apt-get install fail2ban
   ```

5. **Regular backups of data directory**

6. **Monitor logs for suspicious activity**

7. **Keep API keys in .env file only (never commit)**

---

## Cost Estimate

VPS providers and typical costs:

- **DigitalOcean Droplet:** $6/month (1GB RAM)
- **Linode Nanode:** $5/month (1GB RAM)
- **Vultr:** $6/month (1GB RAM)
- **Hetzner:** €4.15/month (~$5)

Plus:
- Domain name: ~$10-15/year
- SSL Certificate: FREE (Let's Encrypt)

**Total: ~$5-10/month**

---

## Architecture

```
Internet
    ↓
Nginx (Port 80/443) - SSL Termination
    ↓
Gunicorn (Port 5000) - WSGI Server
    ↓
Flask App (Python)
    ↓
OpenAI/Anthropic APIs
```

---

## Support

If you encounter issues:

1. Check logs: `sudo journalctl -u cv-webapp -f`
2. Verify .env file exists and has correct permissions
3. Ensure API keys are valid
4. Check firewall allows ports 80 and 443
5. Verify DNS is pointing to correct IP

For more help, check:
- Nginx docs: https://nginx.org/en/docs/
- Gunicorn docs: https://docs.gunicorn.org/
- Certbot docs: https://certbot.eff.org/
