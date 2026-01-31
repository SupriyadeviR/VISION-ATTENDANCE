# VisionPresence Advanced - AI-Powered Attendance System 🚀

A modern, intelligent biometric face recognition attendance management system built with Flask and advanced analytics capabilities.

## Features ✨

### Core Functionality
- **🔐 Secure Biometric Authentication**: Face recognition-based attendance marking
- **📸 Real-time Face Recognition**: AI-powered employee identification
- **⏰ Automatic Time-In/Time-Out**: Smart dual-scan attendance tracking with automatic state detection
- **📊 Comprehensive Analytics**: Detailed attendance reports with duration calculations
- **💾 Database Backup & Restore**: Automated backup management with version control
- **📤 Data Export**: CSV and JSON export formats for attendance records

### Advanced Features
- **Modern Dark Theme Interface**: Professional dark-mode UI with responsive design
- **Employee Management**: Full CRUD operations with extended staff profiles (DOB, native place, department)
- **Attendance Dashboard**: Real-time statistics and system health monitoring
- **Search & Filtering**: Advanced search with multiple filter options
- **Duration Tracking**: Automatic calculation of work duration (time_out - time_in)
- **Weekly Analytics**: Attendance percentage calculations with trends

## Project Structure 📁

```
VisionPresence_Advanced_Python/
├── app.py                          # Main Flask application with all routes
├── config.py                       # Configuration settings (paths, DB location)
├── create_db.py                    # Database initialization script
├── requirements.txt                # Python dependencies
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                  # Master template with dark theme & sidebar nav
│   ├── dashboard.html             # Landing page with stats & quick actions
│   ├── overview.html              # System overview with analytics
│   ├── register_staff.html        # Staff registration form with image upload
│   ├── staff_list.html            # Staff directory with avatar display
│   ├── biometric_scan.html        # Live camera interface for attendance marking
│   ├── attendance_logs.html       # Attendance records with search/export
│   └── storage.html               # Backup management & export options
│
├── utils/                          # Utility modules
│   ├── db_utils.py               # Database connection management (Flask g pattern)
│   ├── face_utils.py             # Face recognition encoding/recognition logic
│   ├── backup_utils.py           # Database backup/restore functions
│   └── __init__.py
│
├── face_data/                      # Face encodings storage
│   └── encodings.pkl             # Pickled face encodings for recognition
│
├── uploads/                        # User-uploaded staff photos
├── backups/                        # Database backup files (timestamped)
└── static/                         # CSS, JS, images (legacy, now in templates)
```

## Technology Stack 🛠️

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask (Python 3.8+) |
| **Database** | SQLite3 with connection pooling |
| **Face Recognition** | face_recognition library (HOG/CNN models) |
| **Frontend** | Jinja2 templates with modern CSS |
| **Theme** | Dark mode with CSS variables |
| **File Handling** | Werkzeug secure_filename |

## Database Schema 🗄️

### Staff Table
```sql
CREATE TABLE staff (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    department TEXT,
    gender TEXT,
    joining_date DATE,
    dob DATE,
    native TEXT,
    image_path TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Attendance Table
```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id INTEGER NOT NULL,
    attendance_date DATE NOT NULL,
    time_in TIME,
    time_out TIME,
    status TEXT DEFAULT 'Present',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(emp_id, attendance_date),
    FOREIGN KEY(emp_id) REFERENCES staff(emp_id)
)
```

**Key Design Decision**: UNIQUE(emp_id, attendance_date) ensures one attendance record per employee per day, simplifying time-out logic (UPDATE vs INSERT).

## Installation & Setup 🚀

### 1. Clone/Extract Project
```bash
cd VisionPresence_Advanced_Python
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python create_db.py
```

### 5. Run Application
```bash
python app.py
```

Visit: http://localhost:5000/overview

## API Endpoints 🔌

### Dashboard & Navigation
- `GET /` - Redirect to overview
- `GET /dashboard` - Landing page with system status
- `GET /overview` - Main dashboard with analytics

### Staff Management
- `GET /staff` - View all registered staff
- `POST /register` - Register new staff member with photo
- `GET /delete_staff/<emp_id>` - Delete staff record
- `GET /uploaded_file/<filename>` - Serve uploaded staff photos

### Attendance Tracking
- `GET /scan` - Live biometric scan interface
- `POST /mark_attendance` - Process face recognition and mark attendance
- `GET /attendance` - View attendance logs with filters

### Data Management
- `GET /storage` - Storage management dashboard
- `GET /export_attendance` - Export attendance (CSV/JSON)
- `GET /backup_db` - Create database backup
- `GET /download/<filename>` - Download backup file
- `GET /delete_backup/<filename>` - Delete backup file

## Key Code Features 🔑

### 1. Database Connection Management (Fixes "Closed Database" Error)
```python
# Flask g object for per-request connection lifecycle
def get_db():
    db = g.get('db')
    if db is None:
        db = sqlite3.connect(DATABASE_FILE)
        db.row_factory = sqlite3.Row
        g.db = db
    return db

# Automatic cleanup on request end
app.teardown_appcontext(close_db)
```

### 2. Smart Time In/Time Out Logic
```python
# Check for existing attendance record (UNIQUE constraint)
existing = conn.execute(
    "SELECT * FROM attendance WHERE emp_id=? AND attendance_date=?",
    (emp_id, today)
).fetchone()

if existing:
    if existing["time_out"]:
        # Already checked out
        return {"status": "failed", "message": "Already checked out"}
    else:
        # Mark time_out
        conn.execute("UPDATE attendance SET time_out=?, status=? WHERE id=?",
                    (now, "Present", existing["id"]))
else:
    # First scan of the day - mark time_in
    conn.execute("INSERT INTO attendance (...) VALUES (...)", 
                (emp_id, today, now, "Present"))
```

### 3. Attendance Analytics with JOINs
```python
# Calculate duration for each attendance record
rows = conn.execute("""
    SELECT a.id, a.emp_id, s.name, a.attendance_date,
           a.time_in, a.time_out, a.status
    FROM attendance a
    JOIN staff s ON a.emp_id = s.emp_id
    ORDER BY a.attendance_date DESC
""").fetchall()

# Calculate duration in hours
for row in rows:
    if row['time_out'] and row['time_in']:
        duration = (row['time_out'] - row['time_in']).total_seconds() / 3600
```

### 4. CSV/JSON Export
```python
# Export with multiple formats
if format == 'json':
    return jsonify([dict(row) for row in rows])
else:  # CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['EMP ID', 'Name', 'Date', 'Time In', 'Time Out', 'Status'])
    for row in rows:
        writer.writerow([...])
    return send_file(...)
```

## Frontend Features 🎨

### Base Template
- **Sidebar Navigation**: Access all major sections via emoji-labeled navigation
- **Dark Theme**: CSS variables for consistent styling (--bg-dark, --accent, --success, --danger)
- **Responsive Layout**: Mobile-friendly grid system with media queries
- **Top Bar**: System title and user context

### Biometric Scan Interface
- **Live Video Feed**: Real-time camera capture via HTML5 canvas
- **JavaScript Camera Control**: Auto-play, capture, and processing
- **Today's Attendance Summary**: Quick view of current day's records
- **Recognition Feedback**: Visual success/error messages with status colors

### Attendance Logs
- **Advanced Filtering**: Search by employee ID/name, filter by status
- **Duration Calculation**: Automatic hours worked calculation
- **Quick Statistics**: Average attendance %, peak hours, total records
- **Export Options**: Download as CSV or JSON

## Configuration ⚙️

Edit `config.py` to customize:
```python
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
BACKUP_FOLDER = os.path.join(os.path.dirname(__file__), 'backups')
DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'vision_attendance.db')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB file upload limit
```

## Troubleshooting 🔧

### Issue: "Cannot operate on a closed database"
- **Cause**: Manual `conn.close()` calls conflicting with Flask teardown
- **Fix**: Already resolved in current version using Flask g object and teardown_appcontext

### Issue: Face recognition returns no matches
- **Check 1**: Staff photos uploaded clearly with visible face
- **Check 2**: Run face encoding: `encode_faces()` is called automatically on registration
- **Check 3**: Verify `face_data/encodings.pkl` exists after registering staff

### Issue: Camera not working on biometric scan
- **Check**: Browser permissions for camera access (Chrome/Firefox)
- **Check**: HTTPS required in production (localhost works with HTTP)
- **Fix**: Use `https://` or `localhost` URL

### Issue: Database locked errors
- **Cause**: Multiple processes accessing database
- **Fix**: Ensure only one Flask instance running on port 5000

## Performance Tips 📈

1. **Database Optimization**:
   - Indexes are on UNIQUE(emp_id, attendance_date) for fast lookups
   - Consider indexing emp_id, attendance_date separately for large datasets

2. **Face Recognition**:
   - CNN model more accurate but slower than HOG
   - Batching multiple face encodings for bulk registration recommended

3. **File Management**:
   - Regular backups prevent data loss
   - Clean old backups to save disk space

## Security Considerations 🔒

1. **File Upload**: Uses `secure_filename()` to prevent directory traversal
2. **Database**: SQLite suitable for single-instance; consider PostgreSQL for multi-user
3. **Face Data**: Encodings stored locally; consider encryption for sensitive deployments
4. **Authentication**: Currently open-access; add login system for production

## Future Enhancements 🔮

- [ ] User authentication & role-based access
- [ ] Email notifications for attendance alerts
- [ ] Advanced reporting (PDF exports, charts)
- [ ] Mobile app integration
- [ ] Real-time attendance dashboard (WebSocket)
- [ ] Liveness detection to prevent spoofing
- [ ] Multi-site support with data sync

## Contributing 🤝

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

## License 📜

MIT License - See LICENSE file for details

## Support 💬

For issues, questions, or feature requests, please open an issue in the repository.

---

**Built with ❤️ using Flask & Face Recognition Technology**

*Last Updated: 2024*
