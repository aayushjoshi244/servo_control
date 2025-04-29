import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)

# Initialize PWM on the servo pin
servo = GPIO.PWM(servo_pin, 50)  # 50 Hz
servo.start(0)

def move_servo(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(servo_pin, False)
    servo.ChangeDutyCycle(0)

print("Press 'O' to open servo, 'C' to close it. Press 'Q' to quit.")

try:
    while True:
        key = input("Enter command (O/C/Q): ").strip().upper()

        if key == 'O':
            print("Opening servo...")
            move_servo(90)  # You can adjust to 120 or more if needed

        elif key == 'C':
            print("Closing servo...")
            move_servo(0)

        elif key == 'Q':
            print("Exiting...")
            break

        else:
            print("Invalid input. Please press 'O', 'C', or 'Q'.")

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    servo.stop()
    GPIO.cleanup()
