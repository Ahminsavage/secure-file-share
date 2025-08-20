# secure-file-share
Secure File Share: A minimal Flask web app for encrypted file storage using AES‑GCM. Allows uploading and downloading files securely with encryption at rest.

# 🔐 Secure File Share (Flask + AES-GCM)

A minimal, **secure-by-default** file sharing portal.  
- Files are encrypted **at rest** with AES-GCM (via PyCryptodome).  
- Decryption occurs **only on download**, with integrity validated using the GCM tag.  
- Run behind **HTTPS** to protect data **in transit**.  

> ⚠️ For internship/learning purposes — not production-hardened.

Project: Secure File Sharing System
Tools Used: Python Flask, PyCryptodome (AES), HTML/CSS/JS, Postman, curl, 
Prepared by: RAWLINGS ODIERO
Date: August 2025
Task: FutureInterns – Task 3


---

## ✨ Features
- 📤 Upload files up to a configurable size (default: **50 MB**).  
- 🔑 AES-256-GCM with scrypt KDF; random salt & nonce per file.  
- 🚀 Streaming encryption/decryption (constant memory use).  
- 🗂️ File index with original names + timestamps.  
- 🛡️ Secure headers (CSP, X-CTO, XFO, Referrer-Policy).  
- 🎨 Minimal dark-themed UI.  

---

## ⚡ Quickstart

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set a strong SFS_PASSPHRASE (>=16 chars)

# Run the server
python -m flask run
# → http://127.0.0.1:5000

⚙️ Configuration (.env)
SFS_PASSPHRASE (required) – long random passphrase; used to derive per-file AES keys with scrypt.

FLASK_SECRET_KEY – cookie signing secret (auto-random if omitted).

MAX_UPLOAD_MB – maximum upload size (MB).

ALLOWED_EXTS – comma-separated whitelist (e.g., pdf,jpg,txt).

STORAGE_DIR – directory for encrypted files + index.json.

📦 File Format
Each encrypted file is structured as:

MAGIC(4) | SALT(16) | NONCE(12) | CIPHERTEXT(...) | TAG(16)
scrypt(passphrase, salt) → 32-byte AES-256-GCM key

Integrity/authenticity enforced by the GCM tag (download fails if tampered)

🌐 API Examples (curl)
Upload:
curl -F "file=@/path/to/document.pdf" http://127.0.0.1:5000/upload

Download (using id from UI table or storage/index.json):
curl -OJ http://127.0.0.1:5000/download/<id>

🔒 Security Notes
Always deploy Flask behind TLS (Caddy, NGINX, Apache, or a cloud LB).

The passphrase is never stored — losing it = permanent data loss.

Adjust scrypt N/r/p for higher brute-force cost (CPU/RAM trade-off).

GCM ensures tamper detection; invalid files trigger 409.

Configure ALLOWED_EXTS to reduce risky file uploads.

For production: add authentication, CSRF protection, audit logs, and rate limiting.

🎯 Threat Model (Summary)
Data at rest – AES-GCM encryption; attacker needs passphrase.

MITM – Use HTTPS; without it, traffic is plaintext.

Key compromise – Rotate passphrase; re-encrypt stored files.

DoS / oversized files – Enforced MAX_CONTENT_LENGTH; configure nginx upload limits.

Path traversal – Prevented (UUID-based storage, no user path control).

🔄 Key Rotation (Outline)
Set SFS_PASSPHRASE_NEW alongside SFS_PASSPHRASE.

For each file: decrypt (old) → re-encrypt (new) → write as *.rot.

Swap in rotated files after verification.

Remove old passphrase securely.

📄 License
MIT License – see LICENSE for details.
