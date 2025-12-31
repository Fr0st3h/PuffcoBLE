from enum import IntEnum

class PikachuService:
    UUID = '06caf9c0-74d3-454f-9be9-e30cd999c17a'
    CHARACTERISTIC_BASE = 'f9a98c15-c651-4f34-b656-d100bf58'


class LoraxService:
    UUID = 'e276967f-ea8a-478a-a92e-d78f5dd15dd5'
    VERSION_CHAR = '05434bca-cc7f-4ef6-bbb3-b1c520b9800c'
    COMMAND_CHAR = '60133d5c-5727-4f2c-9697-d842c5292a3c'
    REPLY_CHAR = '8dc5ec05-8f7d-45ad-99db-3fbde65dbd9c'
    EVENT_CHAR = '43312cd1-7d34-46ce-a7d3-0a98fd9b4cb8'


class PupService:
    UUID = '420b9b40-457d-4abe-a3bf-71609d79581b'
    TRIGGER_CHAR = 'c830ee3e-0e32-4780-a51d-b1b0b38089a4'
    APP_VERSION_CHAR = '58b0a7aa-d89f-4bf2-961d-0d892d7439d8'
    APP_HASH_CHAR = '4daad5ae-8a9e-417d-924d-b237ac64ad9c'
    DEVICE_INFO_CHAR = '2dab0217-8a4e-4de8-83c7-8fded59f4599'
    SERIAL_NUMBER_CHAR = 'a5fa5a5d-f28e-47d9-b95b-f82c06177503'
    GENERAL_COMMAND_CHAR = 'c364cf1d-117f-4a3b-baae-3e2fce5a248f'
    GENERAL_COMMAND_RESPONSE_CHAR = 'baeb965b-58ac-43bf-9cc5-bfb448ec2e72'
    BOOTLOADER_VERSION_CHAR = '0d7ec9f3-efe4-4e51-aea0-3a1477a9c37e'
    BOOTLOADER_HASH_CHAR = '5c03d675-2588-490f-87dc-b88772934bbb'


class SilabsOtaService:
    UUID = '1d14d6ee-fd63-4fa1-bfa4-8f47b42119f0'
    CONTROL_CHAR = 'f7bf3564-fb6d-4e53-88a4-5e37e0326063'
    DATA_CHAR = '984227f3-34fc-4045-a5d0-2c581f81a153'
    APP_VERSION_CHAR = '0d77cc11-4ac1-49f2-bfa9-cd96ac7a92f8'
    LOADER_VERSION_CHAR = '4cc07bcf-0868-4b32-9dad-ba4cc41e5316'

class LoraxOpCodes(IntEnum):
    GET_ACCESS_SEED = 0x00
    UNLOCK_ACCESS = 0x01
    GET_LIMITS = 0x02
    ACK_EVENTS = 0x03
    READ_SHORT = 0x10
    WRITE_SHORT = 0x11
    STAT_SHORT = 0x12
    UNLINK = 0x13
    FILE_OPEN = 0x20
    FILE_READ = 0x21
    FILE_WRITE = 0x22
    FILE_WATCH = 0x23
    FILE_UNWATCH = 0x24
    FILE_STAT = 0x25
    FILE_CLOSE = 0x26
    PRUNE_FILE_HANDLES = 0x27

class UnlockKeys:
    FLAT_A_KEY = 8469038
    FLAT_X_KEY = 'FUrZc0WilhUBteT2JlCc+A=='
    LORAX_KEY = 'ZMZFYlbyb1scoSc3pd1x+w=='

class ModeCommands(IntEnum):
    MASTER_OFF = 0
    SLEEP = 1
    IDLE = 2
    TEMP_SELECTION_BEGIN = 3
    TEMP_SELECTION_END = 4
    SHOW_BATTERY_LEVEL = 5
    SHOW_VERSION = 6
    HEAT_CYCLE_START = 7
    HEAT_CYCLE_ABORT = 8
    HEAT_CYCLE_BOOST = 9
    FACTORY_TEST = 10
    BONDING = 11


class OperatingState(IntEnum):
    INIT_MEMORY = 0
    INIT_VERSION_DISP = 1
    INIT_BATTERY_DISP = 2
    MASTER_OFF = 3
    SLEEP = 4
    IDLE = 5
    TEMP_SELECT = 6
    HEAT_CYCLE_PREHEAT = 7
    HEAT_CYCLE_ACTIVE = 8
    HEAT_CYCLE_FADE = 9
    VERSION_DISP = 10
    BATTERY_DISP = 11
    FACTORY_TEST = 12
    BLE_BONDING = 13

class BatteryChargeSource(IntEnum):
    USB = 0
    GENERIC_QI = 1
    POWER_DOCK = 2
    NONE = 3


class BatteryChargeState(IntEnum):
    BULK = 0
    TOPUP = 1
    FULL = 2
    TEMP_STOP = 3
    DONE_DISCONNECTED = 4

class ChamberType(IntEnum):
    NONE = 0
    CLASSIC = 1
    XL = 2
    THREE_D = 3

class AnimationCode(IntEnum):
    PRESERVE = 0
    ALL_ON = 1
    ALL_OFF = 2
    BONDING_SUCCESSFUL = 3
    CONNECT_SUCCESSFUL = 4
    BREATHING = 5
    RISING = 6
    CIRCLING = 7
    HEAT_CYCLE_ACTIVE = 8
    TEMP_SELECT = 9
    CHARGE_START = 10
    CHARGING = 11
    CHARGING_LOW = 12
    IDLE_WAKEUP = 13
    IDLE_TO_OFF = 14
    HEAT_CYCLE_FADE = 15
    STEALTH_ENGAGE = 16
    STEALTH_DISENGAGE = 17
    LOGO_ONLY = 18
    FACTORY_RESET = 19
    BONDING = 20
    USER0 = 240
    USER1 = 241
    USER2 = 242
    USER3 = 243
    USER0_TO_1 = 244
    USER2_TO_3 = 245
    USER0_TO_3 = 246
    USER4 = 247
    USER5 = 248
    USER4_TO_5 = 249