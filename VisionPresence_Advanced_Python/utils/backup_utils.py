import os
from shutil import copyfile
from datetime import datetime

# Folder paths
DB_PATH = "database/attendance.db"
BACKUP_FOLDER = "backups/"

# 🔹 Ensure backup folder exists
def ensure_backup_folder():
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

# 🔹 Create a timestamped backup of the database
def backup_database():
    ensure_backup_folder()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"attendance_backup_{now}.db"
    backup_path = os.path.join(BACKUP_FOLDER, backup_name)

    copyfile(DB_PATH, backup_path)
    print(f"[✅] Backup created: {backup_name}")
    return backup_name

# 🔹 List all backups with details (for storage.html table)
def list_backups():
    ensure_backup_folder()
    backups = []
    for f in sorted(os.listdir(BACKUP_FOLDER), reverse=True):
        path = os.path.join(BACKUP_FOLDER, f)
        backups.append({
            "name": f,
            "date": datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y-%m-%d %H:%M"),
            "size": round(os.path.getsize(path) / 1024, 2)  # KB
        })
    return backups

# 🔹 Delete a specific backup by filename
def delete_backup(filename):
    path = os.path.join(BACKUP_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        print(f"[🗑] Deleted backup: {filename}")
        return True
    return False

# 🔹 Get latest backup filename
def latest_backup():
    backups = list_backups()
    if backups:
        return backups[0]["name"]
    return None
