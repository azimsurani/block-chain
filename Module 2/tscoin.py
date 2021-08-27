# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 23:47:41 2021

@author: Azim
"""

# Module 2 - Create a cryptocurrency

import datetime
import hashlib
import json
from flask import Flask, jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Part 1 - Building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1,previous_hash='0')
    
    def create_block(self,proof,previous_hash):
        block = {
                    'index': len(self.chain)+1,
                    'timestamp' : str(datetime.datetime.now()),
                    'proof':proof,
                    'previous_hash':previous_hash,
                    'transactions': self.transactions
                }
        self.transactions = []
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] ==  "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self,block):
        encoded_block= json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index<len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] !=  "0000":
                return False
            block_index += 1
            previous_block = block
        
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
                'sender': sender,
                'receiver': receiver,
                'amount': amount
            })
        
        previous_block = self.get_previous_block()
        return previous_block['index']+1
    

# Part 2 - Mining  our Blockchain

# Creating a flask app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
blockchain = Blockchain()

@app.route("/mine_block", methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof, previous_hash)
    response = { "Message" : "Congratulations, you just mined a block",
                "index":block["index"],
                "timestamp":block["timestamp"],
                "proof":block["proof"],
                "previous_hash":block["previous_hash"]}
    
    return jsonify(response), 200

# Getting the full Blockchain
@app.route("/get_chain", methods=['GET'])
def get_chain():
    response = {
           'chain': blockchain.chain,
           'length' : len(blockchain.chain)
        }
    return jsonify(response), 200

# Getting the full Blockchain
@app.route("/is_valid", methods=['GET'])
def is_valid():
    return jsonify(blockchain.is_chain_valid(blockchain.chain)), 200

#Running the app
if __name__ == '__main__':