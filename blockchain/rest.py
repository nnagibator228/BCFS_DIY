from blockchain import *
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

global blockchain
txs_pool = {}

SUCCESS_CODE = '200 OK'


@app.route('/gb', methods=['POST'])
def init_bc() -> str:
    gb = request.get_json()['gb']
    gb = load_block(gb)
    global blockchain
    blockchain = Blockchain(gb)
    return SUCCESS_CODE


@app.route('/block', methods=['POST'])
def post_block() -> str:
    b = request.get_json()['block']
    b = load_block(b)
    blockchain.add(b)
    return SUCCESS_CODE


@app.route('/block/<block_number>', methods=['GET'])
def get_block(block_number: str) -> str:
    return blockchain.blocks[int(block_number)].json()


@app.route('/blocks', methods=['GET'])
def get_blocks() -> Dict[str, str]:
    return {'blocks': json.dumps([b.json() for b in blockchain.blocks])}


@app.route('/tx/<block_number>/<tx_hash>', methods=['GET'])
def get_tx(block_number, tx_hash: Hash) -> Dict[str, str]:
    return {'tx': blockchain.blocks[int(block_number)][tx_hash].json()}


@app.route('/txs', methods=['GET'])
def get_txs() -> Dict[str, List[TX]]:
    txs = []
    for b in blockchain.blocks:
        for tx in b.txs.values():
            txs.append(tx.json())
    return {'transactions': txs}


@app.route('/tx', methods=['POST'])
def post_tx() -> str:
    tx = request.get_json()['tx']
    tx = load_tx(tx)
    txs_pool[tx.hash] = tx
    return SUCCESS_CODE


@app.route('/tx_pool/<tx_hash>', methods=['GET'])
def get_pool_tx(tx_hash) -> Dict[str, str]:
    return {'tx': txs_pool[tx_hash].json()}


@app.route('/txs_pool', methods=['GET'])
def get_pool_txs() -> Dict[str, List[str]]:
    return {'txs_pool': [tx.json() for tx in txs_pool.values()]}


@app.route('/acc/<acc_hash>', methods=['GET'])
def get_account(acc_hash) -> str:
    return blockchain[acc_hash].json()


PORT = 5000

app.run(port=PORT)
