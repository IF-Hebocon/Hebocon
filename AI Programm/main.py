import sys

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
# import serial  # Uncomment when using Arduino

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Initialize Arduino COM connection
# ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your port

def callback(result, bla, blub):
    command = 'NOOP'

    if len(result.gestures) == 0:
        return

    gesture_name = result.gestures[0][0].category_name

    if gesture_name == 'Closed_Fist':
        command = 'NOOP'
    elif gesture_name == 'Open_Palm':
        command = 'FORWARD'
    elif gesture_name == 'Thumb_Up':
        command = 'LEFT'
    elif gesture_name == 'Thumb_Down':
        command = 'RIGHT'
    elif gesture_name == 'ILoveYou':
        command = 'ATTACK'

    # ser.write(command.encode())
    print(command)

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options, running_mode=vision.RunningMode.LIVE_STREAM, result_callback=callback)
recognizer = vision.GestureRecognizer.create_from_options(options)

# Initialize Arduino COM connection
# ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your port

timestamp = 0
while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    timestamp += 1
    recognizer.recognize_async(mp.Image(image_format=mp.ImageFormat.SRGB, data=imageRGB), timestamp)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Uncomment when using Arduino
            # ser.write(gesture.encode())
            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow('Output', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ser.close()  # Uncomment when using Arduino
cap.release()
cv2.destroyAllWindows()