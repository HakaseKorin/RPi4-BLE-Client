import serial # pip install pyserial
import time

ser = serial.Serial('/dev/serial0', 115200, timeout=1)
time.sleep(2)

while True:
    data = ser.read(1)
    if data:
        print("Received:", data.hex())
        # after recieving information from the fpga board forward to esp32 for commands

"""
Notes for Usage
===============
TX pin on the FPGA De2i 150 Cyclone IV is gpio 15 referenced as PIN_G16 in the manual
connect this to the RX pin on the GPIO 15 pin on the Raspberry Pi 4

"""