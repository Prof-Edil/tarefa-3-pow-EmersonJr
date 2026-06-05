import pandas as pd
import sys

data = pd.read_csv("../data/mempool.csv", header=None, names=["txid", "fee", "weight", "parent_txids"])

g=dict()
weights=dict()
parents=dict()
fee=dict()
deg=dict()
data["parent_txids"] = data["parent_txids"].apply(lambda x: list(x.split(';')) if not pd.isna(x) else [x])
for _, row in data.iterrows():
    g[row["txid"]]=[]   
    deg[row["txid"]]= len(row["parent_txids"]) if not pd.isna(row["parent_txids"][0]) else 0
    for p in row["parent_txids"]:
        if p not in g:
            g[p]=[row["txid"]]
        else:
            g[p].append(row["txid"])
    weights[row["txid"]]=row["weight"]
    fee[row["txid"]]=row["fee"]
    parents[row["txid"]]=row["parent_txids"]
ans = list()

acc = 4000000

start = "4c50e3dad7f98bceb6441f96b23748dea84fbdb7cedd603441e6ea4a574d04a6"
aux = [start]
while len(aux) > 0:
    txid = aux.pop()
    if aux.count(txid) > 0:
        continue
    if txid != start:
        ans.append(txid)
        acc -= weights[txid]
    if deg[txid] == 0:
        continue
    for parent in parents[txid]:
        aux.append(parent)
        

ans.reverse()

def greedy(txid, acc):
    
    pq = set()
    pq.add((-fee[txid], txid))

    while len(pq) > 0:
        
        w, txid = min(pq)
        pq.remove((w, txid))
        if(weights[txid] > acc):
            continue
        ans.append(txid)
        acc -= weights[txid]
        for child in g[txid]:
            deg[child]-=1
            if deg[child] == 0:
                pq.add((-fee[child], child))

for _, row in data.iterrows():
    if deg[row["txid"]] == 0 and row["txid"] != start:
        deg[row["txid"]]+=1
        g[start].append(row["txid"])
greedy(start, acc)

sys.stdout = open("../solutions/exercise01.txt", "w")
for txid in ans:
    print(txid)