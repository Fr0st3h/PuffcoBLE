"""Puffco BLE communication module."""

import asyncio
import os
import struct
import sys
from base64 import b64decode
from hashlib import sha256
from sys import platform
from typing import Any, Literal, Optional, Union

import cbor2
from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from tamga import Tamga

from puffcoble.puffco.constants import LoraxOpCodes, LoraxService, UnlockKeys, BatteryChargeState, ModeCommands, OperatingState
from puffcoble.utils.codec import hexify
from puffcoble.utils.product_info import get_product_info
from puffcoble.utils.rgbtApi2 import decode_puffco_json
from puffcoble.utils.utils import PuffcoUtils

if platform.startswith("win32") and sys.version_info >= (3, 8):
    os.environ["PATH"] += os.pathsep + os.path.dirname(__file__)

_STRUCT_FORMATS = {
    "int8": "b",
    "uint8": "B",
    "int16": "h",
    "uint16": "H",
    "int32": "i",
    "uint32": "I",
    "int64": "q",
    "uint64": "Q",
    "float32": "f",
    "float64": "d",
    "bool": "?",
}

DataType = Literal[
    "int8", "uint8", "int16", "uint16", "int32", "uint32",
    "int64", "uint64", "float32", "float64", "bool", "bytes"
]


class PuffcoBLE:
    def __init__(
        self,
        device_name: Optional[str] = None,
        device_mac: Optional[str] = None,
        debug: bool = False
    ):
        self.device_name = device_name
        self.device_mac = device_mac
        self.debug = debug
        self.logger = Tamga()
        self.lorax_sequence = 0
        self.client: Optional[BleakClient] = None

    def debug_print(self, message: str) -> None:
        if self.debug:
            self.logger.debug(message)

    async def search_for_device(self) -> Optional[BLEDevice]:
        if not self.device_mac and not self.device_name:
            raise ValueError("Either device_name or device_mac is required")

        self.debug_print("Scanning for devices...")
        devices = await BleakScanner.discover()

        for device in devices:
            if self.device_name and self.device_name in (device.name or ""):
                return device
            if self.device_mac and self.device_mac.lower() == (device.address or "").lower():
                return device

        return None

    async def connect(self) -> BleakClient:
        device = await self.search_for_device()
        if not device:
            raise RuntimeError("Device not found")

        self.debug_print(f"Connecting to {device.name} ({device.address})")
        client = BleakClient(device)

        if not await client.connect():
            raise ConnectionError("Failed to connect to device")

        self.client = client
        await self.trigger_bonding()
        await self.auth_device()
        return client

    async def disconnect(self) -> None:
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            self.debug_print("Disconnected from device")

    async def trigger_bonding(self) -> bool:
        if not self.client:
            raise RuntimeError("Client not connected")
        await self.client.read_gatt_char(LoraxService.VERSION_CHAR)
        return True

    async def run_command(
        self,
        opcode: int,
        body: bytes = b"",
        max_reply_len: int = 512,
        exact_reply_len: bool = False,
        timeout: float = 3.0,
        log_msg: str = ""
    ) -> bytes:
        if not self.client:
            raise RuntimeError("Client not connected")

        seq = self.lorax_sequence & 0xFFFF
        self.lorax_sequence += 1

        header = struct.pack("<HB", seq, opcode)
        msg = header + body
        self.debug_print(f"→ seq {seq:04X} {log_msg}")

        fut = asyncio.get_event_loop().create_future()

        def handler(_characteristic, data: bytes):
            reply_seq = struct.unpack_from("<H", data)[0]
            if reply_seq != seq:
                return

            payload = data[3:]
            if exact_reply_len and len(payload) != max_reply_len:
                fut.set_exception(
                    Exception(f"Reply length {len(payload)} != expected {max_reply_len}")
                )
            else:
                fut.set_result(payload)

        await self.client.start_notify(LoraxService.REPLY_CHAR, handler)
        await self.client.write_gatt_char(LoraxService.COMMAND_CHAR, msg, response=False)

        try:
            reply = await asyncio.wait_for(fut, timeout=timeout)
            self.debug_print(f"← seq {seq:04X} reply ({len(reply)} bytes)")
            return reply
        finally:
            await self.client.stop_notify(LoraxService.REPLY_CHAR)

    async def read(
        self,
        path: str,
        offset: int = 0,
        size: Optional[int] = None,
        data_type: DataType = "bytes",
        count: int = 1
    ) -> Union[float, int, bool, bytes, list[Union[float, int, bool]]]:
        if data_type == "bytes":
            if size is None:
                raise ValueError("size is required when data_type='bytes'")
            fmt = None
            elem_size = None
        else:
            base_format = _STRUCT_FORMATS.get(data_type)
            if not base_format:
                raise ValueError(f"Unsupported data_type: {data_type}")

            fmt = f"<{count}{base_format}"
            elem_size = struct.calcsize(f"<{base_format}")
            required_size = elem_size * max(1, count)

            size = required_size if size is None else size
            if size < required_size:
                raise ValueError(
                    f"size {size} is too small for {count} {data_type} elements "
                    f"(need {required_size} bytes)"
                )

        body = struct.pack("<HH", offset, size) + path.encode("utf-8")
        result = await self.run_command(
            LoraxOpCodes.READ_SHORT,
            body,
            size,
            False,
            3.0,
            f"Read {path} ({size} bytes @ offset {offset})"
        )
        self.debug_print(f"Read {path}: {result.hex()} @ offset {offset}")

        if data_type == "bytes":
            return result

        data = result[:elem_size * max(1, count)]
        values = struct.unpack(fmt, data)
        return values[0] if count == 1 else list(values)

    async def read_short(self, path: str, offset: int, size: int) -> bytes:
        body = struct.pack("<HH", offset, size) + path.encode("utf-8")
        result = await self.run_command(
            LoraxOpCodes.READ_SHORT,
            body,
            size,
            False,
            3.0,
            f"ReadShort {path} ({size} bytes @ offset {offset})"
        )
        self.debug_print(f"ReadShort {path}: {result.hex()} @ offset {offset}")
        return result

    async def write_short(
        self,
        path: str,
        offset: int,
        flags: int,
        value_bytes: bytes
    ) -> None:
        body = (
            struct.pack("<HB", offset, flags)
            + path.encode("utf-8")
            + b"\x00"
            + bytes(value_bytes)
        )
        result = await self.run_command(
            LoraxOpCodes.WRITE_SHORT,
            body,
            0,
            True,
            3.0,
            f"WriteShort {path} (flags={flags}, data={value_bytes.hex()})"
        )
        if result:
            raise Exception(f"Unexpected write response: {result.hex()}")

    async def write(
        self,
        path: str,
        value: Union[int, float, bool, bytes],
        offset: int = 0,
        flags: int = 0,
        data_type: DataType = "bytes"
    ) -> None:
        if data_type == "bytes":
            if not isinstance(value, bytes):
                raise ValueError("value must be bytes when data_type='bytes'")
            value_bytes = value
        else:
            base_format = _STRUCT_FORMATS.get(data_type)
            if not base_format:
                raise ValueError(f"Unsupported data_type: {data_type}")
            value_bytes = struct.pack(f"<{base_format}", value)

        await self.write_short(path, offset, flags, value_bytes)

    async def auth_device(self) -> bool:
        seed = await self.read_access_seed_key()
        key = self._make_key(seed, bytearray(b64decode(UnlockKeys.LORAX_KEY)))
        await self.unlock_access(key)
        return True

    async def unlock_access(self, key: bytes) -> bytes:
        return await self.run_command(
            LoraxOpCodes.UNLOCK_ACCESS,
            key,
            0,
            True,
            3.0,
            "UnlockAccess"
        )

    async def read_access_seed_key(self) -> list[int]:
        result = await self.run_command(
            LoraxOpCodes.GET_ACCESS_SEED,
            b"",
            16,
            True,
            3.0,
            "GetAccessSeed"
        )
        return list(result)

    def _make_key(self, access_seed: list[int], handshake_key: bytearray) -> bytearray:
        buf = bytearray(32)
        for i in range(16):
            buf[i] = handshake_key[i]
            buf[i + 16] = access_seed[i]

        h = sha256(buf).hexdigest()
        return bytearray(int(h[i:i+2], 16) for i in range(0, 32, 2))

    async def read_bytes_all(
        self,
        path: str,
        *,
        chunk_size: int = 125,
        max_len: Optional[int] = None
    ) -> bytes:
        out = bytearray()
        idx = 0
        cap = 1_048_576

        while True:
            req = chunk_size if max_len is None else min(chunk_size, max_len - len(out))
            if req <= 0:
                break

            chunk = await self.read(path, idx, req, data_type="bytes")
            if not chunk:
                break

            out.extend(chunk)
            idx += len(chunk)

            if len(chunk) < req:
                break
            if max_len is not None and len(out) >= max_len:
                break
            if len(out) >= cap:
                raise RuntimeError(f"read_bytes_all exceeded cap of {cap} bytes")

        return bytes(out)

    async def write_cbor_full(self, path: str, obj: dict, chunk: int = 80) -> None:
        blob = cbor2.dumps(hexify(obj), canonical=True)
        offset = 0

        while offset < len(blob):
            piece = blob[offset:offset + chunk]
            await self.write_short(path, offset, 0, piece)
            offset += len(piece)

    async def _read_and_decode(self, path: str) -> str:
        raw = await self.read_short(path, 0, 125)
        return bytes(raw).decode(errors="ignore").rstrip('\x00')


    async def get_device_info(self) -> dict[str, Any]:
        mdcd = await self.read("/p/sys/hw/mdcd", 0, 4, "uint32")
        return get_product_info(model_code=mdcd)

    async def get_serial_number(self) -> str:
        return await self._read_and_decode("/p/sys/hw/ser")

    async def get_device_name(self) -> str:
        return await self._read_and_decode("/u/sys/name")

    async def get_software_version(self) -> str:
        data = await self.read_short("/p/sys/fw/ver", 0, 125)
        return PuffcoUtils.revision_number_to_string(data[0])

    async def get_bootloader_version(self) -> str:
        data = await self.read("/p/sys/fw/bver", 0, 12, "uint8")
        return PuffcoUtils.revision_number_to_string(data[0])

    async def get_uptime(self) -> list[int]:
        return list(await self.read_short("/p/sys/uptm", 0, 125))

    async def get_battery_charge_state(self) -> dict[str, Union[int, str]]:
        data = await self.read_short("/p/bat/chg/stat", 0, 125)
        state = BatteryChargeState(data[0])
        return {"value": state.value, "name": state.name}

    async def get_battery_level(self) -> int:
        return int(await self.read("/p/bat/cap", 0, 4, "float32"))

    async def get_current_profile_name(self) -> str:
        return await self._read_and_decode("/p/app/thc/name")

    async def get_current_profile_temp(self) -> int:
        temp_c = await self.read("/p/app/thc/temp", 0, 4, "float32")
        return int(round(temp_c * 9 / 5 + 32, 0))

    async def get_current_profile_duration(self) -> int:
        return int(await self.read("/p/app/thc/time", 0, 4, "float32"))

    async def get_current_profile_colour(self) -> Any:
        raw = await self.read_bytes_all("/p/app/thc/colr")
        decoded = cbor2.loads(raw)
        return decode_puffco_json(decoded)

    async def get_operating_state(self) -> OperatingState:
        data = await self.read_short("/p/app/stat/id", 0, 125)
        return OperatingState(data[0])

    async def get_approx_dabs_remaining(self) -> int:
        return int(await self.read("/p/app/info/drem", 0, 12, "float32"))

    async def get_dabs_per_day(self) -> int:
        return int(await self.read("/p/app/info/dpd", 0, 12, "float32"))

    async def get_total_dabs(self) -> int:
        return int(await self.read("/p/app/info/dtot", 0, 4, "uint32"))

    async def send_mode_command(self, command: ModeCommands) -> None:
        await self.write_short("/p/app/mc", 0, 0, bytes([command]))

    async def start_heat_cycle(self) -> None:
        await self.send_mode_command(ModeCommands.HEAT_CYCLE_START)

    async def stop_heat_cycle(self) -> None:
        await self.send_mode_command(ModeCommands.HEAT_CYCLE_ABORT)

    async def boost_heat_cycle(self) -> None:
        await self.send_mode_command(ModeCommands.HEAT_CYCLE_BOOST)

    async def start_lantern(self) -> None:
        await self.write_short("/p/app/ltrn/cmd", 0, 0, bytes([1]))

    async def stop_lantern(self) -> None:
        await self.write_short("/p/app/ltrn/cmd", 0, 0, bytes([0]))

    async def set_led_brightness(
        self,
        base: int,
        mid: int,
        glass: int,
        logo: int
    ) -> None:
        await self.write_short(
            "/u/app/ui/lbrt",
            0,
            0,
            bytes([base, mid, glass, logo])
        )

    async def show_battery_level(self) -> None:
        await self.send_mode_command(ModeCommands.SHOW_BATTERY_LEVEL)

    async def show_version(self) -> None:
        await self.send_mode_command(ModeCommands.SHOW_VERSION)

    async def enter_sleep_mode(self) -> None:
        await self.send_mode_command(ModeCommands.SLEEP)

    async def power_off(self) -> None:
        await self.send_mode_command(ModeCommands.MASTER_OFF)