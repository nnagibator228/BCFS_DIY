from wallet import *
from block import *

class Miner:
    def __init__(self, acc): 
        self.acc = acc
        self.pub = acc.pub
        
    def mine(self, txs, prev_header, diff, reward, attempts=1000):
        txs.insert(0, self.coinbase(reward))
        mt = MerkleTree(txs)
        bh = Header(mt.root, prev_header.hash, prev_header.number+1, len(txs))
        bh.diff   = diff
        bh.reward = reward
        bh.miner  = self.pub
        bh.mined  = True
        bh_b = bytes(bh)
        nonce = 0
        for i in range(attempts):
            candidate   = bh_b + str(nonce).encode()
            candidate_h = sha(candidate)
            if candidate_h[2:2+diff] == '0'*diff: break
            nonce += 1
            assert nonce != attempts, 'no nonce could be found'
        bh.nonce  = nonce
        return Block(bh, txs)
        
    def coinbase(self, reward): 
        return self.acc.sign(TX(self.pub, self.pub, reward, 0, self.acc.nonce))
    

def mine_genesis(txs):
    mt  = MerkleTree(txs)
    bh  = Header(mt.root, '0x0', 0, len(txs))
    return Block(bh, txs)

def val_pow(mb):
    bh          = mb.header
    mb_b        = bytes(bh)
    candidate   = mb_b + str(bh.nonce).encode()
    candidate_h = sha(candidate)
    if candidate_h[2:2+bh.diff] == '0'*bh.diff: return True
    else                                      : return False
