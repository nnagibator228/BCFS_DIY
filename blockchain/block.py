from transaction import *
from merkle import *
from wallet import *

class Header(Hashable):
    def __init__(self, root, prev_hash, number, n_txs):
        self.root      = root
        self.prev_hash = prev_hash
        self.number    = number
        self.n_txs     = n_txs
        self.mined     = False
        self.time      = time.ctime()


class Info(Hashable):
    def __init__(self, txs): 
        self.volume = sum([tx.value for tx in txs])
        self.fees   = sum([tx.fee   for tx in txs])


class Block(Hashable): 
    def __init__(self, bh, txs):
        self.info   = Info(txs)
        self.header = bh
        self.mt     = MerkleTree(txs)
        self.txs    = self.val_txs(txs)
        self.hash   = bh.hash
        
    def val_txs(self, txs):
        for tx in txs: assert val_sig(tx),       'tx signature invalid'
        assert self.are_unique(txs),             'txs include duplicates'
        assert self.mt.root == self.header.root, 'txs root hash do not match'
        return {tx.hash: tx for tx in txs}
    
    def json(self): 
        info = self.info.__dict__
        h    = self.header.__dict__
        txs  = [tx.json() for tx in self.txs.values()]
        d    = {**info, **h, 'txs': txs}
        return json.dumps(d, indent=4)
    
    def are_unique(self, txs): return len(set([tx.hash for tx in txs])) == len(txs)
    def __getitem__(self, key):return self.txs[key] 
    def __str__(self):         return (str(self.header)
                                       +'\n'+str(self.info)
                                       +'\n\ntxs:\n' 
                                       +'\n'.join(tx.smry() for tx in self.txs.values()))