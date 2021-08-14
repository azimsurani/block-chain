# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 00:05:40 2021

@author: Azim
"""
import datetime
import hashlib
import json
from flask import Flask, jsonify


# Module 1 - Building a Blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof=1,previous_hash='0')

    
# Module 1 - Mining  our Blockchain