import cv2
import mediapipe as mp
import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servo1_pin = 17
servo2_pin = 27

GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

servo1 = GPIO.PWM(servo1_pin, 50)  # 50Hz
servo2 = GPIO.PWM(servo2_pin, 50)

servo1.start(0)
servo2.start(0)

def move_servo(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

# MediaPipe init
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Finger tip landmarks
fingertips_ids = [4, 8, 12, 16, 20]

def fingers_up(hand_landmarks):
    finger_states = []

    # Thumb
    finger_states.append(hand_landmarks.landmark[fingertips_ids[0]].x < hand_landmarks.landmark[fingertips_ids[0] - 1].x)

    # Other four fingers
    for tip_id in fingertips_ids[1:]:
        finger_states.append(hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y)

    return finger_states

cap = cv2.VideoCapture(0)

try:
    while True:
        success, img = cap.read()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

                finger_status = fingers_up(handLms)

                if all(finger_status):  # All fingers up
                    print("Open Hand detected → Servo 1 Move")
                    move_servo(servo1, 90)

                elif finger_status == [False, True, True, False, False]:  # Index & middle only
                    print("Peace sign detected → Servo 2 Move")
                    move_servo(servo2, 90)

        cv2.imshow("Floppy Cam", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Exiting...")

finally:
    cap.release()
    cv2.destroyAllWindows()
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
