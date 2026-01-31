# 🚀 VisionPresence - Quick Start Guide

## Step 1: Start the Server
```bash
python app.py
```
Server runs at: http://127.0.0.1:5000

## Step 2: Register Staff Members

**URL**: http://127.0.0.1:5000/register

1. Click "Register Staff"
2. Fill in details:
   - Employee ID (e.g., E001)
   - Name
   - Email
   - Phone
   - Date of Birth
   - Designation
   - Department
   - Native (origin/location)
3. Click "Capture Photo"
4. Allow camera access
5. Smile and take the photo
6. Click "Register" to save

✅ Staff is now registered and face is encoded for recognition

---

## Step 3: Mark Attendance via Biometric Scan

**URL**: http://127.0.0.1:5000/scan

### First Scan (Time In - Morning)
1. Click "Start Camera"
2. Position your face in the camera
3. Click "Scan Face & Mark Attendance"
4. ✅ You'll see "Welcome! Time In recorded"
5. Your photo is automatically saved to `uploads/scans/`

### Second Scan (Time Out - Evening)
1. Click "Start Camera"
2. Scan your face again
3. Click "Scan Face & Mark Attendance"
4. ✅ You'll see "Time Out recorded. Have a good day!"
5. Your attendance duration is auto-calculated

---

## Step 4: View & Export Reports

**URL**: http://127.0.0.1:5000/attendance

### View All Records
- See complete attendance history
- Search by employee name
- Filter by status (Present/Absent)

### Export Data
- **📊 Excel**: Download as professional .xlsx file with formatting
- **📥 CSV**: Download as comma-separated values
- **📄 JSON**: Download as JSON format

All scanned face images are stored in `uploads/scans/` folder with timestamps

---

## Folder Structure

```
uploads/
├── scans/                    ← Your scanned face images
│   ├── E001_20260129_090000.jpg  (Time In photo)
│   ├── E001_20260129_180000.jpg  (Time Out photo)
│   └── ...
```

Each file is named: `{EMPLOYEE_ID}_{TIMESTAMP}.jpg`

---

## Features Summary

✅ **Automatic Staff Registration**
   - Photo capture and face encoding
   - All data saved to database

✅ **Automatic Attendance Marking**
   - First scan = Time In
   - Second scan = Time Out
   - Scanned photos automatically saved

✅ **Smart Duration Calculation**
   - System calculates hours worked automatically
   - Shows in Excel reports

✅ **Professional Reports**
   - Export to Excel with formatting
   - CSV for spreadsheet imports
   - JSON for integrations

✅ **Face Image Backup**
   - All scanned photos saved with date/time
   - Can review who scanned when

---

## 🎯 System Requirements

- Python 3.10+
- Webcam/Camera device
- Browser (Chrome, Firefox, Edge)
- Modern operating system (Windows/Linux/Mac)

---

## Support

For any issues:
1. Check that camera is working
2. Ensure staff member is registered before scanning
3. Verify face is clearly visible under good lighting
4. Check `uploads/scans/` folder for exported images

**System Status**: ✅ Ready to Use
