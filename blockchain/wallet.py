import eth_account

from typing import Tuple

from transaction import *
from eth_account.messages import encode_defunct as encode_msg
import web3 as w3

w3 = w3.Account
LocalAccount = NewType('LocalAccount', eth_account.account.LocalAccount)


def keys() -> Tuple[str, Hash]:
    acc: LocalAccount = w3.create()
    return acc._private_key.hex(), acc.address


class Wallet(Hashable):
    def __init__(self) -> None:
        self.priv, self.pub = keys()
        self.nonce: int = 0

    def sign(self, tx: TX) -> TX:
        self.nonce += 1
        m: eth_account.messages.SignableMessage = encode_msg(bytes(tx))
        sig: 'SignedMessage' = w3.sign_message(m, self.priv)
        tx.sig = sig.signature.hex()
        return tx

    def signed_tx(self, to: 'Wallet', value: float, fee: float) -> TX:
        tx = TX(self.pub, to.pub, value, fee, self.nonce)
        return self.sign(tx)

    def __str__(self) -> str:
        return pretty_hash(self.pub)


def val_sig(tx: TX) -> bool:
    if not hasattr(tx, 'sig'):
        return False
    m = encode_msg(bytes(tx))
    return w3.recover_message(m, signature=tx.sig) == tx.fr
