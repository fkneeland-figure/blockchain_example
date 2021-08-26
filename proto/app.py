from flask import Flask, jsonify, request
from uuid import uuid4

# local imports
from blockchain import Blockchain

# Creating a Web App
app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace("-", "")

# Creating a Blockchain
blockchain = Blockchain()


name = "validator"

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

port = "5000"
print("running a server on port: " + port)

# Running the app
app.run(host="0.0.0.0", port=port)