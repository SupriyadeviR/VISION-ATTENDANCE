# Quick Start Guide - VisionPresence Advanced 🚀

## Step 1: Setup (2 minutes)

```bash
# Navigate to project
cd VisionPresence_Advanced_Python

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python create_db.py
```

## Step 2: Run the Server (30 seconds)

```bash
python app.py
```

You'll see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

## Step 3: Open in Browser

Visit: **http://localhost:5000/overview**

You should see the main dashboard with 4 stat boxes.

## Step 4: Test Workflow (5 minutes)

### Test 1: Register Staff ✅
1. Click **➕ Register Staff** in sidebar
2. Fill form:
   - Name: "John Doe"
   - Email: "john@company.com"
   - Phone: "9876543210"
   - Department: "Engineering"
   - Gender: "Male"
   - Joining Date: "2024-01-15"
   - DOB: "1990-05-20"
   - Native: "New York"
   - Image: Upload a clear face photo
3. Click **Register**
4. Should see: ✅ Staff registered successfully!

### Test 2: View Staff ✅
1. Click **👥 Staff Database** in sidebar
2. Should see registered staff with:
   - Photo (avatar)
   - All details including DOB and Native
   - Delete button

### Test 3: Mark Attendance (Biometric Scan) ✅
1. Click **📸 Biometric Scan** in sidebar
2. Allow camera permission
3. Click **📷 Capture & Scan**
4. Should see:
   - ✅ Success: "Employee recognized, Time In recorded"
   - Or ℹ️ Info: "First recognition - please encode faces (register staff first)"

### Test 4: Check Time Out ✅
1. Go back to **Biometric Scan**
2. Click **📷 Capture & Scan** again (with same face)
3. Should see:
   - ✅ Success: "Time Out recorded"
   - Duration calculated automatically

### Test 5: View Attendance Logs ✅
1. Click **📊 Attendance Logs** in sidebar
2. Should see:
   - Employee name, date, time in, time out
   - Duration in hours (calculated)
   - Status badge (Present)
   - Search box to filter

### Test 6: Export Data ✅
1. On **Attendance Logs** page
2. Click **CSV** button → Downloads CSV file
3. Click **JSON** button → Downloads JSON file
4. Open in Excel/Text editor to verify

### Test 7: Backup Management ✅
1. Click **💾 Storage & Backup** in sidebar
2. See database size and backup count
3. Click **📥 Create Backup Now**
4. Should create timestamped backup file
5. Download or delete backups as needed

## Common Issues & Solutions 🔧

### Issue: Camera not working
**Solution**: 
- Ensure browser has permission to access camera
- Use `http://localhost` (not `https://` for local testing)
- Try Chrome or Firefox (best support)

### Issue: Face recognition not matching
**Solution**:
- Make sure staff was registered first with clear face photo
- Try registering another staff member
- Ensure good lighting during biometric scan

### Issue: Database locked
**Solution**:
- Close all browser tabs with the app
- Kill Python process: `Ctrl+C` in terminal
- Restart: `python app.py`

### Issue: Port 5000 already in use
**Solution**:
Edit `app.py` line 427:
```python
app.run(debug=True, port=5001)  # Use different port
```

## Key Features at a Glance 🎯

| Feature | Location | Action |
|---------|----------|--------|
| Dashboard | `/overview` | View system stats |
| Register Staff | `/register` | Add employee with photo |
| Staff List | `/staff` | View all employees |
| Biometric Scan | `/scan` | Mark attendance |
| Attendance Logs | `/attendance` | View & search records |
| Export Data | `/attendance` → CSV/JSON | Download reports |
| Backup Management | `/storage` | Create/download backups |

## Technology Details 🔧

**Backend**: Flask (Python)
**Database**: SQLite (vision_attendance.db)
**Face Recognition**: face_recognition library
**Theme**: Dark mode with modern UI
**Browser**: Chrome, Firefox, Edge (HTML5 Canvas required)

## Next Steps 📋

1. **Customize** colors in `templates/base.html` (search for `--bg-dark`, `--accent`, etc.)
2. **Add more staff** and test attendance workflows
3. **Set up scheduled backups** (optional automation)
4. **Deploy to server** when ready (consider PostgreSQL for production)

## Support 💬

If you encounter issues:
1. Check browser console (F12 → Console tab)
2. Check terminal output where Flask is running
3. Verify database file exists: `vision_attendance.db`

---

**Happy Attendance Tracking! 🎉**
