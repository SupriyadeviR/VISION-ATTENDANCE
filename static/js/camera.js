// ================================
// ADVANCED CAMERA CONTROLLER
// Face Attendance System
// ================================

let video = document.getElementById("video");
let canvas = document.getElementById("canvas");
let statusText = document.getElementById("status");
let stream = null;

// ================================
// START CAMERA
// ================================
async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: "user"
            },
            audio: false
        });

        video.srcObject = stream;
        video.play();

        updateStatus("📷 Camera started. Look at the camera...", "success");
    } catch (error) {
        console.error(error);
        updateStatus("❌ Camera access denied!", "fail");
    }
}

// ================================
// STOP CAMERA
// ================================
function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
        updateStatus("🛑 Camera stopped", "fail");
    }
}

// ================================
// CAPTURE FRAME & SEND TO SERVER
// ================================
function captureAndRecognize() {
    if (!stream) {
        updateStatus("⚠️ Camera not running", "fail");
        return;
    }

    const ctx = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append("frame", blob, "frame.jpg");

        updateStatus("🧠 Scanning face...", "success");

        fetch("/mark_attendance", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                updateStatus(
                    `✅ Attendance marked for ${data.emp}`,
                    "success"
                );
            } else {
                updateStatus("❌ Face not recognized", "fail");
            }
        })
        .catch(err => {
            console.error(err);
            updateStatus("❌ Server error", "fail");
        });
    }, "image/jpeg");
}

// ================================
// AUTO SCAN MODE (OPTIONAL)
// ================================
let autoScanInterval = null;

function startAutoScan(interval = 5000) {
    if (autoScanInterval) return;

    updateStatus("🤖 Auto scan enabled", "success");

    autoScanInterval = setInterval(() => {
        captureAndRecognize();
    }, interval);
}

function stopAutoScan() {
    clearInterval(autoScanInterval);
    autoScanInterval = null;
    updateStatus("🛑 Auto scan stopped", "fail");
}

// ================================
// UI STATUS HANDLER
// ================================
function updateStatus(message, type) {
    if (!statusText) return;

    statusText.innerText = message;
    statusText.className = "badge " + (type === "success" ? "success" : "fail");
}

// ================================
// CLEANUP ON PAGE EXIT
// ================================
window.addEventListener("beforeunload", () => {
    stopCamera();
});
