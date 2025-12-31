from puffcoble import PuffcoBLE
from puffcoble.puffco.constants import ModeCommands, AnimationCode
import asyncio
import cbor2
import re, ast

async def main():
    device = PuffcoBLE(device_name='DEV PUFFCO', debug=True)
    await device.connect()

    payload = {
    "lamp":{
        "name":"pikaled2",
        "param":{
            "anim":AnimationCode.CIRCLING,
            "color":[
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#ffffff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff",
                "#a200ff"
        ],
            "plNum":0,
            "speed":20,
            "bright":255,
            "diFrac":0,
            "offset":[
                15360,
                18773,
                1707,
                5120,
                8533,
                11947,
                15360,
                10240,
                10240,
                5120,
                2844,
                1138,
                853,
                19627,
                19342,
                17636,
                0,
                0,
                0,
                0
            ],
            "plDenom":0,
            "colorLen":32,
            "speedDi0":4,
            "speedDi1":40
        }
    },
    "meta":{
        "version":3,
        "moodUlid":"00018E59EDEJJ53VBME8135KQD",
        "userColors":[
            "#ffffff",
            "#a200ff",
        ],
        "heatProfileUlid":"01K2B6GR5FQ707AASAC18RGWE8",
        "heatProfileDateModified":1766836208
    }
}

    profileIndex = int(await device.get_current_profile())

    await device.set_profile_colour(colour=payload)
    print(f'Wrote colour to profile {profileIndex}')



asyncio.run(main())