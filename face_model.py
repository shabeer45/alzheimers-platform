import os
import cv2
import numpy as np
import pickle
from facedetection import detect_face, preprocess_face_for_embedding

# Path for encoding storage
ENCODING_FILE = "faces.pickles"

# ----- TRAINING FUNCTION -----
def enf(train_folder):
    knownEncodings = []
    knownNames = []

    for person_id in os.listdir(train_folder):
        person_path = os.path.join(train_folder, person_id)

        if not os.path.isdir(person_path):
            continue

        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)

            face = detect_face(img_path)
            if face is None:
                continue

            face = preprocess_face_for_embedding(face)
            if face is None:
                continue

            # Flatten face as embedding (simple method)
            embedding = face.flatten()

            knownEncodings.append(embedding)
            knownNames.append(person_id)

    data = {"encodings": knownEncodings, "names": knownNames}

    with open(ENCODING_FILE, "wb") as f:
        pickle.dump(data, f)

    print("[INFO] Training completed!")
    return True


# ----- PREDICTION FUNCTIONS -----
def rec_face_image(img_path):
    if not os.path.exists(ENCODING_FILE):
        print("Encoding file not found!")
        return None

    with open(ENCODING_FILE, "rb") as f:
        data = pickle.load(f)

    encodings = data["encodings"]
    names = data["names"]

    face = detect_face(img_path)

    if face is None:
        return None

    face = preprocess_face_for_embedding(face)
    if face is None:
        return None

    face_embed = face.flatten()

    # Compare using cosine similarity
    best_score = 0
    best_name = None

    for stored_embed, name in zip(encodings, names):
        score = cosine_similarity(stored_embed, face_embed)
        if score > best_score:
            best_score = score
            best_name = name

    print("BEST SCORE:", best_score)

    # threshold — adjust if needed
    if best_score > 0.75:
        return [best_name]
    else:
        return None


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    dot = np.dot(a, b)
    normA = np.linalg.norm(a)
    normB = np.linalg.norm(b)
    return dot / (normA * normB + 1e-6)
