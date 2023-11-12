from blockchain import Blockchain
from blockchain import *
from transaction import *
from mine import *
from wallet import *
from wallet import *
from xmlrpc.server import SimpleXMLRPCServer

test_w1 = Wallet()
test_w2 = Wallet()
miner = Miner(test_w2)
def r_stxs(n): return [test_w1.signed_tx(test_w2,ri(1,9),ri(1,9)/100) for _ in range(n)]

gb  = mine_genesis(r_stxs(2))

global blockchain 
blockchain = Blockchain(gb)

global acc_dict 
acc_dict = {}

def create_acc(id: str):
    if id not in acc_dict: acc_dict[id] = Wallet()

def create_tx(id: str, to_pub: str, amount: int):
    try: blockchain.add(acc_dict[id].signed_tx(to_pub, amount, 1)); return True
    except AssertionError: return False

def create_block():
    if len(blockchain.staged_txs) > 0:
        return False
    else:
        try: return blockchain.add(blockchain.candidate())
        except AssertionError: return False

def get_blocks():
    return {'blocks': json.dumps([b.json() for b in blockchain.blocks])}

def get_block(block_number: str):
    return blockchain.blocks[int(block_number)].json()

def get_tx(block_number: str, tx_hash: str):
    return {'tx': blockchain.blocks[int(block_number)][tx_hash].json()}

def get_txs():
    txs = []
    for b in blockchain.blocks:
        for tx in b.txs.values():
            txs.append(tx.json())
    return {'transactions': txs}

def get_account(acc_hash: str):
    return blockchain[acc_hash].json()


server = SimpleXMLRPCServer(("localhost", 8000))
print("Starting XML-RPC server on localhost:8000")

server.register_function(create_acc, "add_acc")
server.register_function(create_tx, "add_tx")
server.register_function(create_block, "add_block")
server.register_function(get_blocks, "blocks")
server.register_function(get_block, "block")
server.register_function(get_tx, "tx")
server.register_function(get_txs, "txs")
server.register_function(get_account, "acc")


server.serve_forever()