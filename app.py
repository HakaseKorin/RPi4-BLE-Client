import asyncio
from bleak import BleakClient, BleakScanner # pip install bleak

SV_UUID="ca695dc1-f8ee-4963-a0ec-d60dd3c30eef" # Service Uuid
TX_UUID="ca695dc2-f8ee-4963-a0ec-d60dd3c30eef"
RX_UUID="ca695dc3-f8ee-4963-a0ec-d60dd3c30eef"

DEVICE_NAME="UART Service"

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

# Do have one async main function that does everything.
async def main():
    await scan_and_connect()

    while True:
        disconnect_event = asyncio.Event()

        # do all the back and forth in here..
        try:
            async with BleakClient(
                device, disconnected_callback=lambda c: disconnect_event.set()
            ) as client:
                data = await client.read_gatt_char(TX_UUID)
                print("received:", data)

                await disconnect_event.wait()
                print("device disconnected")

        except Exception:
            print("Exception while connecting/connected")

asyncio.run(scan_and_connect())
print("program stopped")

#TODO: make a case incase of diconnection when communicating to other devices.
# just reuse scan & connect for this case
#TODO: add ability to send to BLE Server
#TODO: add other functionality when its finished