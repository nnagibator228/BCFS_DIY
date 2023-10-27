from typing import List, Sequence, Dict
from transaction import TX
from hash import *
from random import randint as ri


def random_txs(n: int) -> List[TX]:
    return [TX(rh(), rh(), ri(1, 9), ri(1, 9) / 10, 0) for _ in range(n)]


class MerkleTree:
    def __init__(self, txs: Sequence[TX]):
        self.mt: Dict[str, List[Hash]] = {}
        leafs: List[Hash] = [tx.hash for tx in txs]
        if len(leafs) % 2 != 0:
            leafs.append(sha('0x0'))
        self.mt['1'] = leafs
        self.merkle(leafs)

    def merkle(self, leafs: List[Hash]) -> None:
        parents: List[str] = []
        while len(leafs) > 1:
            for i in range(0, len(leafs), 2):
                leaf = leafs[i]
                if i + 1 >= len(leafs):
                    r = '0x0'
                else:
                    r = leafs[i + 1]
                parents.append(sha(leaf + r))
            leafs = parents
            self.mt[f'{len(self) + 1}'] = parents
            parents = []

    @property
    def root(self) -> Hash:
        return self.mt[str(len(self))][0]

    def __eq__(self, o: 'MerkleTree') -> bool:
        return self.root == o.root

    def __len__(self) -> int:
        return len(self.mt)

    def __getitem__(self, k) -> List[Hash]:
        return self.mt[str(k)]

    def __str__(self) -> str:
        s = ''
        for k, v in self.mt:
            s += f'height {k}'
            for h in v:
                s += f'\n {pretty_hash(h)}'
            s += '\n'
        return s


def proof(mt: MerkleTree, mb: List[int], tx: TX) -> bool:
    if mb[0] % 2 != 0:
        cn = sha(tx.hash + mt[1][mb[0]])
    else:
        cn = sha(mt[1][mb[0]] + tx.hash)
    for i in range(2, len(mt)):
        if mb[i - 1] % 2 != 0:
            cn = sha(cn + mt[i][mb[i - 1]])
        else:
            cn = sha(mt[i][mb[i - 1]] + cn)
    return cn == mt.root


# This function is not used anywhere, so I commented it
# def r_stxs(n): return [w1.signed_tx(w2, ri(1, 9), ri(1, 9) / 100) for _ in range(n)]

