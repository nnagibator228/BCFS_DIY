from hash import *
from typing import Union, Sequence

num = Union[int, float]


class TX(Hashable):
    def __init__(self, fr: Hash, to: Hash, value: num, fee: num, nonce: int):
        self.fr, self.to = fr, to
        self.value: float = float(value)
        self.fee: num     = fee
        self.nonce: int   = nonce
        self.time: str    = time.ctime()
        self.signed: bool = False

    def __setattr__(self, prop: Any, val: Any) -> None:
        super().__setattr__(prop, val)
        if prop == 'sig':
            self.signed = True

    def smry(self) -> str:
        return f'{mini_pretty_hash(self.fr)} -> {mini_pretty_hash(self.to)} {self.value} eth'


def load_tx(json_tx: str) -> TX:
    d = json.loads(json_tx)
    tx = TX(d['fr'], d['to'], d['value'], d['fee'], d['nonce'])
    for k, v in d:
        setattr(tx, k, v)
    tx.hash = d['hash']
    return tx


def txs2str(txs: Sequence[TX]) -> str:
    return '\n'.join([str(tx) + '\n' for tx in txs])
