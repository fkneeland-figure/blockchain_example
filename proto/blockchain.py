# global imports
import hashlib
import requests
from urllib.parse import urlparse

# local imports
from block import Block
from txs import Txs

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
