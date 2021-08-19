# Module 2 - Create a Cryptocurrency

import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import sys

# Part 1 - Building a blockchain

class Block:
    def __init__(self, idx, proof, prev_hash, txs):
        self.idx = idx
        self.timeStamp = str(datetime.datetime.now())
        self.proof = proof
        self.prev_hash = prev_hash
        self.data = {}
        self.txs = txs
    
    def is_block_valid(self, prev_hash):
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
        print(encoded_block)
        return hashlib.sha256(encoded_block).hexdigest()
            
class Txs:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        
    def get_json_obj(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self.txs = []
        self.create_block(proof = 1, prev_hash = '0')
        self.nodes = set() 
        
        
    def add_block(self):
        prev_block = self.get_prev_block()
        prev_proof = prev_block.proof
        proof = self.proof_of_work(prev_proof)
        return self.create_block(proof, prev_block.hash())
        
    def create_block(self, proof, prev_hash):
        block = Block(len(self.chain)+1, proof, prev_hash, self.txs)
        self.txs = []
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
            
    
    def is_chain_valid(self, chain):
        prev_hash = chain[0].hash()
        prev_proof = 1
        print(chain[0].get_json_obj())
        for block in chain[1:]:
            if block.prev_hash != prev_hash:
                print("prev hash is wrong: "+str(block.prev_hash)+" : " + str(prev_hash))
                return False
            prev_hash = block.hash()
            if not self.golden_proof(block.proof, prev_proof):
                print("golden_proof is wrong")
                return False
            prev_proof = block.proof
            print("block is correct")
        return True
    
    def convert_json_chain(self, chain):
        json_chain = []
        
        for block in chain:
            txs = [Txs(tx['sender'], tx['receiver'], int(tx['amount'])) for tx in block["txs"]]
            newblock = Block(int(block["index"]), int(block["proof"]), block["previous_hash"], txs)
            newblock.timeStamp = block["timestamp"]
            json_chain.append(newblock)
        
        return json_chain
    
    def add_tx(self, sender, receiver, amount):
        self.txs.append(Txs(sender, receiver, amount))
        return self.get_prev_block().idx + 1    
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        longest_chain = None
        max_length = len(self.chain)
        print("our chain length: " + str(max_length))
        
        for node in self.nodes:
            response = requests.get("http://"+node+"/get_chain")
            print("got response from node: " +node+ " response: " + str(response.status_code))
            if response.status_code == 200:
                print("response is 200")
                length = response.json()['length']
                print("length is: "+str(length))
                chain = self.convert_json_chain(response.json()['chain'])
                if length > max_length and self.is_chain_valid(chain):
                    print("use this chain")
                    max_length = length
                    longest_chain = chain
                    
        if longest_chain:
            self.chain = longest_chain
            return True
        
        return False

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace("-", "")

# Creating a Blockchain
blockchain = Blockchain()

name = "Fred"

if len(sys.argv) > 2:
    name = sys.argv[2]

# http://127.0.0.1:5000/
# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    blockchain.add_tx(node_address, name, 100)
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

# Check that the chain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    response = {
        'is_valid': blockchain.is_chain_valid(blockchain.chain),    
    }
    return jsonify(response), 200

# Post a Tx
@app.route('/add_tx', methods=['POST'])
def add_tx():
    json = request.get_json()
    tx_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in tx_keys):
        return 'Some elements are missing', 400
    
    index = blockchain.add_tx(json['sender'], json['receiver'], json['amount'])
    response = {'message': f"This tx will be added to Block {index}"}
    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes == None:
        return "No node", 400
    
    for node in nodes:
        blockchain.add_node(node)
    
    response = {'message': "All the nodes have been added to the blockchain",
                'total_nodes': len(blockchain.nodes)}
    return response, 201

# Check that the chain is valid
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    response = {
        'replaced_chain': blockchain.replace_chain(),    
    }
    return jsonify(response), 200

port = sys.argv[1]
print("running a server on port: " + port)

# Running the app
app.run(host="0.0.0.0", port=port)


