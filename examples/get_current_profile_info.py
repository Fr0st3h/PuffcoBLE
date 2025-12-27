from puffcoble import PuffcoBLE
from puffcoble.puffco.constants import ModeCommands
import asyncio
import cbor2
import re, ast

async def main():
    device = PuffcoBLE(device_name='DEV PUFFCO', debug=True)
    await device.connect()
    
    profileName = await device.get_current_profile_name()
    profileTemp = await device.get_current_profile_temp()
    profileDuration = await device.get_current_profile_duration()
    profileIndex = await device.get_current_profile_index()
    print(f"Connected to {device.device_name}, Profile Index: {profileIndex} Profile Name: {profileName}, Profile Temperature: {profileTemp}, Profile Duration: {profileDuration}")


asyncio.run(main())