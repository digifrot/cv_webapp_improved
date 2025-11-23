# Quick Setup Guide for cv.go-live.app

Deploy your CV Webapp to Ubuntu VPS in under 10 minutes!

---

## Prerequisites

✅ Ubuntu VPS (20.04 or later)
✅ Root SSH access
✅ Domain: `cv.go-live.app` pointed to your VPS IP
✅ GitHub repository with your code

---

## Step 1: DNS Configuration

In your domain registrar (where you bought go-live.app), add this DNS record:

```
Type: A
Name: cv
Value: YOUR_VPS_IP_ADDRESS
TTL: 3600
```

**Example:**
- If your VPS IP is `203.0.113.45`
- Add A record: `cv` → `203.0.113.45`

Wait 5-15 minutes for DNS propagation.

**Verify DNS:**
```bash
nslookup cv.go-live.app
```

Should return your VPS IP.

---

## Step 2: Update Deployment Script

Before deploying, update your GitHub repository URL in `deployment/deploy.sh`:

```bash
REPO_URL="https://github.com/YOURUSERNAME/cv_webapp_improved.git"
```

Push to GitHub:
```bash
git add .
git commit -m "Configure deployment for cv.go-live.app"
git push origin master
```

---

## Step 3: SSH into Your VPS

```bash
ssh root@YOUR_VPS_IP
```

---

## Step 4: Run Automated Deployment

Copy and paste these commands:

```bash
# Download deployment script
wget https://raw.githubusercontent.com/YOURUSERNAME/cv_webapp_improved/master/deployment/deploy.sh

# Make executable
chmod +x deploy.sh

# Run deployment
sudo ./deploy.sh
```

The script will:
- ✅ Install Python 3, Nginx, Certbot
- ✅ Clone your repository
- ✅ Set up virtual environment
- ✅ Install all dependencies
- ✅ Configure systemd service
- ✅ Set up Nginx reverse proxy
- ✅ Configure firewall (UFW)

**Time: ~5 minutes**

---

## Step 5: Configure Environment Variables

Run the interactive setup script:

```bash
sudo bash /var/www/cv_webapp/deployment/setup-env.sh
```

You'll be prompted for:
- ✅ OpenAI API Key
- ✅ Anthropic API Key
- ✅ User profile info (optional)

The script will:
- Create `.env` file
- Set correct permissions
- Restart the application

---

## Step 6: Get SSL Certificate (HTTPS)

Run Certbot to get free SSL certificate from Let's Encrypt:

```bash
sudo certbot --nginx -d cv.go-live.app
```

**Follow the prompts:**
1. Enter your email
2. Agree to Terms of Service
3. Choose whether to share email with EFF (optional)

Certbot will:
- ✅ Generate SSL certificate
- ✅ Update Nginx config automatically
- ✅ Set up auto-renewal

**Time: ~2 minutes**

---

## Step 7: Verify Deployment

Check if everything is running:

```bash
# Check application status
sudo systemctl status cv-webapp

# Check Nginx status
sudo systemctl status nginx

# View application logs
sudo journalctl -u cv-webapp -n 50
```

**Visit your site:**
```
https://cv.go-live.app
```

You should see the CV Generator form! 🎉

---

## 🎯 Complete Command Summary

For copy-paste convenience:

```bash
# 1. SSH into VPS
ssh root@YOUR_VPS_IP

# 2. Download and run deployment
wget https://raw.githubusercontent.com/YOURUSERNAME/cv_webapp_improved/master/deployment/deploy.sh
chmod +x deploy.sh
sudo ./deploy.sh

# 3. Set up environment variables
sudo bash /var/www/cv_webapp/deployment/setup-env.sh

# 4. Get SSL certificate
sudo certbot --nginx -d cv.go-live.app

# 5. Check status
sudo systemctl status cv-webapp
```

---

## 🔧 Useful Commands

### View Real-time Logs
```bash
sudo journalctl -u cv-webapp -f
```

### Restart Application
```bash
sudo systemctl restart cv-webapp
```

### Restart Nginx
```bash
sudo systemctl restart nginx
```

### Check Nginx Configuration
```bash
sudo nginx -t
```

### View Nginx Logs
```bash
# Access logs
sudo tail -f /var/log/nginx/cv_webapp_access.log

# Error logs
sudo tail -f /var/log/nginx/cv_webapp_error.log
```

---

## 🔄 Updating Your App

After making code changes and pushing to GitHub:

```bash
# SSH into VPS
ssh root@YOUR_VPS_IP

# Run update script
sudo bash /var/www/cv_webapp/deployment/update.sh
```

That's it! Your changes are live.

---

## 🐛 Troubleshooting

### Application Not Starting

```bash
# Check logs
sudo journalctl -u cv-webapp -n 100

# Check if .env file exists
ls -la /var/www/cv_webapp/.env

# Verify environment variables are set
sudo cat /var/www/cv_webapp/.env
```

### 502 Bad Gateway Error

```bash
# Restart application
sudo systemctl restart cv-webapp

# Check if Gunicorn is running
sudo systemctl status cv-webapp

# Check Nginx error logs
sudo tail -f /var/log/nginx/cv_webapp_error.log
```

### SSL Certificate Not Working

```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew --force-renewal

# Test renewal process
sudo certbot renew --dry-run
```

### DNS Not Resolving

```bash
# Check DNS
nslookup cv.go-live.app

# Check if it returns your VPS IP
# If not, wait longer for DNS propagation (up to 24 hours)
```

### Permission Errors

```bash
# Reset all permissions
sudo chown -R www-data:www-data /var/www/cv_webapp
sudo chmod -R 755 /var/www/cv_webapp
sudo chmod 600 /var/www/cv_webapp/.env
```

---

## 📊 File Structure on VPS

```
/var/www/cv_webapp/
├── app.py                  # Main Flask application
├── generator/              # CV generation logic
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── data/                   # Base CV, examples
├── outputs/                # Generated CVs
├── venv/                   # Python virtual environment
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Python dependencies
└── deployment/
    ├── cv-webapp.service   # Systemd service file
    ├── nginx-cv-webapp.conf # Nginx configuration
    ├── deploy.sh           # Deployment script
    ├── setup-env.sh        # Environment setup
    └── update.sh           # Update script
```

---

## 🔐 Security Checklist

After deployment, ensure:

- ✅ Firewall enabled (ports 22, 80, 443 only)
- ✅ SSL certificate installed (HTTPS working)
- ✅ `.env` file has 600 permissions
- ✅ Application runs as www-data (not root)
- ✅ API keys stored in `.env` only (never in code)
- ✅ Regular system updates scheduled

---

## 📈 Monitoring

### Check Resource Usage

```bash
# Disk space
df -h

# Memory usage
free -m

# CPU usage
top

# Application logs size
du -sh /var/log/nginx/
```

### Monitor Application

```bash
# Service uptime
systemctl status cv-webapp

# Recent errors
sudo journalctl -u cv-webapp -p err -n 50

# Access count (daily)
sudo grep "$(date +'%d/%b/%Y')" /var/log/nginx/cv_webapp_access.log | wc -l
```

---

## 💾 Backup

Backup your data regularly:

```bash
# Backup data directory
sudo tar -czf ~/cv_backup_$(date +%Y%m%d).tar.gz /var/www/cv_webapp/data

# Download to local machine (from your computer)
scp root@YOUR_VPS_IP:~/cv_backup_*.tar.gz .
```

---

## 🆘 Support

If you encounter issues:

1. **Check logs first:** `sudo journalctl -u cv-webapp -f`
2. **Verify .env file** has correct API keys
3. **Check DNS** is pointing to correct IP
4. **Verify firewall** allows ports 80 and 443
5. **Test Nginx config:** `sudo nginx -t`

For detailed troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🎉 Success!

Your CV Generator should now be live at:

**https://cv.go-live.app**

Enjoy your automated CV tailoring service! 🚀
