import cv2
import face_recognition
import os
import pickle

# Path to save the temporary video
video_path = "temp_video.avi"

# Path to the face encodings cache
encodings_file = 'face_encodings.pkl'

# Initialize encoding and name lists
known_face_encodings = []
known_face_names = []

# Function to load encodings from file
def load_encodings(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    return [], []

# Function to save encodings to a file
def save_encodings(encodings, names, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump((encodings, names), f)

# Step 1: Record a short video
def record_video(duration=10, fps=20):
    print("Recording video...")
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    frames_recorded = 0
    while frames_recorded < duration * fps:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break
        out.write(frame)
        frames_recorded += 1

    cap.release()
    out.release()
    print("Video recorded successfully.")

# Step 2: Extract frames from the video
def extract_frames(video_path, frame_interval=5):
    print("Extracting frames...")
    cap = cv2.VideoCapture(video_path)
    frame_list = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_list.append(frame)
        frame_count += 1

    cap.release()
    print(f"Extracted {len(frame_list)} frames.")
    return frame_list

# Step 3: Process frames to generate face encodings
def generate_encodings_from_frames(frames, name):
    new_encodings = []
    for frame in frames:
        # Convert the frame to RGB (face_recognition expects RGB images)
        rgb_frame = frame[:, :, ::-1]
        face_encodings = face_recognition.face_encodings(rgb_frame)
        new_encodings.extend(face_encodings)

    print(f"Generated {len(new_encodings)} face encodings for {name}.")
    return new_encodings

# Main process
if __name__ == "__main__":
    # Load existing encodings
    known_face_encodings, known_face_names = load_encodings(encodings_file)

    # Step 1: Record video
    record_video(duration=10)

    # Step 2: Extract frames
    frames = extract_frames(video_path)

    # Step 3: Generate face encodings
    name = input("Enter the name of the person: ")
    new_encodings = generate_encodings_from_frames(frames, name)

    # Step 4: Filter and save new encodings
    for encoding in new_encodings:
        if encoding not in known_face_encodings:
            known_face_encodings.append(encoding)
            known_face_names.append(name)

    # Save updated encodings
    save_encodings(known_face_encodings, known_face_names, encodings_file)
    print(f"Face encodings for {name} have been added successfully.")

    # Clean up temporary video
    if os.path.exists(video_path):
        os.remove(video_path)
        print("Temporary video file deleted.")
