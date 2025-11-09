#!/usr/bin/env python3
"""
Simple web server for runtime sustainability reports
Serves fresh reports on-demand without static files
"""

import os
import json
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import urllib.parse
from datetime import datetime

class RuntimeReportHandler(SimpleHTTPRequestHandler):
    """HTTP handler for runtime sustainability reports"""
    
    def __init__(self, *args, **kwargs):
        self.project_path = Path('.').absolute()
        self.reporter_path = self.project_path / "runtime_sustainability_reporter.py"
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests for reports"""
        path = urllib.parse.urlparse(self.path).path
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        if path == '/':
            self._serve_dashboard()
        elif path == '/api/report':
            format_type = query.get('format', ['html'])[0]
            self._serve_runtime_report(format_type)
        elif path == '/api/status':
            self._serve_status()
        elif path == '/refresh':
            self._serve_dashboard(force_refresh=True)
        else:
            self.send_error(404, "Not Found")
    
    def _serve_dashboard(self, force_refresh=False):
        """Serve the main dashboard page"""
        try:
            # Generate fresh HTML report
            result = subprocess.run([
                sys.executable, 
                str(self.reporter_path),
                '--path', str(self.project_path),
                '--format', 'html'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                html_content = result.stdout
                
                # Add refresh functionality
                html_content = html_content.replace(
                    '</head>',
                    '''
                    <script>
                        // Auto-refresh every 5 minutes
                        setTimeout(() => {
                            window.location.reload();
                        }, 300000);
                        
                        // Manual refresh button
                        function refreshReport() {
                            window.location.reload();
                        }
                        
                        // Add refresh button
                        window.onload = function() {
                            const container = document.querySelector('.container');
                            if (container) {
                                const refreshBtn = document.createElement('div');
                                refreshBtn.style = 'text-align: center; margin: 20px; position: sticky; top: 20px; z-index: 1000;';
                                refreshBtn.innerHTML = `
                                    <button onclick="refreshReport()" style="
                                        background: linear-gradient(135deg, #4CAF50, #45a049);
                                        color: white; border: none; padding: 12px 24px;
                                        border-radius: 25px; cursor: pointer; font-size: 16px;
                                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                                        transition: transform 0.2s;
                                    " onmouseover="this.style.transform='scale(1.05)'" 
                                       onmouseout="this.style.transform='scale(1)'">
                                        🔄 Refresh Report
                                    </button>
                                    <span style="margin-left: 15px; color: #666; font-size: 14px;">
                                        Last updated: ''' + datetime.now().strftime('%H:%M:%S') + '''
                                    </span>
                                `;
                                container.insertBefore(refreshBtn, container.firstChild);
                            }
                        };
                    </script>
                    </head>'''
                )
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.end_headers()
                self.wfile.write(html_content.encode())
            else:
                self._serve_error("Failed to generate runtime report", result.stderr)
                
        except subprocess.TimeoutExpired:
            self._serve_error("Report generation timeout", "Analysis taking too long")
        except Exception as e:
            self._serve_error("Runtime report error", str(e))
    
    def _serve_runtime_report(self, format_type):
        """Generate and serve report in specified format"""
        try:
            result = subprocess.run([
                sys.executable,
                str(self.reporter_path),
                '--path', str(self.project_path),
                '--format', format_type
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                if format_type == 'json':
                    content_type = 'application/json'
                    content = result.stdout
                elif format_type == 'html':
                    content_type = 'text/html'
                    content = result.stdout
                elif format_type == 'markdown':
                    content_type = 'text/plain'
                    content = result.stdout
                else:
                    content_type = 'text/plain'
                    content = result.stdout
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(content.encode())
            else:
                self._serve_json_error("Report generation failed", result.stderr)
                
        except Exception as e:
            self._serve_json_error("Runtime analysis error", str(e))
    
    def _serve_status(self):
        """Serve server status and capabilities"""
        status = {
            "server": "Runtime Sustainability Reporter",
            "version": "1.0.0",
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "project_path": str(self.project_path),
            "capabilities": {
                "formats": ["html", "json", "markdown", "console"],
                "endpoints": ["/", "/api/report", "/api/status", "/refresh"],
                "auto_refresh": True,
                "real_time": True
            },
            "last_analysis": "On demand"
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(status, indent=2).encode())
    
    def _serve_error(self, title, message):
        """Serve error page"""
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Runtime Report Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; background: #f5f5f5; }}
                .error {{ background: #fff; padding: 30px; border-radius: 10px; 
                         border-left: 5px solid #e74c3c; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #e74c3c; margin-top: 0; }}
                .retry {{ margin-top: 20px; }}
                button {{ background: #3498db; color: white; border: none; padding: 10px 20px; 
                         border-radius: 5px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>⚠️ {title}</h1>
                <p><strong>Error Details:</strong></p>
                <pre>{message}</pre>
                <div class="retry">
                    <button onclick="window.location.reload()">🔄 Retry</button>
                    <button onclick="window.location.href='/'">🏠 Home</button>
                </div>
            </div>
        </body>
        </html>
        """
        
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(error_html.encode())
    
    def _serve_json_error(self, title, message):
        """Serve JSON error response"""
        error_data = {
            "error": True,
            "title": title,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_response(500)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(error_data, indent=2).encode())
    
    def log_message(self, format, *args):
        """Custom logging for cleaner output"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def main():
    """Start the runtime sustainability report server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Runtime Sustainability Report Server')
    parser.add_argument('--port', type=int, default=8000, help='Server port')
    parser.add_argument('--host', default='localhost', help='Server host')
    
    args = parser.parse_args()
    
    try:
        server = HTTPServer((args.host, args.port), RuntimeReportHandler)
        
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║              🔄 Runtime Sustainability Report Server           ║
╚════════════════════════════════════════════════════════════════╝

🌐 Server URL:     http://{args.host}:{args.port}/
📊 API Endpoint:   http://{args.host}:{args.port}/api/report?format=json
🔄 Refresh URL:    http://{args.host}:{args.port}/refresh
📡 Status API:     http://{args.host}:{args.port}/api/status

📋 Available Formats:
   • HTML:      /api/report?format=html
   • JSON:      /api/report?format=json  
   • Markdown:  /api/report?format=markdown
   • Console:   /api/report?format=console

✨ Features:
   • Real-time report generation
   • Auto-refresh every 5 minutes
   • No static files - all runtime
   • Fresh analysis on every request

Press Ctrl+C to stop the server...
        """)
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()