import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

PORT = 8080
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileUploadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body>
                    <h2>Upload File</h2>
                    <form enctype="multipart/form-data" method="post">
                        <input name="file" type="file"/>
                        <input type="submit" value="Upload"/>
                    </form>
                    <h3>Uploaded Files:</h3>
                    <ul>
            """ + 
            "".join([
                f"<li><a href='/uploads/{f}'>{f}</a></li>" 
                for f in os.listdir(UPLOAD_DIR)
            ]).encode() + 
            b"""
                    </ul>
                </body>
                </html>
            """)
        elif self.path.startswith("/uploads/"):
            file_name = self.path[len("/uploads/"):]
            file_path = os.path.join(UPLOAD_DIR, file_name)
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header('Content-Disposition', f'attachment; filename="{file_name}"')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")

    def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers.get('content-type'))
        if content_type == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = int(self.headers['content-length'])
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'},
                keep_blank_values=True
            )
            if 'file' in form:
                file_item = form['file']
                filename = os.path.basename(file_item.filename)
                with open(os.path.join(UPLOAD_DIR, filename), 'wb') as f:
                    f.write(file_item.file.read())
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"<h3>File '{filename}' uploaded successfully!</h3><a href='/'>Back</a>".encode())
            else:
                self.send_error(400, "No file uploaded")
        else:
            self.send_error(400, "Content-Type not supported")

if __name__ == "__main__":
    server = HTTPServer(('', PORT), FileUploadHandler)
    print(f"🚀 Server running on http://localhost:{PORT}")
    server.serve_forever()
