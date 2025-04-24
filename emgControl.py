import spidev
import RPi.GPIO as GPIO
import time

# ---------- GPIO & Servo Setup ----------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servo1_pin = 17
servo2_pin = 27

GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

servo1 = GPIO.PWM(servo1_pin, 50)  # 50Hz frequency
servo2 = GPIO.PWM(servo2_pin, 50)

servo1.start(0)
servo2.start(0)

def move_servo(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

# ---------- SPI & MCP3008 Setup ----------
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CS) 0
spi.max_speed_hz = 1350000

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# ---------- Thresholds ----------
open_hand_threshold = 500  # All fingers open (strong signal)
peace_sign_threshold = 300  # Index + middle active

try:
    while True:
        # Read EMG channels (you can expand this for more channels)
        emg1 = read_channel(0)  # Channel 0 (maybe forearm)
        emg2 = read_channel(1)  # Channel 1 (maybe biceps)

        print(f"EMG1: {emg1}, EMG2: {emg2}")

        if emg1 > open_hand_threshold and emg2 > open_hand_threshold:
            print("🖐️ Open hand detected → Servo 1 Move")
            move_servo(servo1, 90)

        elif emg1 > peace_sign_threshold and emg2 < peace_sign_threshold:
            print("✌️ Peace sign detected → Servo 2 Move")
            move_servo(servo2, 90)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
    spi.close()
