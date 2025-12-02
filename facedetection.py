import cv2
import numpy as np

# Load OpenCV Haarcascade (face detector)
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------------------
# 1. FACE DETECTION
# ---------------------------
def detect_face(image_path):
    """
    Detects the largest face in an image and returns the cropped region.
    """
    img = cv2.imread(image_path)

    if img is None:
        print("[ERROR] Image not found:", image_path)
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    if len(faces) == 0:
        print("[INFO] No face detected:", image_path)
        return None

    # Pick the largest face
    x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
    face_crop = img[y:y+h, x:x+w]

    return face_crop


# ---------------------------
# 2. PREPROCESS FOR EMBEDDING
# ---------------------------
def preprocess_face_for_embedding(face):
    """
    Converts face to 96x96 grayscale normalized embedding.
    This keeps training + recognition consistent.
    """
    try:
        # Resize for uniform embeddings
        face = cv2.resize(face, (96, 96))

        # Convert to grayscale
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        # Normalize 0–1
        gray = gray.astype("float32") / 255.0

        return gray
    except Exception as e:
        print("Preprocessing failed:", e)
        return None
