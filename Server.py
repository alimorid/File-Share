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
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>File Share - Hacker Terminal</title>
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    
                    body {{
                        background: #0a0a0a;
                        color: #00ff00;
                        font-family: 'Courier New', monospace;
                        line-height: 1.6;
                        padding: 20px;
                        min-height: 100vh;
                        background-image: 
                            radial-gradient(circle at 25% 25%, rgba(0, 255, 0, 0.1) 0%, transparent 50%),
                            radial-gradient(circle at 75% 75%, rgba(0, 255, 0, 0.05) 0%, transparent 50%);
                    }}
                    
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        background: rgba(0, 0, 0, 0.8);
                        border: 2px solid #00ff00;
                        border-radius: 10px;
                        padding: 30px;
                        box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
                        backdrop-filter: blur(10px);
                    }}
                    
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                        border-bottom: 2px solid #00ff00;
                        padding-bottom: 20px;
                    }}
                    
                    .header h1 {{
                        font-size: 2.5em;
                        text-shadow: 0 0 10px #00ff00;
                        margin-bottom: 10px;
                        animation: glow 2s ease-in-out infinite alternate;
                    }}
                    
                    @keyframes glow {{
                        from {{ text-shadow: 0 0 10px #00ff00; }}
                        to {{ text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00; }}
                    }}
                    
                    .subtitle {{
                        color: #888;
                        font-size: 0.9em;
                        font-style: italic;
                    }}
                    
                    .upload-section {{
                        margin-bottom: 40px;
                        padding: 20px;
                        border: 1px solid #333;
                        border-radius: 5px;
                        background: rgba(0, 0, 0, 0.5);
                    }}
                    
                    .upload-section h2 {{
                        color: #00ff00;
                        margin-bottom: 20px;
                        font-size: 1.5em;
                        border-left: 4px solid #00ff00;
                        padding-left: 15px;
                    }}
                    
                    .file-input-wrapper {{
                        position: relative;
                        margin-bottom: 20px;
                    }}
                    
                    .file-input {{
                        width: 100%;
                        padding: 15px;
                        background: #111;
                        border: 2px dashed #00ff00;
                        border-radius: 5px;
                        color: #00ff00;
                        font-family: 'Courier New', monospace;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    }}
                    
                    .file-input:hover {{
                        border-color: #00cc00;
                        background: #1a1a1a;
                        box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
                    }}
                    
                    .file-input:focus {{
                        outline: none;
                        border-color: #00ff00;
                        box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
                    }}
                    
                    .upload-btn {{
                        background: linear-gradient(45deg, #00ff00, #00cc00);
                        color: #000;
                        border: 2px solid #00ff00;
                        padding: 15px 30px;
                        font-size: 1.1em;
                        font-weight: bold;
                        border-radius: 0;
                        cursor: pointer;
                        font-family: 'Courier New', monospace;
                        text-transform: uppercase;
                        letter-spacing: 2px;
                        transition: all 0.3s ease;
                        box-shadow: 
                            0 0 10px rgba(0, 255, 0, 0.5),
                            inset 0 0 10px rgba(0, 255, 0, 0.2);
                        position: relative;
                        overflow: hidden;
                        text-shadow: 0 0 5px #000;
                    }}
                    
                    .upload-btn::before {{
                        content: '';
                        position: absolute;
                        top: 0;
                        left: -100%;
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                        transition: left 0.5s;
                    }}
                    
                    .upload-btn:hover {{
                        transform: translateY(-3px) scale(1.02);
                        box-shadow: 
                            0 0 20px rgba(0, 255, 0, 0.8),
                            0 0 40px rgba(0, 255, 0, 0.4),
                            inset 0 0 15px rgba(0, 255, 0, 0.3);
                        background: linear-gradient(45deg, #00cc00, #00ff00, #00cc00);
                        border-color: #fff;
                        text-shadow: 0 0 10px #00ff00;
                    }}
                    
                    .upload-btn:hover::before {{
                        left: 100%;
                    }}
                    
                    .upload-btn:active {{
                        transform: translateY(-1px) scale(0.98);
                        box-shadow: 
                            0 0 15px rgba(0, 255, 0, 0.6),
                            inset 0 0 20px rgba(0, 255, 0, 0.4);
                    }}
                    
                    .upload-btn:focus {{
                        outline: none;
                        box-shadow: 
                            0 0 25px rgba(0, 255, 0, 0.9),
                            0 0 50px rgba(0, 255, 0, 0.5),
                            inset 0 0 20px rgba(0, 255, 0, 0.4);
                    }}
                    
                    .files-section {{
                        margin-top: 30px;
                    }}
                    
                    .files-section h3 {{
                        color: #00ff00;
                        margin-bottom: 20px;
                        font-size: 1.3em;
                        border-left: 4px solid #00ff00;
                        padding-left: 15px;
                    }}
                    
                    .files-list {{
                        list-style: none;
                        background: rgba(0, 0, 0, 0.5);
                        border-radius: 5px;
                        overflow: hidden;
                    }}
                    
                    .files-list li {{
                        border-bottom: 1px solid #333;
                        transition: all 0.3s ease;
                    }}
                    
                    .files-list li:last-child {{
                        border-bottom: none;
                    }}
                    
                    .files-list li:hover {{
                        background: rgba(0, 255, 0, 0.1);
                    }}
                    
                    .files-list a {{
                        display: block;
                        padding: 15px 20px;
                        color: #00ff00;
                        text-decoration: none;
                        font-size: 1em;
                        transition: all 0.3s ease;
                    }}
                    
                    .files-list a:hover {{
                        color: #fff;
                        text-shadow: 0 0 10px #00ff00;
                        padding-left: 25px;
                    }}
                    
                    .files-list a::before {{
                        content: "📁 ";
                        margin-right: 10px;
                    }}
                    
                    .status-bar {{
                        position: fixed;
                        bottom: 0;
                        left: 0;
                        right: 0;
                        background: #000;
                        border-top: 1px solid #00ff00;
                        padding: 10px 20px;
                        font-size: 0.8em;
                        color: #888;
                        text-align: center;
                    }}
                    
                    /* Responsive Design */
                    @media (max-width: 768px) {{
                        body {{
                            padding: 10px;
                        }}
                        
                        .container {{
                            padding: 20px;
                            margin: 10px;
                        }}
                        
                        .header h1 {{
                            font-size: 2em;
                        }}
                        
                        .upload-section {{
                            padding: 15px;
                        }}
                        
                        .file-input {{
                            padding: 12px;
                        }}
                        
                        .upload-btn {{
                            width: 100%;
                            padding: 15px;
                        }}
                        
                        .files-list a {{
                            padding: 12px 15px;
                            font-size: 0.9em;
                        }}
                    }}
                    
                    @media (max-width: 480px) {{
                        .header h1 {{
                            font-size: 1.5em;
                        }}
                        
                        .container {{
                            padding: 15px;
                        }}
                        
                        .upload-section {{
                            padding: 10px;
                        }}
                    }}
                    
                    /* Terminal-style cursor animation */
                    .cursor {{
                        animation: blink 1s infinite;
                    }}
                    
                    @keyframes blink {{
                        0%, 50% {{ opacity: 1; }}
                        51%, 100% {{ opacity: 0; }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>FILE SHARE TERMINAL<span class="cursor">_</span></h1>
                        <p class="subtitle">Secure File Transfer System v1.0</p>
                    </div>
                    
                    <div class="upload-section">
                        <h2>UPLOAD FILES</h2>
                        <form enctype="multipart/form-data" method="post">
                            <div class="file-input-wrapper">
                                <input name="file" type="file" multiple class="file-input" 
                                       accept="*/*" title="Select files to upload"/>
                            </div>
                            <button type="submit" class="upload-btn">UPLOAD FILES</button>
                        </form>
                    </div>
                    
                    <div class="files-section">
                        <h3>UPLOADED FILES</h3>
                        <ul class="files-list">
                            {files_list}
                        </ul>
                    </div>
                </div>
                
                <div class="status-bar">
                    <span>Status: Ready | Files: {len(files)} | Server: localhost:{PORT}</span>
                </div>
            </body>
            </html>
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
