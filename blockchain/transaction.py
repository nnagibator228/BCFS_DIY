from hash import *
from copy import deepcopy

class TX(Hashable): 
    def __init__(self, fr, to, value, fee, nonce): 
        self.fr, self.to = fr, to
        self.value       = float(value)
        self.fee         = fee
        self.nonce       = nonce
        self.time        = time.ctime()
        self.signed      = False
        
    def __setattr__(self, prop, val):
        super().__setattr__(prop, val)
        if prop == 'sig': self.signed = True
    
    def smry(self): return f'{pmh(self.fr)} -> {pmh(self.to)} {self.value} eth'


def load_tx(d):
    d = json.loads(d)
    tx = TX(d['fr'],d['to'],d['value'],d['fee'],d['nonce'])
    for k,v in d.items(): setattr(tx, k, v)
    tx.hash = d['hash']
    return tx

def txs2str(txs): return '\n'.join([str(tx)+'\n' for tx in txs])