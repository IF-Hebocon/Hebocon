import math
import struct
import sys

import cv2
import mediapipe as mp
import numpy as np
import serial
import serial.tools.list_ports

from time import sleep

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

sleep(3)  # Wait for Arduino


def send(flag, value):
    data = struct.pack('BB', flag, value)
    ser.write(data)


address = int(input("Address number: "))
send(ADDRESS_FLAG, address)

response = ser.readline().strip()
if response != b'OK':
    sys.exit(1)

print('--- Connection established ---')

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils
mpDrawStyles = mp.solutions.drawing_styles


# Function to calculate the distance between two landmarks.
def distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2) ** 0.5


# Helper function to calculate the angle between three points
def calculate_angle(landmark1, landmark2, landmark3):
    a = [landmark1.x - landmark2.x, landmark1.y - landmark2.y]
    b = [landmark3.x - landmark2.x, landmark3.y - landmark2.y]

    inner_product = a[0] * b[0] + a[1] * b[1]
    norm_a = math.sqrt(a[0] ** 2 + a[1] ** 2)
    norm_b = math.sqrt(b[0] ** 2 + b[1] ** 2)

    cos_angle = inner_product / (norm_a * norm_b)
    angle = math.acos(cos_angle)

    return math.degrees(angle)


# Function to check if a finger is extended
def is_finger_extended(landmarks, finger_joints):
    mcp, pip, dip, tip = [landmarks[joint] for joint in finger_joints]
    angle = calculate_angle(mcp, pip, dip)
    # return angle > 160  # Threshold for extended finger, can be adjusted
    return tip.y < mcp.y


# Main function to get the map of extended fingers
def get_extended_fingers(landmarks):
    # Define the joints for each finger
    fingers_joints = {
        "Thumb": [mp_hands.HandLandmark.THUMB_CMC, mp_hands.HandLandmark.THUMB_MCP, mp_hands.HandLandmark.THUMB_IP, mp_hands.HandLandmark.THUMB_TIP],
        "Index": [mp_hands.HandLandmark.INDEX_FINGER_MCP, mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.INDEX_FINGER_DIP, mp_hands.HandLandmark.INDEX_FINGER_TIP],
        "Middle": [mp_hands.HandLandmark.MIDDLE_FINGER_MCP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_DIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
        "Ring": [mp_hands.HandLandmark.RING_FINGER_MCP, mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.RING_FINGER_DIP, mp_hands.HandLandmark.RING_FINGER_TIP],
        "Pinky": [mp_hands.HandLandmark.PINKY_MCP, mp_hands.HandLandmark.PINKY_PIP, mp_hands.HandLandmark.PINKY_DIP, mp_hands.HandLandmark.PINKY_TIP]
    }

    # Check if each finger is extended
    extended_fingers = {finger: is_finger_extended(landmarks, joints) for finger, joints in fingers_joints.items()}
    extended_fingers['Thumb'] = distance(landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP], landmarks[mp_hands.HandLandmark.THUMB_TIP]) > 0.05
    return extended_fingers


# Function to detect gestures.
def detect_gesture2(landmarks):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]

    # Detect Open Palm
    if all(distance(thumb_tip, other) > 0.1 for other in [index_tip, middle_tip, ring_tip, pinky_tip]):
        return "Open Palm"

    # Detect Closed Fist
    # if all(distance(thumb_tip, other) < 0.1 for other in [index_tip, middle_tip, ring_tip, pinky_tip]):
    #     return "Closed Fist"

    if distance(thumb_tip, landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP]) < 0.05:
        return "Closed Fist"

    # Detect Peace Sign
    if distance(index_tip, middle_tip) > 0.1 and all(distance(other, middle_tip) < 0.1 for other in [ring_tip, pinky_tip]):
        return "Peace Sign"

    # Detect Closed Fist with Thumb Left or Right
    thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_MCP]
    if distance(thumb_tip, thumb_mcp) < 0.1:
        if thumb_tip.x < thumb_mcp.x:
            return "Closed Fist, Thumb Left"
        else:
            return "Closed Fist, Thumb Right"

    return "Unknown"


# Function to detect gestures.
def detect_gesture(landmarks):
    fingers = get_extended_fingers(landmarks)

    # print(fingers)

    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_MCP]

    if fingers['Thumb'] and not any([fingers['Index'], fingers['Middle'], fingers['Ring'], fingers['Pinky']]):
        # if distance(thumb_tip, thumb_mcp) < 0.1:
        if thumb_tip.x < thumb_mcp.x:
            # return "Closed Fist, Thumb Left"
            return "Closed Fist, Thumb Right"
        else:
            # return "Closed Fist, Thumb Right"
            return "Closed Fist, Thumb Left"

    if not any(fingers.values()):
        return 'Closed Fist'

    if all([fingers['Index'], fingers['Middle']]) and not any([fingers['Thumb'], fingers['Ring'], fingers['Pinky']]):
        return 'Peace Sign'

    if all(fingers.values()):
        return 'Open Palm'

    return None


def map_gesture_str(gesture_str):
    if gesture_str == 'Open Palm':
        return 1
    elif gesture_str == 'Closed Fist, Thumb Left':
        return 2
    elif gesture_str == 'Peace Sign':
        return 3
    elif gesture_str == 'Closed Fist, Thumb Right':
        return 4
    elif gesture_str == 'Closed Fist':
        return 5
    else:
        return None


def update_queue(queue, new_element, max_length):
    queue.append(new_element)
    if len(queue) > max_length:
        queue.pop(0)
    return queue


def calculate_hand_centroid(landmarks):
    x = [landmark.x for landmark in landmarks]
    y = [landmark.y for landmark in landmarks]
    centroid = np.mean(np.array([x, y]), axis=1)
    return centroid


def has_hand_stopped(prev_positions, current_position, stability_threshold, frames_stable_required):
    if len(prev_positions) < frames_stable_required:
        return False

    for pos in prev_positions[-frames_stable_required:]:
        if np.linalg.norm(pos - current_position) > stability_threshold:
            return False
    return True


stability_threshold = 0.01  # Adjust based on your requirement
frames_stable_required = 3  # Number of frames to check for stability
previous_positions = []
last_gesture = None
last_gestures = []
while True:
    success, image = cap.read()
    if not success:
        break
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    multi_hand_landmarks = getattr(results, 'multi_hand_landmarks')

    if multi_hand_landmarks:
        hand_landmarks = multi_hand_landmarks[0]

        hand_position = calculate_hand_centroid(hand_landmarks.landmark)
        previous_positions = update_queue(previous_positions, hand_position, frames_stable_required)

        if has_hand_stopped(previous_positions, hand_position, stability_threshold, frames_stable_required):
            # Perform gesture detection.
            gesture = detect_gesture(hand_landmarks.landmark)
            if gesture and last_gesture != gesture:
                last_gestures = update_queue(last_gestures, gesture, 5)

                if all(gesture == x for x in last_gestures):
                    last_gesture = gesture
                    print(gesture)
                    send(CONTROL_FLAG, map_gesture_str(gesture))

        mpDraw.draw_landmarks(image,
                              hand_landmarks,
                              mp_hands.HAND_CONNECTIONS,
                              mpDraw.DrawingSpec(color=(31, 103, 249), thickness=5, circle_radius=6),
                              mpDraw.DrawingSpec(color=(255, 255, 255), thickness=2)
                              )
    else:
        last_gesture = None

    cv2.imshow('Output', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
cap.release()
cv2.destroyAllWindows()
