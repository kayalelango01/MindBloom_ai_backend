"""
Quick HTTP Server for Testing
This serves the test HTML files so they can access the Django API
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow API calls
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-CSRFToken')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        super().end_headers()

def run_server():
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🌐 Test server running at http://localhost:{PORT}")
        print(f"📁 Serving files from: {DIRECTORY}")
        print(f"\n📄 Available test pages:")
        print(f"   • http://localhost:{PORT}/simple-test.html")
        print(f"   • http://localhost:{PORT}/test-api.html")
        print(f"\n✨ Press Ctrl+C to stop the server")
        
        # Auto-open the simple test page
        webbrowser.open(f'http://localhost:{PORT}/simple-test.html')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped.")

if __name__ == "__main__":
    run_server()
