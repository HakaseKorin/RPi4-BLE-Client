import serial

# RPi UART on GPIO14/15 is /dev/ttyS0 on Pi 4
ser = serial.Serial("/dev/ttyS0", 115200, timeout=1)

print("Listening for FPGA UART data...")

while True:
    data = ser.read(1)     # read 1 byte
    if data:
        value = data[0]    # convert byte to int
        print("Received:", value)