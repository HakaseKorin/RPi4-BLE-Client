import RPi.GPIO as GPIO
import time

# --- CONFIG ---
FPGA_PIN = 17   # physical pin 11 on Raspberry Pi header

# --- SETUP ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(FPGA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Listening for FPGA GPIO...")

try:
    while True:
        val = GPIO.input(FPGA_PIN)
        print("FPGA Signal:", val)
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
