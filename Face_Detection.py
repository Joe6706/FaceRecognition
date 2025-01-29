import cv2
import face_recognition
import os
import pickle

authentication = False

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

# List to store known face encodings and names
known_face_encodings = []
known_face_names = []

# Path to your dataset
dataset_path = 'example/Faces'  #Adjust Accordingly

# Filename for caching encodings
encodings_file = 'face_encodings.pkl'

# Function to save encodings to a file
def save_encodings(encodings, names, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump((encodings, names), f)

# Function to load encodings from a file
def load_encodings(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

# Function to compute and load face encodings from images
def load_faces(dataset_path):
    for person in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person)
        if os.path.isdir(person_path):  # Check if it's a directory
            for image in os.listdir(person_path):
                image_path = os.path.join(person_path, image)
                try:
                    img = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(img)
                    if encodings:  # Check if encoding was found
                        known_face_encodings.append(encodings[0])
                        known_face_names.append(person)
                except Exception as e:
                    print(f"Could not process image {image_path}: {e}")

# Load encodings from file if it exists, otherwise compute and save
if os.path.exists(encodings_file):
    known_face_encodings, known_face_names = load_encodings(encodings_file)
    print("Loaded cached face encodings from file.")
else:
    print("No cached encodings found. Computing from dataset...")
    load_faces(dataset_path)
    save_encodings(known_face_encodings, known_face_names, encodings_file)
    print("Face encodings computed and saved to cache.")

# Now continue with the face recognition process in real-time
while True:
    ret, frame = video_capture.read()
    frame = cv2.resize(frame, (640, 480))  # Resize frame to speed up processing

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

        # Print recognized name
        if name != "Unknown":
            print(f"Recognized: {name}")
            authentication = True
        else:
            print("Unknown face detected")

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
video_capture.release()
cv2.destroyAllWindows()

