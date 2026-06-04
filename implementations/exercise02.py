import sys
import hashlib

sys.stdin = open("../data/ex02_txid_list.txt", "r")
sys.stdout = open("../solutions/exercise02.txt", "w")
txids = sys.stdin.read().splitlines()

parent = dict()
son = dict()
lvl = [hashlib.sha256(txid.encode()).hexdigest() for txid in txids]

while len(lvl) > 1:
    nxLvl = []
    for i in range(0, len(lvl), 2):
        if i+1 == len(lvl):
            lvl.append(lvl[i])
        pai = hashlib.sha256((lvl[i] + lvl[i+1]).encode()).hexdigest()
        parent[lvl[i]] = pai
        parent[lvl[i+1]] = pai
        nxLvl.append(pai)
        son[pai] = [lvl[i], lvl[i+1]]
    lvl = nxLvl

start = "49ff8cccf1ca12179e9ae7a4760f550b5a18401b27e1e057604e27c3e10c08fb"
start = hashlib.sha256(start.encode()).hexdigest()
ans = []
while start in parent:
    ans.append(start)
    start = parent[start]
ans.reverse()
for txid in ans:
    print(txid)