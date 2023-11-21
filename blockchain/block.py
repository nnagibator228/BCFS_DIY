from merkle import *
from wallet import *


class Header(Hashable):
    def __init__(self, root: Hash, prev_hash: Hash, number: num, n_txs: int) -> None:
        self.root: Hash = root
        self.prev_hash: Hash = prev_hash
        self.number: num = number
        self.n_txs: int = n_txs
        self.mined: bool = False
        self.time: str = time.ctime()


class Info(Hashable):
    def __init__(self, txs: Sequence[TX]) -> None:
        self.volume: float = sum([tx.value for tx in txs])
        self.fees: float = sum([tx.fee for tx in txs])


class Block(Hashable):
    def __init__(self, bh: Header, txs: Sequence[TX]) -> None:
        self.info: Info = Info(txs)
        self.header: Header = bh
        self.mt: MerkleTree = MerkleTree(txs)
        self.txs = self.val_txs(txs)
        self.hash: Hash = bh.hash

    def val_txs(self, txs: Sequence[TX]) -> Dict[str, TX]:
        for tx in txs:
            assert val_sig(tx), 'tx signature invalid'
        assert self.are_unique(txs), 'txs include duplicates'
        assert self.mt.root == self.header.root, 'txs root hash do not match'
        return {tx.hash: tx for tx in txs}

    def json(self) -> str:
        info: Dict[str, Any] = self.info.__dict__
        h: Dict[str, Any] = self.header.__dict__
        json_txs: List[str] = [tx.json() for tx in self.txs.values()]
        d = {**info, **h, 'txs': json_txs}
        return d

    def are_unique(self, txs: Sequence[TX]) -> bool:
        return len(set([tx.hash for tx in txs])) == len(txs)

    def __getitem__(self, key) -> TX:
        return self.txs[key]

    def __str__(self) -> str:
        return (str(self.header)
                + '\n' + str(self.info)
                + '\n\ntxs:\n'
                + '\n'.join(tx.smry() for tx in self.txs.values()))


def load_block(json_block: str) -> Block:
    d = json.loads(json_block)
    txs = []

    for tx in d['txs']:
        txs.append(load_tx(tx))

    bh = Header(d['root'], d['prev_hash'], d['number'], d['n_txs'])
    for k, v in d:
        setattr(bh, k, v)
    bh.hash = d['hash']
    b = Block(bh, txs)
    return b
