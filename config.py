import os

# ================= FOLDERS =================
# Folder to store uploaded staff images
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")

# Folder to store database backups
BACKUP_FOLDER = os.path.join(os.path.dirname(__file__), "backups")

# ================= DATABASE =================
# Path to the SQLite database file
DATABASE_FILE = os.path.join(os.path.dirname(__file__), "vision_attendance.db")

# ================= APP SETTINGS =================
# Maximum size for uploaded files (5 MB)
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Flask secret key for sessions / flash messages
SECRET_KEY = "visionpresence-secret"

# ================= OTHER CONFIGS =================
# Add any other global settings here
# Example:
# FACE_RECOGNITION_TOLERANCE = 0.6
