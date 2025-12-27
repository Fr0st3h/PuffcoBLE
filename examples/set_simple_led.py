from puffcoble import PuffcoBLE
from puffcoble.puffco.constants import ModeCommands
import asyncio
import cbor2
import re, ast

async def main():
    device = PuffcoBLE(device_name='DEV PUFFCO', debug=True)
    await device.connect()
    
    payload = {'lamp': {'name': 'solid', 'param': {'color': ["#b700ff"]}}}
    
    profileIndex = int(await device.get_current_profile_index())
    await device.write_cbor_full(f"/u/app/hc/{profileIndex}/colr", payload)
    print(f'Wrote colour to profile {profileIndex}')



asyncio.run(main())