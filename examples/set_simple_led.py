from puffcoble import PuffcoBLE
from puffcoble.puffco.constants import ModeCommands
import asyncio
import cbor2
import re, ast

async def main():
    device = PuffcoBLE(device_name='DEV PUFFCO', debug=True)
    await device.connect()
    
    payload = {'lamp': {'name': 'solid', 'param': {'color': ["#ff0000"]}}}
    
    profileIndex = int(await device.get_current_profile())

    await device.set_profile_colour(colour=payload)
    print(f'Wrote colour to profile {profileIndex}')



asyncio.run(main())