# PuffcoBLE

Python library for communicating with Puffco devices over Bluetooth Low Energy using the Lorax protocol.

This library allows you to connect to a Puffco device, authenticate, read and write Lorax paths, and control device features such as heat cycles, LEDs, lantern mode, and device information. Everything is async and built on top of `bleak`.

---

## Features

- Scan for devices by name or MAC address
- Automatic Lorax authentication
- Read and write Lorax paths
- Typed reads (int, float, bool) and raw byte reads
- Chunked reads for large data
- Start, stop, and boost heat cycles
- Lantern mode control
- LED brightness control
- Battery, firmware, uptime, and usage info
- Fully async / asyncio-based

---

## Requirements

- Python 3.11+
- Bluetooth Low Energy capable system

Supported platforms:
- Windows
- macOS
- Linux (BlueZ)

---

## Installation

From PyPI:

```bash
pip install PuffcoBLE
```

From source:

```bash
git clone https://github.com/Fr0st3h/PuffcoBLE.git
cd PuffcoBLE
pip install -e .
```

---

## Basic usage

```python
import asyncio
from puffcoble import PuffcoBLE

async def main():
    device = PuffcoBLE(device_name="DEV PUFFCO", debug=True)
    await device.connect()

    print("Device name:", await device.get_device_name())
    
    #get current profile info
    currentProfile = await device.get_current_profile_name()
    currentProfileTemp = await device.get_current_profile_temp()
    currentProfileDuration = await device.get_current_profile_duration()

    #start heat cycle
    await device.start_heat_cycle()

    #sleep for 3 seconds
    await asyncio.sleep(3)

    #cancel the heat cycle
    await device.stop_heat_cycle()

    #print the current profiles info
    print(f'Current Profile: {currentProfile}, Temperature: {currentProfileTemp}, Duration: {currentProfileDuration} seconds')

    payload = {'lamp': {'name': 'solid', 'param': {'color': ["#b700ff"]}}}


    #sets profile 4 colour
    await device.write_cbor_full("/u/app/hc/3/colr", payload)
    await device.disconnect()

asyncio.run(main())
```

---

## Connection and authentication

Authentication is handled automatically when calling `connect()`:

- BLE bonding trigger
- Access seed request
- Unlock key generation
- Lorax access unlock

Manual authentication is not required for normal usage.

---

## Reading data

Typed read:

```python
temp = await puffco.read(
    "/p/app/thc/temp",
    size=4,
    data_type="float32"
)
```

Raw bytes:

```python
data = await puffco.read("/p/sys/fw/ver", size=12)
```

Read full path (chunked):

```python
blob = await puffco.read_bytes_all("/p/app/thc/colr")
```

---

## Writing data

Write raw bytes:

```python
await puffco.write_short(
    "/u/app/ui/lbrt",
    0,
    0,
    bytes([80, 80, 80, 80])
)
```

Write typed values:

```python
await puffco.write(
    "/p/app/thc/time",
    45.0,
    data_type="float32"
)
```

---

## Heat cycle control

```python
await puffco.start_heat_cycle()
await puffco.boost_heat_cycle()
await puffco.stop_heat_cycle()
```

---

## Lantern mode

```python
await puffco.start_lantern()
await puffco.stop_lantern()
```

---

## Device information

```python
info = await puffco.get_device_info()
serial = await puffco.get_serial_number()
fw = await puffco.get_software_version()
uptime = await puffco.get_uptime()
```

---

## Debug logging

Enable debug output:

```python
PuffcoBLE(debug=True)
```

Logging uses `Tamga`.

---

## Notes

- This project is not affiliated with Puffco
- Firmware updates may break compatibility
- Use at your own risk

---

## License

MIT

---

## Contributing

Pull requests are welcome.  
If you add new Lorax paths or opcodes, please document them clearly.
