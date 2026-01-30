# Deployment Guide: HTTPS Configuration

This guide provides instructions for deploying the Library Management System with HTTPS enabled.

## Prerequisites

1. A domain name (e.g., `example.com`)
2. A server with root access
3. Python 3.8+ installed
4. Nginx or Apache web server installed
5. SSL/TLS certificates (from Let's Encrypt or other CA)

## 1. Server Setup

### Install Required Packages

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3-pip python3-venv libpq-dev nginx certbot python3-certbot-nginx
```

## 2. Configure Web Server (Nginx)

### Nginx Configuration

Create a new Nginx configuration file at `/etc/nginx/sites-available/library_project`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Strong SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'none'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net code.jquery.com; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' fonts.gstatic.com cdn.jsdelivr.net; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none';";

    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        access_log off;
    }

    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
        access_log off;
    }

    # Proxy to Gunicorn
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Enable the site and test Nginx configuration:

```bash
sudo ln -s /etc/nginx/sites-available/library_project /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

## 3. Obtain SSL Certificate

Use Certbot to obtain an SSL certificate from Let's Encrypt:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Set up automatic renewal:

```bash
sudo certbot renew --dry-run  # Test renewal
sudo systemctl enable certbot.timer
```

## 4. Configure Gunicorn

Install Gunicorn:

```bash
pip install gunicorn
```

Create a Gunicorn systemd service file at `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=your_username
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock LibraryProject.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Start and enable Gunicorn:

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## 5. Environment Variables

Create a `.env` file in your project root with sensitive information:

```bash
# Database
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost,127.0.0.1

# Email (for production)
EMAIL_HOST=your-smtp-host
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com
SERVER_EMAIL=your-email@example.com
```

## 6. Update Django Settings

Ensure your `settings.py` includes:

```python
# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

## 7. Final Steps

1. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

2. Run database migrations:
   ```bash
   python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Restart services:
   ```bash
   sudo systemctl restart gunicorn
   sudo systemctl restart nginx
   ```

## 8. Monitoring and Maintenance

- Set up log rotation for Nginx and Gunicorn logs
- Configure backups for your database and media files
- Set up monitoring (e.g., Uptime Robot, Sentry for error tracking)
- Regularly update your system and Python packages

## 9. Security Hardening

- Configure a firewall (UFW):
  ```bash
  sudo ufw allow 'Nginx Full'
  sudo ufw allow 'OpenSSH'
  sudo ufw enable
  ```

- Disable SSH password authentication (use SSH keys only)
- Set up fail2ban to prevent brute force attacks
- Regularly review server logs for suspicious activity

## 10. Troubleshooting

- Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`
- Check Gunicorn logs: `sudo journalctl -u gunicorn`
- Test SSL configuration: [SSL Labs](https://www.ssllabs.com/ssltest/)
- Check security headers: [Security Headers](https://securityheaders.com/)

---
*Last updated: 2026-01-30*
