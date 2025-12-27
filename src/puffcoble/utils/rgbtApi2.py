import ast

C32="0123456789ABCDEFGHJKMNPQRSTVWXYZ"

def _b(s:str):
    if not isinstance(s,str): return None
    if s.startswith('b""'): s='b"'+s[3:]
    return ast.literal_eval(s) if s.startswith('b"') and s.endswith('"') else None

_hex = lambda b: f"#{b[0]:02x}{b[1]:02x}{b[2]:02x}"

def _ulid16_to_str(b:bytes):
    n=int.from_bytes(b,"big"); bits=bin(n)[2:].zfill(128); bits="00"+bits
    return "".join(C32[int(bits[i:i+5],2)] for i in range(0,130,5))

def _x(o, parent=None, key=None):
    if isinstance(o,dict):
        return {k:_x(v,o,k) for k,v in o.items()}
    if isinstance(o,list):
        if key=="userColors":
            return [_hex(x) if isinstance(x,(bytes,bytearray)) and len(x)>=3 else _x(x) for x in o]
        return [_x(v,parent,None) for v in o]
    if isinstance(o,str):
        b=_b(o)
        return _x(b,parent,key) if b is not None else o
    if isinstance(o,(bytes,bytearray)):
        b=bytes(o)
        if key=="color":
            n = parent.get("colorLen") if isinstance(parent,dict) else None
            n = int(n) if isinstance(n,int) and n>0 else len(b)//3
            return [_hex(b[i*3:i*3+3]) for i in range(n) if len(b[i*3:i*3+3])==3]
        if isinstance(key,str) and key.endswith("Ulid") and len(b)==16:
            return _ulid16_to_str(b)
        if len(b)==3:
            return _hex(b)
    return o

def decode_puffco_json(payload: dict) -> dict:
    return _x(payload)