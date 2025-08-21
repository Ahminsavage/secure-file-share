import os
from dotenv import load_dotenv

load_dotenv()

# Flask secret key
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

# File Key Encryption Key (KEK)
FILE_KMS_KEK = bytes.fromhex(
    os.getenv("FILE_KMS_KEK", "3832cccdcbf3a252cb44a1e192bfdd0edc47558f9ea9d2c913cf5ef6e6455c77")
)

# Upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///files.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
