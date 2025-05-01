import sys
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import os

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_POST(self):
        """Gère les requêtes POST et log les paramètres."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_params = urllib.parse.parse_qs(post_data)

        print("\n🔹 Requête POST reçue")
        print(f"📌 Paramètres : {post_params}")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "success"}')

    def do_PUT(self):
        path = self.translate_path(self.path)
        if path.endswith('/'):
            self.send_response(405, "Method Not Allowed")
            self.wfile.write("PUT not allowed on a directory\n".encode())
            return
        else:
            print("\n🔹 Requête PUT reçue")
            print(f"📄 Write file : {path}")

            try:
                os.makedirs(os.path.dirname(path))
            except FileExistsError: pass
            length = int(self.headers['Content-Length'])
            with open(path, 'wb') as f:
                f.write(self.rfile.read(length))
            self.send_response(201, "Created")

def run():
    """Lance le serveur HTTP avec le port spécifié en argument."""
    if len(sys.argv) != 2:
        print("❌ Usage : python3 server.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        if not (1 <= port <= 65535):
            raise ValueError
    except ValueError:
        print("❌ Erreur : Le port doit être un nombre entre 1 et 65535.")
        sys.exit(1)

    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
    print(f"✅ Serveur démarré sur http://0.0.0.0:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur.")
        httpd.server_close()

if __name__ == "__main__":
    run()
