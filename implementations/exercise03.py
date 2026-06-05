import sys
import hashlib
from datetime import datetime, timezone

sys.stdout = open("../solutions/exercise03.txt", "w")
dt = datetime(2009, 1, 10, 12, 0, 0, tzinfo=timezone.utc)
timestamp = int(dt.timestamp())
merkle_root = bytes.fromhex("c0a692de10b69e2381a2856dcb0d0736dcd307bf25af7ce74831bf25793de626")
prev_block = bytes.fromhex("00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee")
version=(129).to_bytes(4, byteorder='little')
target=bytes.fromhex("00000000ffff0000000000000000000000000000000000000000000000000000")
nonce = 0  
while True:
    nonce += 1
    block_header = version + prev_block + merkle_root + timestamp.to_bytes(4, byteorder='big') + nonce.to_bytes(8, byteorder='little')
    hash_result = hashlib.sha256(block_header).digest()
    if int.from_bytes(hash_result, byteorder='big') <= int.from_bytes(target, byteorder='big'):
        print(block_header.hex())
        break