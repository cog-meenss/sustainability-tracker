#!/usr/bin/env python3
"""
Simple HTTP server for Carbon Dashboard
"""
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def serve_dashboard(port=8080):
    """Serve the carbon dashboard on localhost"""
    
    # Change to dashboard directory
    dashboard_dir = Path(__file__).parent
    os.chdir(dashboard_dir)
    
    # Create server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🌱 Carbon Dashboard Server")
            print(f"📊 Serving at: http://localhost:{port}")
            print(f"🌐 Dashboard URL: http://localhost:{port}/index.html")
            print(f"📁 Directory: {dashboard_dir}")
            print(f"\nPress Ctrl+C to stop the server")
            
            # Try to open in default browser
            try:
                webbrowser.open(f'http://localhost:{port}/index.html')
                print(f"🚀 Opening dashboard in default browser...")
            except:
                print(f"💡 Manually open: http://localhost:{port}/index.html")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print(f"💡 Try a different port: python3 serve_dashboard.py --port 8081")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    import sys
    
    port = 8080
    if len(sys.argv) > 1 and sys.argv[1] == "--port" and len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port number, using default 8080")
    
    serve_dashboard(port)