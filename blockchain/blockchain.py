from block import *
from mine import *

class AccountState:
    def __init__(self): self.balance,self.nonce = 0,0
    def inc_nonce  (self):        self.nonce   += 1
    def add_balance(self, value): self.balance += value
    def sub_balance(self, value): self.balance -= value
    def json(self): return json.dumps(self.__dict__)
    def __str__(self): return f'balance: {self.balance}\nnonce: {self.nonce}'


class State:
    def __init__(self): self.state={}
    def new   (self, pub): self.state[pub] = AccountState()
    def is_new(self, pub): return pub not in self.state
    def add(self, pubs):
        for pub in pubs:
            if self.is_new(pub): self.new(pub)
    
    def init(self, gb):
        gh = gb.header
        assert gh.number    == 0
        assert gh.prev_hash == '0x0'
        for tx in gb.txs.values():
            self.add([tx.fr, tx.to])
            assert val_sig(tx)
            self.state[tx.fr].inc_nonce()
            self.state[tx.to].add_balance(tx.value)
        
    def apply(self, tx, miner):
        self.add([tx.fr,tx.to,miner])
        if tx.fr != tx.to: 
            assert val_sig(tx)
            assert self.state[tx.fr].nonce  == tx.nonce
            assert self.state[tx.fr].balance - tx.value > 0
        else: 
            assert tx.fr == tx.to == miner
        self.state[tx.fr].inc_nonce()
        self.state[tx.fr].sub_balance(tx.value)
        self.state[tx.to].add_balance(tx.value)
        self.state[miner].add_balance(tx.fee)
        return True
    
    def apply_reward(self, miner, reward):
        self.state[miner].add_balance(reward)
    
    def __getitem__(self, key): return self.state[key] 
    def __str__(self):
        return '\n'.join(f'{ph(k)}\n{v}\n' for k,v in self.state.items())
    

class Blockchain:
    def __init__(self, gb):
        self.state  = State()
        self.blocks = []
        self.state.init(gb)
        self.blocks.append(gb)

    def candidate(self, txs):
        mt = MerkleTree(txs)
        bh = Header(mt.root, self.blocks[-1].hash, len(self.blocks), len(txs))
        return Block(bh, txs)
        
    def add(self, mb):
        assert self.val(mb)
        for tx in mb.txs.values(): assert self.state.apply(tx, mb.header.miner)
        self.state.apply_reward(mb.header.miner, mb.header.reward)
        self.blocks.append(mb)
        return True
    
    def val(self, mb):
        bh = mb.header
        assert val_pow(mb)
        assert bh.number == len(self.blocks)
        if len(self.blocks) > 0: assert self.blocks[-1].hash == bh.prev_hash
        return True
    
    def __getitem__(self, key): return self.state.__getitem__(key)
    def __str__(self): 
        return (('\n'*2+'--'*20+'\n'*2).join(f'{str(block)}' for block in self.blocks)
                +'\n'*2+'-'*6+'\nstate:\n'+'-'*6
                +'\n'+str(self.state))