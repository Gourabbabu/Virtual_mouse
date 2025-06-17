import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
from collections import deque

# Initialize MediaPipe Hands
def init_hands():
    return mp.solutions.hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

# Constants and settings
SMOOTHING_ALPHA = 0.05   # exponential smoothing factor
MOVING_AVG_WINDOW = 15   # frames for moving average
SENSITIVITY = 1.3        # higher = more sensitive cursor movement
FIST_THRESHOLD = 0.1     # mean fingertip-to-wrist distance for fist click
PINCH_THRESHOLD = 0.05   # distance for right-click pinch
CLICK_COOLDOWN = 0.7      # seconds between clicks

# Screen dimensions
screen_w, screen_h = pyautogui.size()

# Landmark indices
I_WRIST = 0
TIP_INDEX = 8
TIP_MIDDLE = 12
FINGER_TIPS = [8, 12, 16, 20]

# Globals for smoothing and clicks
pos_buffer = deque(maxlen=MOVING_AVG_WINDOW)
prev_x, prev_y = None, None
last_left_click = 0
last_right_click = 0

# Utility: get hand landmarks
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = init_hands()

def get_frame_landmarks(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)
    if not res.multi_hand_landmarks:
        return None
    return res.multi_hand_landmarks[0]

# Main loop
def main():
    global prev_x, prev_y, last_left_click, last_right_click

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam error")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Mirror frame for natural movement
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        hand = get_frame_landmarks(frame)
        if hand:
            # Index fingertip normalized coords
            idx = hand.landmark[TIP_INDEX]
            # Sensitivity mapping from center
            center_x, center_y = screen_w / 2, screen_h / 2
            raw_x = idx.x * screen_w
            raw_y = idx.y * screen_h
            # Apply sensitivity around center
            raw_x = center_x + (raw_x - center_x) * SENSITIVITY
            raw_y = center_y + (raw_y - center_y) * SENSITIVITY
            # Clamp
            raw_x = np.clip(raw_x, 0, screen_w)
            raw_y = np.clip(raw_y, 0, screen_h)

            # Smoothing: moving average
            pos_buffer.append((raw_x, raw_y))
            avg_x = np.mean([p[0] for p in pos_buffer])
            avg_y = np.mean([p[1] for p in pos_buffer])

            # Exponential smoothing
            if prev_x is None:
                smooth_x, smooth_y = avg_x, avg_y
            else:
                smooth_x = prev_x + SMOOTHING_ALPHA * (avg_x - prev_x)
                smooth_y = prev_y + SMOOTHING_ALPHA * (avg_y - prev_y)
            prev_x, prev_y = smooth_x, smooth_y

            # Move cursor
            pyautogui.moveTo(smooth_x, smooth_y)

            # Click gestures
            # Fist detection for left-click
            wrist = hand.landmark[I_WRIST]
            dists = [np.hypot(hand.landmark[t].x - wrist.x,
                              hand.landmark[t].y - wrist.y)
                     for t in FINGER_TIPS]
            mean_dist = np.mean(dists)
            now = time.time()
            if mean_dist < FIST_THRESHOLD and now - last_left_click > CLICK_COOLDOWN:
                pyautogui.click(button='left')
                last_left_click = now

            # Pinch for right-click
            mid = hand.landmark[TIP_MIDDLE]
            pinch_dist = np.hypot(idx.x - mid.x, idx.y - mid.y)
            if pinch_dist < PINCH_THRESHOLD and now - last_right_click > CLICK_COOLDOWN:
                pyautogui.click(button='right')
                last_right_click = now

            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Hand Mouse', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
