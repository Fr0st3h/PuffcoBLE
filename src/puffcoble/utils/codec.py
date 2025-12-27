import re

HEX6 = re.compile(r"#?([0-9a-fA-F]{6})$")

def ulid26_to_16(u: str) -> bytes:
    a = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
    m = {ch: i for i, ch in enumerate(a)}
    for k in "iIlL": m[k] = m["1"]
    for k in "oO":   m[k] = m["0"]
    v = 0
    for ch in u:
        v = (v << 5) | m[ch]
    v &= (1 << 128) - 1
    return v.to_bytes(16, "big")

def hexify(o, key=None):
    if isinstance(o, dict):
        return {k: hexify(v, k) for k, v in o.items()}
    if isinstance(o, list):
        if key == "color":
            return b"".join(bytes.fromhex(HEX6.fullmatch(x).group(1)) for x in o)
        if key == "userColors":
            return [bytes.fromhex(HEX6.fullmatch(x).group(1)) for x in o]
        return [hexify(v) for v in o]
    if isinstance(o, str):
        if key and key.endswith("Ulid") and len(o) == 26:
            return ulid26_to_16(o)
        m = HEX6.fullmatch(o)
        return bytes.fromhex(m.group(1)) if m else o
    return o
