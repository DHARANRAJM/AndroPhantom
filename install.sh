#!/bin/bash

# PhantomDroid Framework v2.0 - Installation Script
# Advanced Android Penetration Testing Framework Installer

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Show banner
show_banner() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
 ██████╗██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
                    DROID Framework v2.0 - Installer
EOF
    echo -e "${NC}"
    echo -e "${CYAN}Advanced Android Penetration Testing Framework${NC}"
    echo -e "${WHITE}Created by: M DHARAN RAJ - Web Developer & Ethical Hacker${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════${NC}"
    echo
}

# Logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        "INFO") echo -e "${CYAN}[INFO]${NC} $message" ;;
        "WARN") echo -e "${YELLOW}[WARN]${NC} $message" ;;
        "ERROR") echo -e "${RED}[ERROR]${NC} $message" ;;
        "SUCCESS") echo -e "${GREEN}[SUCCESS]${NC} $message" ;;
    esac
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log "ERROR" "This script must be run as root (use sudo)"
        exit 1
    fi
}

# Detect OS
detect_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        log "ERROR" "Cannot detect operating system"
        exit 1
    fi
    
    log "INFO" "Detected OS: $OS $VER"
}

# Install system dependencies
install_system_deps() {
    log "INFO" "Installing system dependencies..."
    
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
        apt-get update
        apt-get install -y python3 python3-pip python3-venv openjdk-11-jdk wget curl unzip git
        apt-get install -y android-tools-adb android-tools-fastboot aapt zipalign
    elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
        yum update -y
        yum install -y python3 python3-pip java-11-openjdk-devel wget curl unzip git
    elif [[ "$OS" == *"Arch"* ]]; then
        pacman -Syu --noconfirm
        pacman -S --noconfirm python python-pip jdk11-openjdk wget curl unzip git
    else
        log "WARN" "Unsupported OS. Please install dependencies manually."
    fi
}

# Install Python dependencies
install_python_deps() {
    log "INFO" "Installing Python dependencies..."
    
    pip3 install --upgrade pip
    pip3 install flask cryptography sqlite3 requests
    pip3 install lxml beautifulsoup4 pillow
}

# Install Android SDK
install_android_sdk() {
    log "INFO" "Installing Android SDK..."
    
    SDK_DIR="/opt/android-sdk"
    
    if [[ ! -d "$SDK_DIR" ]]; then
        mkdir -p "$SDK_DIR"
        cd "$SDK_DIR"
        
        # Download Android SDK command line tools
        wget -q https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip
        unzip -q commandlinetools-linux-8512546_latest.zip
        rm commandlinetools-linux-8512546_latest.zip
        
        # Setup SDK
        mkdir -p cmdline-tools/latest
        mv cmdline-tools/* cmdline-tools/latest/ 2>/dev/null || true
        
        # Add to PATH
        echo 'export ANDROID_HOME=/opt/android-sdk' >> /etc/environment
        echo 'export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools' >> /etc/environment
        
        log "SUCCESS" "Android SDK installed"
    else
        log "INFO" "Android SDK already installed"
    fi
}

# Install apktool
install_apktool() {
    log "INFO" "Installing apktool..."
    
    APKTOOL_DIR="/opt/apktool"
    mkdir -p "$APKTOOL_DIR"
    cd "$APKTOOL_DIR"
    
    # Download latest apktool
    wget -q https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
    wget -q https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar
    
    chmod +x apktool
    mv apktool_2.7.0.jar apktool.jar
    
    # Create symlink
    ln -sf "$APKTOOL_DIR/apktool" /usr/local/bin/apktool
    
    log "SUCCESS" "apktool installed"
}

# Install Metasploit (optional)
install_metasploit() {
    log "INFO" "Installing Metasploit Framework..."
    
    if command -v msfconsole &> /dev/null; then
        log "INFO" "Metasploit already installed"
        return
    fi
    
    # Add Metasploit repository
    curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
    chmod 755 msfinstall
    ./msfinstall
    rm msfinstall
    
    log "SUCCESS" "Metasploit Framework installed"
}

# Setup PhantomDroid
setup_phantomdroid() {
    log "INFO" "Setting up PhantomDroid Framework..."
    
    PHANTOM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Create directories
    mkdir -p "$PHANTOM_DIR"/{output,logs,config,templates}
    mkdir -p "$PHANTOM_DIR"/output/{payloads,signed,temp}
    
    # Set permissions
    chmod +x "$PHANTOM_DIR/phantomdroid.sh"
    chmod +x "$PHANTOM_DIR/core"/*.py
    
    # Create configuration files
    cat > "$PHANTOM_DIR/config/core.conf" << EOF
# PhantomDroid Core Configuration
[general]
debug = false
verbose = false
auto_cleanup = true

[paths]
output_dir = output
log_dir = logs
temp_dir = output/temp

[evasion]
default_level = medium
enable_encryption = true
enable_obfuscation = true
EOF

    cat > "$PHANTOM_DIR/config/payloads.conf" << EOF
# Payload Configuration
[tcp_reverse]
default_port = 4444
timeout = 30
retry_count = 3

[http_shell]
default_port = 8080
user_agent = Mozilla/5.0 (Android)
timeout = 60

[dns_tunnel]
domain = phantom.local
query_interval = 3

[sms_shell]
command_prefix = CMD:
response_limit = 160
EOF

    # Create desktop shortcut
    cat > /usr/share/applications/phantomdroid.desktop << EOF
[Desktop Entry]
Name=PhantomDroid Framework
Comment=Advanced Android Penetration Testing
Exec=gnome-terminal -- bash -c 'cd $PHANTOM_DIR && ./phantomdroid.sh; bash'
Icon=$PHANTOM_DIR/icon.png
Terminal=true
Type=Application
Categories=Development;Security;
EOF

    # Create symlink for global access
    ln -sf "$PHANTOM_DIR/phantomdroid.sh" /usr/local/bin/phantomdroid
    
    log "SUCCESS" "PhantomDroid Framework setup completed"
}

# Verify installation
verify_installation() {
    log "INFO" "Verifying installation..."
    
    local deps=("python3" "java" "aapt" "zipalign" "apktool")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_deps+=("$dep")
        fi
    done
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log "ERROR" "Missing dependencies: ${missing_deps[*]}"
        return 1
    fi
    
    # Test Python modules
    python3 -c "import flask, cryptography" 2>/dev/null
    if [[ $? -ne 0 ]]; then
        log "ERROR" "Python dependencies not properly installed"
        return 1
    fi
    
    log "SUCCESS" "All dependencies verified"
    return 0
}

# Main installation function
main() {
    show_banner
    
    log "INFO" "Starting PhantomDroid Framework installation..."
    
    # Check prerequisites
    check_root
    detect_os
    
    # Install components
    install_system_deps
    install_python_deps
    install_android_sdk
    install_apktool
    
    # Optional components
    read -p "Install Metasploit Framework? [y/N]: " install_msf
    if [[ "$install_msf" =~ ^[Yy]$ ]]; then
        install_metasploit
    fi
    
    # Setup PhantomDroid
    setup_phantomdroid
    
    # Verify installation
    if verify_installation; then
        echo
        log "SUCCESS" "PhantomDroid Framework installed successfully!"
        echo
        echo -e "${GREEN}Usage:${NC}"
        echo -e "  ${CYAN}./phantomdroid.sh${NC}          - Start interactive mode"
        echo -e "  ${CYAN}phantomdroid --help${NC}        - Show help"
        echo
        echo -e "${YELLOW}Important:${NC}"
        echo -e "  - Use only for authorized penetration testing"
        echo -e "  - Check local laws and regulations"
        echo -e "  - Obtain proper permissions before testing"
        echo
    else
        log "ERROR" "Installation verification failed"
        exit 1
    fi
}

# Run main function
main "$@"
