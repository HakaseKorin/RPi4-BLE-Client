import asyncio
from bleak import BleakClient, BleakScanner
import serial
import time

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID     = "12345678-1234-5678-1234-56789abcdef1"
DEVICE_NAME="ESP32_Server"

async def scan_and_connect():
    global device
    
    retries = 0
    while True:
        print(f"Scanning for device {DEVICE_NAME}")
        device = await BleakScanner.find_device_by_name(DEVICE_NAME)

        # Breaks out of loop once a connection is found
        if device is not None:
            print(f"Connected to {DEVICE_NAME} at...",device.address)
            break
        
        print("No device found.. Now attemping to reconnect.. (30s)")
        
        # Do use asyncio.sleep() in an asyncio program.
        await asyncio.sleep(30)
        retries += 1
        #TODO: change to properly end program
        if retries>10: return

async def main():
    await scan_and_connect()

    disconnect_event = asyncio.Event()

    ser = serial.Serial("/dev/serial0",9600,timeout=1)
    time.sleep(2)

    # do all the back and forth in here..
    try:
        async with BleakClient(
            device, disconnected_callback=lambda c: disconnect_event.set()
        ) as client:
            while True:
                
                if ser.in_waiting:
                    data = ser.readline().decode(errors="ignore").strip()
                    if data:
                        print("Received:", data)

                        if len(data) > 1:
                            commands = list(data)
                            for _ in commands:
                                msg = _
                                data = msg.encode()
                                await client.write_gatt_char(CHAR_UUID, data, response=True)
                                print("Sent:", msg)
                        else:
                            msg = data
                            data = msg.encode()
                            await client.write_gatt_char(CHAR_UUID, data, response=True)
                            print("Sent:", msg)
                        data = None # resets to none to wait for new input

    except Exception:
        print("Exception while connecting/connected", Exception)

asyncio.run(main())
