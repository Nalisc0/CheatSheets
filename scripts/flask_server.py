from flask import (
    Flask,
    request,
    jsonify,
    make_response,
    send_file,
    render_template_string,
)
import os
import sys

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/", methods=["POST"])
def handle_post():
    post_params = request.form.to_dict(flat=False)
    print("\n🔹 Requête POST reçue")
    print(f"📌 Paramètres : {post_params}")
    return jsonify(status="success")


@app.route("/<path:filename>", methods=["PUT"])
def handle_put(filename):
    path = os.path.abspath(filename)

    if path.endswith(os.path.sep):
        return make_response("PUT not allowed on a directory\n", 405)

    print("\n🔹 Requête PUT reçue")
    print(f"📄 Write file : {path}")

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(request.get_data())
    except Exception as e:
        return make_response(f"Erreur d'écriture : {str(e)}", 500)

    return make_response("Created", 201)


@app.route("/", defaults={"filepath": ""}, methods=["GET"])
@app.route("/<path:filepath>", methods=["GET"])
def handle_get(filepath):
    path = os.path.abspath(filepath or ".")

    if not os.path.exists(path):
        return make_response("Fichier ou dossier non trouvé", 404)

    if os.path.isdir(path):
        try:
            items = os.listdir(path)
            items.sort()
            links = []
            for item in items:
                full_path = os.path.join(filepath, item)
                if os.path.isdir(os.path.join(path, item)):
                    item_display = f"{item}/"
                else:
                    item_display = item
                links.append(f'<li><a href="/{full_path}">{item_display}</a></li>')

            html = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <title>Index of /{filepath}</title>
            </head>
            <body>
                <h1>Index of /{filepath}</h1>
                <ul>
                    {"".join(links)}
                </ul>
            </body>
            </html>
            """
            return render_template_string(html)
        except Exception as e:
            return make_response(
                f"Erreur lors de la lecture du dossier : {str(e)}", 500
            )
    elif os.path.isfile(path):
        try:
            return send_file(path, as_attachment=True)
        except Exception as e:
            return make_response(f"Erreur lors du téléchargement : {str(e)}", 500)

    return make_response("Type de fichier inconnu", 400)


if __name__ == "__main__":
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

    print(f"✅ Serveur Flask démarré sur http://0.0.0.0:{port}/")
    app.run(host="0.0.0.0", port=port)
