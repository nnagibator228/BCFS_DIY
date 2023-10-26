import time, json
from hashlib import sha256

sha = lambda x: '0x'+sha256(str(x).encode()).hexdigest()

rh = lambda: sha(time.time())

def hash2emoji(h):
    if h[:2]!='0x': h='0x'+h
    offset  = int(h[0:4], 0)
    unicode = b'\U' + b'000' + str(hex(0x1F466+offset))[2:].encode()
    return unicode.decode('unicode_escape')

def ph(h):
    if len(h)<12: return h
    else        : return hash2emoji(h)+' '+h[:12] + '...' + h[-3:]

def pmh(h):
    if len(h)<6: return h
    else       : return hash2emoji(h)+' '+h[:6]


class Hashable:
    def __eq__(self, other): return self.hash == other.hash
    def __bytes__(self):     return self.hash.encode()
    def json(self): return json.dumps({**self.__dict__}, indent=4)
    
    def __setattr__(self, prop, val):
        super().__setattr__(prop, val)
        if prop not in ['sig','signed','hash','nonce']: 
                super().__setattr__('hash', sha(self.__dict__))
                
    def __str__(self):
        s = []
        for k,v in self.__dict__.items():
            p = f'{k}:'.ljust(15)
            if hasattr(v,'messageHash'): s.append(p+ph(v.messageHash.hex()))
            elif str(v)[:2]=='0x'      : s.append(p+ph(v))
            elif type(v)   ==float     : s.append(p+str(round(v,8))+' bbc')
            else                       : s.append(p+str(v))
        return '\n'.join(s)

def r_stxs(n): return [w1.signed_tx(w2,ri(1,9),ri(1,9)/100) for _ in range(n)]

def load_block(d):
    d  = json.loads(d)
    txs = []
    for tx in d['txs']: txs.append(load_tx(tx))
    bh = Header(d['root'],d['prev_hash'],d['number'],d['n_txs']) 
    for k,v in d.items(): setattr(bh, k, v)
    bh.hash = d['hash']
    b = Block(bh, txs)
    return b