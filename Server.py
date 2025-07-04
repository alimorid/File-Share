import os
from http.server import HTTPServer, BaseHTTPRequestHandler

UPLOAD_DIR = "uploads"
PORT = 8080
os.makedirs(UPLOAD_DIR, exist_ok=True)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # فرم آپلود چندفایلی + لیست فایل‌ها
            files = os.listdir(UPLOAD_DIR)
            files_list = "".join(f'<li><a href="/uploads/{f}">{f}</a></li>' for f in files)
            html = f"""
            <html><body>
            <h2>Upload Files</h2>
            <form enctype="multipart/form-data" method="post">
              <input name="file" type="file" multiple/>
              <input type="submit" value="Upload"/>
            </form>
            <h3>Uploaded Files:</h3>
            <ul>{files_list}</ul>
            </body></html>
            """
            self.wfile.write(html.encode())
        elif self.path.startswith("/uploads/"):
            filename = self.path[len("/uploads/"):]
            filepath = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header("Content-Disposition", f"attachment; filename={filename}")
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        boundary = self.headers['Content-Type'].split("boundary=")[1].encode()
        body = self.rfile.read(content_length)
        parts = body.split(b"--" + boundary)

        for part in parts:
            if b'Content-Disposition' in part and b'name="file"' in part:
                try:
                    head, file_data = part.split(b"\r\n\r\n", 1)
                    file_data = file_data.rstrip(b"\r\n--")

                    # پیدا کردن نام فایل
                    for line in head.split(b"\r\n"):
                        if b'filename="' in line:
                            filename = line.split(b'filename="')[1].split(b'"')[0].decode()
                            if filename:
                                filepath = os.path.join(UPLOAD_DIR, filename)
                                with open(filepath, "wb") as f:
                                    f.write(file_data)
                            break
                except Exception as e:
                    print(f"[!] Error handling file part: {e}")

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
    print(f"🚀 Server running on http://localhost:{PORT}")
    server.serve_forever()
