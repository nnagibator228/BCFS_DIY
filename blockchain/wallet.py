from transaction import *
from eth_account.messages import encode_defunct as encode_msg
import web3 as w3; w3 = w3.Account

def keys():
    acc = w3.create()
    return acc.privateKey.hex(), acc.address


class Wallet:
    def __init__(self): 
        self.priv, self.pub = keys()
        self.nonce = 0
        
    def sign(self, tx):
        self.nonce += 1
        m = encode_msg(bytes(tx))
        sig = w3.sign_message(m, self.priv)
        tx.sig = sig.signature.hex()
        return tx
            
    def signed_tx(self, to, value, fee):
        tx = TX(self.pub, to.pub, value, fee, self.nonce)
        return self.sign(tx)
    
    def __str__(self): return ph(self.pub)

def val_sig(tx):
    if not hasattr(tx, 'sig'): return False
    m = encode_msg(bytes(tx))
    return w3.recover_message(m, signature=tx.sig) == tx.fr
