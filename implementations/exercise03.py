import sys
import hashlib
from datetime import datetime, timezone

sys.stdout = open("../solutions/exercise03.txt", "w")
dt = datetime(2009, 1, 10, 12, 0, 0, tzinfo=timezone.utc)
timestamp = int(dt.timestamp())
merkle_root = bytes.fromhex("c7ecd2eb8d65ab0e2dd4acde31c37b5be16d25c6fbe8b1a3303abfab63808c38")
prev_block = bytes.fromhex("00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee")
version=(129).to_bytes(4, byteorder='little')
target=bytes.fromhex("00000000ffff0000000000000000000000000000000000000000000000000000")
prev_block=prev_block[::-1]
merkle_root=merkle_root[::-1]
nonce = 0
while True:
    nonce += 1
    block_header = version + prev_block + merkle_root + timestamp.to_bytes(4, byteorder='little') + nonce.to_bytes(8, byteorder='little')
    hash_result = hashlib.sha256(hashlib.sha256(block_header).digest()).digest()
    if int.from_bytes(hash_result, byteorder='big') <= int.from_bytes(target, byteorder='big'):
        print(hashlib.sha256(hashlib.sha256(block_header).digest()).digest()[::-1].hex())
        break