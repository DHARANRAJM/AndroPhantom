# PhantomDroid Local Server Access Guide

```
 ██████╗██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
           M DHARAN RAJ - WEB DEVELOPER & ETHICAL HACKER
```

## 🏠 Local Server Access Guide

This guide shows you how to access and download generated payloads from your local PhantomDroid server.

## 🚀 Method 1: Web Interface Access

### **Start the Web Interface**
```bash
# Navigate to PhantomDroid directory
cd PhantomDroid

# Start the web interface
python3 core/web_interface.py

# Or use the main script
./phantomdroid.sh --web-interface

# Server will start on: http://localhost:8080
```

### **Access via Browser**
```bash
# Open your web browser and navigate to:
http://localhost:8080

# Or if running on a different port:
http://localhost:5000
http://127.0.0.1:8080
```

### **Web Interface Features**
- **Payload Generation**: Create payloads through web UI
- **File Browser**: Browse and download generated APKs
- **C2 Management**: Monitor active sessions
- **Log Viewer**: View framework logs
- **Download Manager**: Direct download links

## 📂 Method 2: Direct File Access

### **Local File System Access**
```bash
# Navigate to output directory
cd PhantomDroid/output

# List all generated payloads
ls -la

# Example output:
# phantom_tcp_reverse_20250810_110000.apk
# phantom_http_shell_20250810_110500.apk
# phantom_dns_tunnel_20250810_111000.apk

# Copy payload to desktop
cp phantom_tcp_reverse_*.apk ~/Desktop/

# Copy to Downloads folder
cp phantom_tcp_reverse_*.apk ~/Downloads/
```

### **Windows File Access**
```cmd
# Navigate to PhantomDroid directory
cd C:\PhantomDroid\output

# List files
dir *.apk

# Copy to Desktop
copy phantom_tcp_reverse_*.apk %USERPROFILE%\Desktop\

# Copy to Downloads
copy phantom_tcp_reverse_*.apk %USERPROFILE%\Downloads\
```

## 🌐 Method 3: HTTP File Server

### **Start Simple HTTP Server**
```bash
# Navigate to output directory
cd PhantomDroid/output

# Start Python HTTP server (Python 3)
python3 -m http.server 8000

# Or Python 2
python -m SimpleHTTPServer 8000

# Server accessible at: http://localhost:8000
```

### **Access Files via Browser**
```bash
# Open browser and go to:
http://localhost:8000

# You'll see a file listing with all APKs
# Click on any APK file to download it directly
```

### **Download via Command Line**
```bash
# From another terminal, download files using curl
curl -O http://localhost:8000/phantom_tcp_reverse_20250810_110000.apk

# Or using wget
wget http://localhost:8000/phantom_tcp_reverse_20250810_110000.apk

# Download to specific location
curl -o ~/Downloads/payload.apk http://localhost:8000/phantom_tcp_reverse_20250810_110000.apk
```

## 📱 Method 4: Mobile Device Access

### **Same Network Access**
```bash
# Find your local IP address
# Linux/Mac:
ip addr show | grep inet
ifconfig | grep inet

# Windows:
ipconfig

# Example IP: 192.168.1.100

# Start HTTP server on all interfaces
python3 -m http.server 8000 --bind 0.0.0.0

# Access from mobile device:
# http://192.168.1.100:8000
```

### **QR Code Generation**
```bash
# Install qrencode
sudo apt install qrencode  # Linux
brew install qrencode      # Mac

# Generate QR code for download link
echo "http://192.168.1.100:8000/phantom_tcp_reverse_20250810_110000.apk" | qrencode -t UTF8

# Generate QR code as image
qrencode -o payload_qr.png "http://192.168.1.100:8000/phantom_tcp_reverse_20250810_110000.apk"
```

## 🔧 Method 5: FTP Server Setup

### **Start FTP Server**
```bash
# Install vsftpd
sudo apt install vsftpd

# Configure FTP
sudo nano /etc/vsftpd.conf

# Add these lines:
anonymous_enable=YES
local_enable=YES
write_enable=YES
anon_upload_enable=YES
anon_mkdir_write_enable=YES
anon_root=/home/ftp

# Create FTP directory
sudo mkdir -p /home/ftp/payloads
sudo cp output/*.apk /home/ftp/payloads/
sudo chmod 755 /home/ftp/payloads

# Start FTP service
sudo systemctl start vsftpd
sudo systemctl enable vsftpd
```

### **Access FTP Server**
```bash
# Connect via FTP client
ftp localhost

# Or from another machine
ftp 192.168.1.100

# Download files
get phantom_tcp_reverse_20250810_110000.apk
```

## 📧 Method 6: Email/Cloud Upload

### **Upload to Cloud Storage**
```bash
# Upload to Google Drive (using gdrive tool)
gdrive upload output/phantom_tcp_reverse_*.apk

# Upload to Dropbox (using dropbox-cli)
dropbox upload output/phantom_tcp_reverse_*.apk

# Upload to AWS S3
aws s3 cp output/phantom_tcp_reverse_*.apk s3://your-bucket/
```

### **Email Attachment**
```bash
# Send via email using mutt
echo "Payload attached" | mutt -s "PhantomDroid Payload" -a output/phantom_tcp_reverse_*.apk -- your-email@example.com

# Or use mail command
mail -s "Payload" -A output/phantom_tcp_reverse_*.apk your-email@example.com < /dev/null
```

## 🔐 Method 7: Secure Transfer

### **SCP Transfer**
```bash
# Transfer to another machine via SCP
scp output/phantom_tcp_reverse_*.apk user@remote-host:/path/to/destination/

# Transfer from remote machine
scp user@remote-host:/path/to/payload.apk ./
```

### **SFTP Transfer**
```bash
# Connect via SFTP
sftp user@remote-host

# Upload file
put output/phantom_tcp_reverse_*.apk

# Download file
get remote_payload.apk
```

## 🖥️ Method 8: Network Share

### **SMB/CIFS Share (Linux)**
```bash
# Install Samba
sudo apt install samba

# Create share directory
sudo mkdir -p /srv/samba/payloads
sudo cp output/*.apk /srv/samba/payloads/

# Configure Samba
sudo nano /etc/samba/smb.conf

# Add share configuration:
[payloads]
path = /srv/samba/payloads
browseable = yes
read only = no
guest ok = yes

# Restart Samba
sudo systemctl restart smbd
```

### **Access Network Share**
```bash
# Windows:
\\192.168.1.100\payloads

# Linux:
smbclient //192.168.1.100/payloads

# Mac:
smb://192.168.1.100/payloads
```

## 📲 Method 9: ADB Transfer

### **Direct ADB Push**
```bash
# Connect Android device via USB
adb devices

# Push payload directly to device
adb push output/phantom_tcp_reverse_*.apk /sdcard/Download/

# Install directly
adb install output/phantom_tcp_reverse_*.apk

# Verify installation
adb shell pm list packages | grep phantom
```

### **ADB over WiFi**
```bash
# Enable ADB over WiFi (device must be rooted or developer options enabled)
adb tcpip 5555
adb connect 192.168.1.200:5555  # Device IP

# Transfer payload
adb push output/phantom_tcp_reverse_*.apk /sdcard/Download/
```

## 🔍 Method 10: Advanced Access Methods

### **WebDAV Server**
```bash
# Install Apache with WebDAV
sudo apt install apache2 apache2-utils

# Enable WebDAV modules
sudo a2enmod dav
sudo a2enmod dav_fs

# Configure WebDAV
sudo nano /etc/apache2/sites-available/webdav.conf

# Add configuration and restart Apache
sudo systemctl restart apache2

# Access via: http://localhost/webdav/
```

### **Nginx File Browser**
```bash
# Install Nginx
sudo apt install nginx

# Configure file browser
sudo nano /etc/nginx/sites-available/filebrowser

server {
    listen 8080;
    root /path/to/PhantomDroid/output;
    autoindex on;
    autoindex_exact_size off;
    autoindex_localtime on;
}

# Enable site
sudo ln -s /etc/nginx/sites-available/filebrowser /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# Access via: http://localhost:8080
```

## 🛠️ Troubleshooting Local Access

### **Common Issues and Solutions**

#### **Web Interface Not Starting**
```bash
# Check if port is already in use
netstat -tulnp | grep :8080
lsof -i :8080

# Kill process using the port
sudo kill -9 $(lsof -t -i:8080)

# Start on different port
python3 core/web_interface.py --port 8081
```

#### **Permission Denied**
```bash
# Fix file permissions
chmod 644 output/*.apk
chmod 755 output/

# Fix ownership
sudo chown $USER:$USER output/*.apk
```

#### **Network Access Issues**
```bash
# Check firewall
sudo ufw status
sudo ufw allow 8000/tcp

# Check IP binding
netstat -tulnp | grep :8000

# Bind to all interfaces
python3 -m http.server 8000 --bind 0.0.0.0
```

#### **File Not Found**
```bash
# Verify payload exists
ls -la output/
find . -name "*.apk" -type f

# Check generation logs
tail -f logs/phantomdroid.log
```

## 📊 Quick Access Commands

### **One-Line Commands**
```bash
# Start web server and open browser
python3 -m http.server 8000 --directory output & sleep 2 && xdg-open http://localhost:8000

# Copy latest payload to desktop
cp output/$(ls -t output/*.apk | head -1) ~/Desktop/

# Generate QR code for latest payload
echo "http://$(hostname -I | awk '{print $1}'):8000/$(ls -t output/*.apk | head -1 | xargs basename)" | qrencode -t UTF8

# Start PhantomDroid web interface
./phantomdroid.sh --web-interface --port 8080 --host 0.0.0.0
```

### **Batch Operations**
```bash
# Copy all payloads to USB drive
cp output/*.apk /media/usb/

# Upload all payloads to cloud
for file in output/*.apk; do gdrive upload "$file"; done

# Create archive of all payloads
tar -czf payloads_$(date +%Y%m%d).tar.gz output/*.apk
```

## 🎯 Best Practices

### **Security Considerations**
- Only run local servers on trusted networks
- Use authentication for web interfaces
- Regularly clean up old payloads
- Monitor access logs for suspicious activity

### **Performance Tips**
- Use lightweight HTTP servers for large files
- Compress payloads before transfer
- Use local network for faster transfers
- Cache frequently accessed files

### **Organization**
- Use descriptive filenames for payloads
- Maintain logs of generated payloads
- Create separate directories for different payload types
- Document payload configurations

---

**Created by: M DHARAN RAJ - Web Developer & Ethical Hacker**

**Remember**: Always ensure proper authorization before deploying any payloads, even in local environments.
