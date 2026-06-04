import pandas as pd
import sys

data = pd.read_csv("../data/mempool.csv")

g=dict()
weights=dict()
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
ans = list()

acc = 50000
def greedy(txid, acc):
    
    pq = set()
    pq.add((weights[txid], txid))

    while len(pq) > 0:
        
        w, txid = min(pq)
        pq.remove((w, txid))
        if(fee[txid] > acc):
            continue
        ans.append(txid)
        acc -= fee[txid]
        for child in g[txid]:
            deg[child]-=1
            if deg[child] == 0:
                pq.add((weights[child], child))

start = "4c50e3dad7f98bceb6441f96b23748dea84fbdb7cedd603441e6ea4a574d04a6"
for _, row in data.iterrows():
    if deg[row["txid"]] == 0 and row["txid"] != start:
        deg[row["txid"]]+=1
        g[start].append(row["txid"])
greedy(start, acc)

sys.stdout = open("../solutions/exercise01.txt", "w")
for txid in ans:
    print(txid)