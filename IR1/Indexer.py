#Gil Teixeira - 88194
from datetime import date, datetime
from Tokenizer import Tokenizer
import json
import sys
import os
class Indexer:
    def __init__(self, filename):
        init_timer = datetime.now()
        self.tokenizer = Tokenizer(filename, 0, [], True)
        self.tokenizer_timer = 0
        if(self.tokenizer.parsedDoc.dataFile and not len(self.tokenizer.parsedDoc.documents.keys()) == 0):
            self.index_SPIMI()
            self.indexed_size = sys.getsizeof(self.index)
            self.vocabulary_size = len(self.tokenizer.indexable_tokens)
            self.index_time = datetime.now() - init_timer
        else:
            self.indexed_size = 0
            self.vocabulary_size = 0
            
    def index_SPIMI(self, block_memory=10000000, block_postings=1000000):
        token_yielder = self.tokenizer.token_yielder()
        current_block_postings = 0
        current_block = {}
        total_blocks = 0
        for (token, doc) in token_yielder:
            if sys.getsizeof(current_block) >= block_memory or current_block_postings >= block_postings:
                for token in current_block:
                    current_block[token].sort()
                fp = open('block_' + str(total_blocks), 'w')
                json.dump(current_block, fp)
                fp.close()
                total_blocks += 1
                current_block_postings = 0
                current_block = {}
                
            if token in current_block.keys():
                if doc not in current_block[token]:
                    current_block[token].append(doc)
                    current_block_postings += 1
            else:
                current_block[token] =  [doc]
        
        if sys.getsizeof(current_block) > 0 or current_block_postings > 0:
                for token in current_block:
                    current_block[token].sort()
                fp = open('block_' + str(total_blocks), 'w')
                json.dump(current_block, fp)
                total_blocks += 1
                fp.close()
        self.total_blocks = total_blocks
        self.mergeBlocks()

    def mergeBlocks(self):
        blocks = []
        for i in range(self.total_blocks):
            block_file = open('block_' + str(i), 'r')
            block = json.load(block_file)
            block_file.close()
            blocks.append(block)
            os.remove('block_' + str(i))
        index = {}
        for token in self.tokenizer.indexable_tokens:
            for block in blocks:
                if token in block.keys():
                    if token in index.keys():
                        res = index[token]
                        for doc in block[token]:
                            if doc not in res:
                                res.append(doc)
                        index[token] = res
                    else:
                        index.setdefault(token, block[token])
        self.index = index