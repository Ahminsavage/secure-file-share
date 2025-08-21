import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from io import BytesIO
from config import SECRET_KEY, UPLOAD_FOLDER, MAX_CONTENT_LENGTH
from models import db, File
from crypto_utils import encrypt_file, decrypt_file

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = SECRET_KEY

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Init DB
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if not uploaded_file:
            flash("No file selected")
            return redirect(request.url)

        filename = secure_filename(uploaded_file.filename)
        file_data = uploaded_file.read()

        enc = encrypt_file(file_data)

        stored_filename = secure_filename(filename) + ".enc"
        stored_path = os.path.join(UPLOAD_FOLDER, stored_filename)
        with open(stored_path, "wb") as f:
            f.write(enc["ciphertext"])

        file_record = File(
            filename=filename,
            stored_filename=stored_filename,
            enc_key=enc["wrapped_key"],
            nonce=enc["nonce"],
            tag=enc["tag"]
        )
        db.session.add(file_record)
        db.session.commit()

        flash("File uploaded and encrypted successfully!")
        return redirect(url_for("files_list"))

    return render_template("index.html")

@app.route("/files")
def files_list():
    files = File.query.all()
    return render_template("files.html", files=files)

@app.route("/download/<int:file_id>")
def download_file(file_id):
    file_record = File.query.get_or_404(file_id)
    stored_path = os.path.join(UPLOAD_FOLDER, file_record.stored_filename)

    with open(stored_path, "rb") as f:
        ciphertext = f.read()

    plaintext = decrypt_file(ciphertext, file_record.nonce, file_record.tag, file_record.enc_key)

    return send_file(
        BytesIO(plaintext),
        as_attachment=True,
        download_name=file_record.filename
    )

if __name__ == "__main__":
    app.run(debug=True)
