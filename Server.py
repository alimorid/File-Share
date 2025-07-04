import http.server
import socketserver
import os
from urllib.parse import unquote
import json

UPLOAD_DIR = "uploads"
PORT = 8000

os.makedirs(UPLOAD_DIR, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/files":
            files = os.listdir(UPLOAD_DIR)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/upload":
            content_length = int(self.headers['Content-Length'])
            boundary = self.headers['Content-Type'].split("=")[1].encode()
            body = self.rfile.read(content_length)
            file_data = body.split(boundary)[2]
            headers, file_content = file_data.split(b"\r\n\r\n", 1)
            file_content = file_content.rsplit(b"\r\n", 1)[0]
            filename_line = headers.decode(errors="ignore").split("\r\n")[1]
            filename = filename_line.split("filename=")[1].strip('"')
            with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
                f.write(file_content)
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

Handler.extensions_map.update({
    '.html': 'text/html',
})

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()
