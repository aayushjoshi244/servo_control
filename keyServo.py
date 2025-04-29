import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)

# Setup PWM
servo = GPIO.PWM(servo_pin, 50)  # 50 Hz
servo.start(0)

def move_servo(angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    print(f"Moving to {angle} degrees → duty: {duty:.2f}")
    time.sleep(1.5)  # Hold signal longer so servo can reach the angle
    servo.ChangeDutyCycle(0)  # Stop signal (to avoid jittering)

print("Press 'O' to open (rotate 90°), 'C' to close (rotate 0°), 'Q' to quit.")

try:
    while True:
        key = input("Enter command (O/C/Q): ").strip().upper()

        if key == 'O':
            print("Opening servo fully...")
            move_servo(90)  # You can go up to 120 if your servo allows

        elif key == 'C':
            print("Closing servo fully...")
            move_servo(0)

        elif key == 'Q':
            print("Quitting...")
            break

        else:
            print("Invalid input. Please press 'O', 'C', or 'Q'.")

except KeyboardInterrupt:
    print("Interrupted manually.")

finally:
    servo.stop()
    GPIO.cleanup()
