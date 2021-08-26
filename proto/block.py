import datetime
import hashlib
import json

class Block:
    def __init__(self, idx, proof, prev_hash, txs):
        self.idx = idx
        self.timeStamp = str(datetime.datetime.now())
        self.proof = proof
        self.prev_hash = prev_hash
        self.data = {}
        self.txs = txs   
    
    def is_block_valid(self, prev_hash):
        # TODO: make sure that each tx is correctly signed
        return True
        
    def get_json_obj(self):
        return {
            "index": self.idx,
            "timestamp": self.timeStamp,
            "proof": self.proof,
            "previous_hash": self.prev_hash,
            "txs": self.jsonify_txs(),
        }
    
    def jsonify_txs(self):
        txs = []
        
        for tx in self.txs:
            txs.append(tx.get_json_obj())
        
        return txs
        
    def hash(self):
        encoded_block = json.dumps(self.get_json_obj(), sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()