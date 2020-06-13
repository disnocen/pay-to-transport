from typing import Tuple, Optional, Any
import hashlib
import binascii
import base58check

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

Point = Tuple[int, int]

def hash160(hex_str) -> str:
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(hex_str.encode())
    rip.update( sha.digest() )
    return rip.hexdigest()

def create_hash_from_string(data: str) -> str:
   return hashlib.sha256(data.encode('utf-8')).hexdigest() 

def secr_key_from_hash(hash: str) -> int:
    return (int(hash,16)%p)

def secr_key_from_string(data: str) -> int:
    return secr_key_from_hash(create_hash_from_string(data))

def non_redeemable_tx(customer_addr,merchant_addr,amount):
    """the non redeemable transaction from the customer to the merchant to pay
    for the transportation costs"""
    print("amount:","\t",amount,"\n","from:","\t",customer_addr,'to:','\t',merchant_addr)



def bytes_from_int(x: int) -> bytes:
    return x.to_bytes(32, byteorder="big")

def bytes_from_point(P: Point) -> bytes:
    return bytes_from_int(x(P))

def x(P: Point) -> int:
    return P[0]

def y(P: Point) -> int:
    return P[1]

def point_add(P1: Optional[Point], P2: Optional[Point]) -> Optional[Point]:
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    if (x(P1) == x(P2)) and (y(P1) != y(P2)):
        return None
    if P1 == P2:
        lam = (3 * x(P1) * x(P1) * pow(2 * y(P1), p - 2, p)) % p
    else:
        lam = ((y(P2) - y(P1)) * pow(x(P2) - x(P1), p - 2, p)) % p
    x3 = (lam * lam - x(P1) - x(P2)) % p
    return (x3, (lam * (x(P1) - x3) - y(P1)) % p)

def point_mul(P: Optional[Point], n: int) -> Optional[Point]:
    R = None
    for i in range(256):
        if (n >> i) & 1:
            R = point_add(R, P)
        P = point_add(P, P)
    return R

def pubkey_gen(seckey: int) -> bytes:
    P = point_mul(G, seckey)
    assert P is not None
    return bytes_from_point(P)

def hex_to_p2pkh(pubkey: str, testnet=True) -> str:
    #bytes_key=bytes.fromhex(pubkey)
    if testnet:
        version = '6f' # 111
    else:
        version = '00'
    key_hash = version + hash160(pubkey)
    checksum = create_hash_from_string(create_hash_from_string(key_hash))[0:8]
    cat=key_hash+checksum
    return base58check.b58encode(bytes.fromhex(cat)).decode()

def seckey_to_wif(seckey: str, testnet=True):
    if testnet:
        version = 'ef'
    else:
        version = '80'
    seckey=version+seckey
    checksum = create_hash_from_string(create_hash_from_string(seckey))[0:8]
    cat=seckey+checksum
    return base58check.b58encode(bytes.fromhex(cat)).decode()
    
def days_to_blocks(days: int) -> int:
    # there are 6 blocks per hour on average in Bitcoin
    # therefore there are 6*24=144 blocks per day
    return days*144
    
