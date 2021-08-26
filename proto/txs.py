# Class for Txs in the blockchain
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