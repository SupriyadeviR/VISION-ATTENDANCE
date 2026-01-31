import os
import pickle
import face_recognition
from utils.db_utils import get_db
from datetime import datetime

# 🔹 Folder where staff images are stored
FACE_DATA_FOLDER = "uploads/"
ENCODINGS_FILE = "face_data/encodings.pkl"

# 🔹 Load known face encodings from file
def load_encodings():
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            known_encodings = pickle.load(f)
        return known_encodings
    return {}

# 🔹 Encode all faces in the staff folder and save to encodings.pkl
def encode_faces():
    known_encodings = {}
    conn = get_db()
    staff_list = conn.execute("SELECT emp_id, image_path FROM staff").fetchall()

    for staff in staff_list:
        emp_id = staff["emp_id"]
        # `image_path` stores the absolute path when saved during registration
        image_file = staff["image_path"]

        if not image_file or not os.path.exists(image_file):
            continue

        image = face_recognition.load_image_file(image_file)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings[emp_id] = encodings[0]  # Take the first face

    # Save encodings
    os.makedirs(os.path.dirname(ENCODINGS_FILE), exist_ok=True)
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(known_encodings, f)
    print(f"[✅] Encoded {len(known_encodings)} staff faces.")
    return known_encodings

# 🔹 Recognize face from a camera frame
def recognize_faces_from_frame(frame, known_encodings):
    # frame is already RGB from load_image_file
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    recognized = []

    for face_encoding, location in zip(face_encodings, face_locations):
        for emp_id, known_encoding in known_encodings.items():
            distance = face_recognition.face_distance([known_encoding], face_encoding)
            if distance[0] < 0.6:  # Tolerance level
                recognized.append({
                    "emp_id": emp_id,
                    "location": location,
                    "distance": distance[0]
                })
                break

    return recognized

# 🔹 Mark attendance automatically
def mark_attendance(emp_id):
    conn = get_db()
    # Current attendance schema stores emp_id and a timestamp (DEFAULT CURRENT_TIMESTAMP)
    conn.execute(
        "INSERT INTO attendance (emp_id) VALUES (?)",
        (emp_id,)
    )
    conn.commit()
