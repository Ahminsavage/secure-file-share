from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    enc_key = db.Column(db.LargeBinary, nullable=False)
    nonce = db.Column(db.LargeBinary, nullable=False)
    tag = db.Column(db.LargeBinary, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<File {self.filename}>"
