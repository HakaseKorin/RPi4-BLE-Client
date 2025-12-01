import asyncio
from bleak import BleakClient, BleakScanner

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID     = "12345678-1234-5678-1234-56789abcdef1"

async def main():
    print("Scanning for ESP32...")
    devices = await BleakScanner.discover()

    esp = None
    for d in devices:
        if "ESP32_Server" in d.name:
            esp = d
            break

    if esp is None:
        print("ESP32 not found")
        return

    async with BleakClient(esp.address) as client:
        print(f"Connected to {esp.address}")

        while True:
            msg = input("Enter data to send to ESP32: ")
            data = msg.encode()
            await client.write_gatt_char(CHAR_UUID, data, response=True)
            print("Sent:", msg)

asyncio.run(main())
