# Module 1 - Create a Blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Block:
    def __init__(self, idx, proof, prev_hash):
        self.idx = idx
        self.timeStamp = str(datetime.datetime.now())
        self.proof = proof
        self.prev_hash = prev_hash
        self.data = {}
    
    def is_block_valid(self, prev_hash):
        return True
        
    def get_json_obj(self):
        return {
            "index": self.idx,
            "timestamp": self.timeStamp,
            "proof": self.proof,
            "previous_hash": self.prev_hash
        }
        
    def hash(self):
        encoded_block = json.dumps(self.get_json_obj(), sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, prev_hash = '0')
        
    def add_block(self):
        prev_block = self.get_prev_block()
        prev_proof = prev_block.proof
        proof = self.proof_of_work(prev_proof)
        return self.create_block(proof, prev_block.hash())
        
    def create_block(self, proof, prev_hash):
        block = Block(len(self.chain)+1, proof, prev_hash)
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        
        while not check_proof:
            if self.golden_proof(new_proof, prev_proof):
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def golden_proof(self, new_proof, prev_proof):
        return hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest().startswith("0000")
    
    def is_chain_valid(self):
        prev_hash = self.chain[0].hash()
        prev_proof = 1
        for block in self.chain[1:]:
            if block.prev_hash != prev_hash:
                return False
            prev_hash = block.hash()
            if not self.golden_proof(block.proof, prev_proof):
                return False
            prev_proof = block.proof
        return True
            

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# Creating a Blockchain
blockchain = Blockchain()

# http://127.0.0.1:5000/
# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    block = blockchain.add_block()
    response = block.get_json_obj()
    response['message'] = 'Congratulations you just mined a block!'
    return jsonify(response), 200


# Getting the full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': [block.get_json_obj() for block in blockchain.chain],  
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    response = {
        'is_valid': blockchain.is_chain_valid(),    
    }
    return jsonify(response), 200

# Running the app
app.run(host="0.0.0.0", port="5000")


