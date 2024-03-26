import cv2
import dlib
import numpy as np


def extract_lip_color(image_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        lip_points = np.array([[landmarks.part(x).x, landmarks.part(x).y] for x in range(48, 68)])
        lip_mask = np.zeros_like(gray)
        lip_mask = cv2.fillPoly(lip_mask, [lip_points], 255)

        lip_color = cv2.bitwise_and(image, image, mask=lip_mask)
        
        mean_lip_color = cv2.mean(lip_color, mask=lip_mask)[:3]  # Ignoring the alpha channel if present
        
        return mean_lip_color


def extract_eyebrow_color(image_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Using only one eyebrow for better shape.
        eyebrow_points = np.array([[landmarks.part(x).x, landmarks.part(x).y] for x in range(18, 22)])
        eyebrow_mask = np.zeros_like(gray)
        eyebrow_mask = cv2.fillPoly(eyebrow_mask, [eyebrow_points], 255)
        eyebrow_color = cv2.bitwise_and(image, image, mask=eyebrow_mask) 
        mean_eyebrow_color = cv2.mean(eyebrow_color, mask=eyebrow_mask)[:3] 

    return mean_eyebrow_color


def extract_skin_color(image_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        cheek_points = np.array([[landmarks.part(0).x, landmarks.part(0).y], [landmarks.part(31).x, landmarks.part(31).y], [landmarks.part(2).x, landmarks.part(2).y]])
        cheek_mask = np.zeros_like(gray)
        cheek_mask = cv2.fillPoly(cheek_mask, [cheek_points], 255)
        cheek_color = cv2.bitwise_and(image, image, mask=cheek_mask)
        mean_cheek_color = cv2.mean(cheek_color, mask=cheek_mask)[:3]

        nose_points = np.array([[landmarks.part(27).x, landmarks.part(27).y], [landmarks.part(32).x, landmarks.part(32).y], [landmarks.part(34).x, landmarks.part(34).y]])
        nose_mask = np.zeros_like(gray)
        nose_mask = cv2.fillPoly(nose_mask, [nose_points], 255)
        nose_color = cv2.bitwise_and(image, image, mask=nose_mask)
        mean_nose_color = cv2.mean(nose_color, mask=nose_mask)[:3]

        chin_points = np.array([[landmarks.part(7).x, landmarks.part(7).y], [landmarks.part(9).x, landmarks.part(9).y], [landmarks.part(57).x, landmarks.part(57).y]])
        chin_mask = np.zeros_like(gray)
        chin_mask = cv2.fillPoly(chin_mask, [chin_points], 255)
        chin_color = cv2.bitwise_and(image, image, mask=chin_mask)
        mean_chin_color = cv2.mean(chin_color, mask=chin_mask)[:3]
        
        mean_skin_color = ()
        for i in range(3):
            mean_skin_color += (int((mean_cheek_color[i] + mean_nose_color[i] + mean_chin_color[i]) / 3),)

        return mean_skin_color
    

def extract_eye_color(image_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Using only one eye.
        eye_points = np.array([[landmarks.part(36).x, landmarks.part(36).y], [landmarks.part(37).x, landmarks.part(37).y], [landmarks.part(41).x, landmarks.part(41).y]])
        eye_mask = np.zeros_like(gray)
        eye_mask = cv2.fillPoly(eye_mask, [eye_points], 255)
        eye_color = cv2.bitwise_and(image, image, mask=eye_mask) 
        mean_eye_color = cv2.mean(eye_color, mask=eye_mask)[:3]
        
        return mean_eye_color

def get_colors(path_to_photo):
    colors = {
        "Lip Color": extract_lip_color(path_to_photo),
        "Eyebrow Color": extract_eyebrow_color(path_to_photo),
        "Skin Color": extract_skin_color(path_to_photo),
        "Eye Color": extract_eye_color(path_to_photo)
    }
    colors = {label: tuple(color[::-1]) for label, color in colors.items()}
    colors = {label: tuple(int(c) for c in color) for label, color in colors.items()}

    return colors