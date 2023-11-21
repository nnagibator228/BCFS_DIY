import time, json
from typing import Any, NewType
from hashlib import sha256

Hash = NewType('Hash', str)


def sha(x: Any) -> Hash:
    return Hash('0x' + sha256(str(x).encode()).hexdigest())


def rh() -> Hash:
    return sha(time.time())


def hash2emoji(hash: Hash) -> str:
    if hash[:2] != '0x':
        hash = '0x' + hash

    offset = int(hash[0:4], 0)
    unicode = b'\U' + b'000' + str(hex(0x1F466 + offset))[2:].encode()
    return unicode.decode('unicode_escape')


def pretty_hash(hash: Hash) -> str:
    if len(hash) < 12:
        return hash
    else:
        return hash2emoji(hash) + ' ' + hash[:12] + '...' + hash[-3:]


def mini_pretty_hash(hash: Hash) -> str:
    if len(hash) < 6:
        return hash
    else:
        return hash2emoji(hash) + ' ' + hash[:6]


class Hashable:

    def __eq__(self, other) -> bool:
        return self.hash == other.hash

    def __bytes__(self) -> str:
        return self.hash.encode()

    def json(self) -> str:
        return {**self.__dict__}

    def __setattr__(self, prop: Any, val: Any) -> None:
        super().__setattr__(prop, val)
        if prop not in ['sig', 'signed', 'hash', 'nonce']:
            super().__setattr__('hash', sha(self.__dict__))

    def __str__(self) -> str:
        s = []
        for k, v in self.__dict__:
            p = f'{k}:'.ljust(15)
            if hasattr(v, 'messageHash'):
                s.append(p + pretty_hash(v.messageHash.hex()))
            elif str(v)[:2] == '0x':
                s.append(p + pretty_hash(v))
            elif type(v) is float:
                s.append(p + str(round(v, 8)) + ' bbc')
            else:
                s.append(p + str(v))
        return '\n'.join(s)
