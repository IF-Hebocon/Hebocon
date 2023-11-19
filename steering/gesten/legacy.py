import struct
import sys

import cv2
import mediapipe as mp
import serial
import serial.tools.list_ports
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

ADDRESS_FLAG = 137
CONTROL_FLAG = 186

REDUCE_BAUD_RATE = True
BAUD_RATE = 9600 / (4 if REDUCE_BAUD_RATE else 1)


def get_serial_ports():
    """Lists serial port names"""
    return [port.device for port in serial.tools.list_ports.comports()]


def select_serial_port():
    """Allow user to select a serial port, or automatically select if only one is available"""
    ports = get_serial_ports()
    if len(ports) == 1:
        return ports[0]
    elif len(ports) > 1:
        print("Available ports:")
        for i, port in enumerate(ports):
            print(f"{i}: {port}")
        selection = int(input("Select port: "))
        return ports[selection]
    else:
        print("No serial ports found.")
        sys.exit(1)


serial_port = select_serial_port()
ser = serial.Serial(serial_port, BAUD_RATE)


def send(flag, value):
    data = struct.pack('BB', flag, value)
    ser.write(data)


address = int(input("Address number: "))
send(ADDRESS_FLAG, address)

if ser.readline().strip() != b'OK':
    sys.exit(1)

print('--- Connection established ---')

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


def interpret_gesture(hand_landmarks):
    # Get the tip and base landmarks for all fingers
    thumb_tip = hand_landmarks[mpHands.HandLandmark.THUMB_TIP]
    thumb_mcp = hand_landmarks[mpHands.HandLandmark.THUMB_MCP]
    index_tip = hand_landmarks[mpHands.HandLandmark.INDEX_FINGER_TIP]
    index_mcp = hand_landmarks[mpHands.HandLandmark.INDEX_FINGER_MCP]
    middle_tip = hand_landmarks[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_mcp = hand_landmarks[mpHands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_tip = hand_landmarks[mpHands.HandLandmark.RING_FINGER_TIP]
    ring_mcp = hand_landmarks[mpHands.HandLandmark.RING_FINGER_MCP]
    pinky_tip = hand_landmarks[mpHands.HandLandmark.PINKY_TIP]
    pinky_mcp = hand_landmarks[mpHands.HandLandmark.PINKY_MCP]

    # Check if each finger is extended
    thumb_extended = thumb_tip.y < thumb_mcp.y
    index_extended = index_tip.y < index_mcp.y
    middle_extended = middle_tip.y < middle_mcp.y
    ring_extended = ring_tip.y < ring_mcp.y
    pinky_extended = pinky_tip.y < pinky_mcp.y

    # Check for specific gestures
    if index_extended and middle_extended and not thumb_extended and not ring_extended and not pinky_extended:
        return 'Peace'
    elif thumb_extended and index_extended and middle_extended and ring_extended and pinky_extended:
        return 'Open_Palm'
    elif not thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
        if thumb_tip.x < pinky_tip.x:
            return 'Closed_Fist_Left'
        elif thumb_tip.x > pinky_tip.x:
            return 'Closed_Fist_Right'
        else:
            return 'Fist'
    else:
        return 'Unknown'


def callback(result, _, __):
    command = 0

    if len(result.hand_landmarks) == 0:
        return

    for handLms in result.hand_landmarks:
        gesture_name = interpret_gesture(handLms)
        print(gesture_name)

        # Define the commands based on the gesture_name
        if gesture_name == 'Open_Palm':
            command = 1  # Forward
        elif gesture_name == 'Closed_Fist_Left':
            command = 2  # Left
        elif gesture_name == 'Closed_Fist_Right':
            command = 4  # Right
        elif gesture_name == 'Fist':
            command = 5  # NOOP
        elif gesture_name == 'Peace':
            command = 3  # Reverse

    send(CONTROL_FLAG, command)


base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options, running_mode=vision.RunningMode.LIVE_STREAM, result_callback=callback)
recognizer = vision.GestureRecognizer.create_from_options(options)

timestamp = 0
while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    timestamp += 1
    recognizer.recognize_async(mp.Image(image_format=mp.ImageFormat.SRGB, data=imageRGB), timestamp)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow('Output', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
cap.release()
cv2.destroyAllWindows()
