from puffcoble import PuffcoBLE
from puffcoble.puffco.constants import ModeCommands
import asyncio
import cbor2
import re, ast

async def main():
    device = PuffcoBLE(device_name='DEV PUFFCO', debug=True)
    await device.connect()
    
    profileName = await device.get_profile_name()
    profileTemp = await device.get_profile_temp()
    profileDuration = await device.get_profile_time()
    profileIndex = await device.get_current_profile()
    chamberType = await device.get_chamber_type()
    print(f"Connected to {device.device_name}\nProfile Index: {profileIndex}\nProfile Name: {profileName}\nProfile Temperature: {profileTemp}\nProfile Duration: {profileDuration}\nChamber Type: {chamberType.name}")

asyncio.run(main())