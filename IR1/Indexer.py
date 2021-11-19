#Gil Teixeira - 88194
from datetime import date, datetime
from Tokenizer import Tokenizer
import json
import sys
import os
class Indexer:
    def __init__(self, filename, min_len_filter=0, stop_words_list=[], porter_stemmer=True):
        self.filename = filename
        self.init_timer = datetime.now()
        self.tokenizer = Tokenizer(filename, min_len_filter, stop_words_list, porter_stemmer)
        self.tokenizer_timer = 0
        if(self.tokenizer.parsedDoc.dataFile and not len(self.tokenizer.parsedDoc.documents.keys()) == 0):
            self.index_SPIMI()
            self.indexed_size = sys.getsizeof(self.index)
            self.vocabulary_size = len(self.tokenizer.indexable_tokens)
            self.index_time = datetime.now() - self.init_timer
        else:
            self.indexed_size = 0
            self.vocabulary_size = 0
            
    def index_SPIMI(self, block_memory=1000000, block_postings=1000000):
        token_yielder = self.tokenizer.token_yielder()
        current_block_postings = 0
        current_block = {}
        total_blocks = 0
        for (token, doc) in token_yielder:
            if (current_block.__sizeof__() + current_block_postings) >= block_memory or current_block_postings >= block_postings:
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
                current_block[token] = [doc]
        
        if sys.getsizeof(current_block) > 0 or current_block_postings > 0:
                for token in current_block:
                    current_block[token].sort()
                fp = open('block_' + str(total_blocks), 'w')
                json.dump(current_block, fp)
                total_blocks += 1
                fp.close()
        self.total_blocks = total_blocks
        print(str(datetime.now() - self.init_timer))
        self.mergeBlocks()

    def mergeBlocks(self):
        index = {}
        for i in range(self.total_blocks):
            block_file = open('block_' + str(i), 'r')
            block = json.load(block_file)
            block_file.close()
            os.remove('block_' + str(i))
            for token in self.tokenizer.indexable_tokens:
                if token in block.keys():
                    if token in index.keys():
                        res = index[token]
                        for doc in block[token]:
                            if doc not in res:
                                res.append(doc)
                        index[token] = res
                    else:
                        index[token] = block[token]
        self.index = index
        self.save_index()

    def save_index(self):
        index_file = open(self.filename + '_index', 'w')
        json.dump(self.index, index_file)
        index_file.close()
if __name__ == "__main__":
    min_length_filter=0
    stop_word_list = []
    porter_stemmer = True
    print(sys.argv)
    if len(sys.argv) == 1:
        usage = 'Usage:\n\tpython3 Indexer.py filename [options]*'
        usage += '\n\toptions:\n\t\t--min-length-filter value\t(default: disabled)\n'
        usage += '\n\t\t--stop-word-list [value (, value)*]]\t(default: [])\n'
        usage += '\n\t\t--no-porter-stemmer\t(default: --porter-stemmer)\n'
        print(usage)
    else:
        for arg_i in range(2, len(sys.argv) ):
            if sys.argv[arg_i] == '--min-length-filter':
                min_length_filter = int(sys.argv[arg_i + 1])
                arg_i += 1
            elif sys.argv[arg_i] == '--no-porter-stemmer':
                porter_stemmer = False
            elif sys.argv[arg_i] == '--stop-word-list':
                i = 1
                value =  sys.argv[arg_i + i].removeprefix('[')
                while value:
                    if value.__contains__(']'):
                        stop_word_list.append(value.removesuffix(']'))
                        value = None 
                    else:
                        stop_word_list.append(value)
                        i += 1
                        value =  sys.argv[arg_i + i]
                arg_i += i 
        indexer = Indexer(sys.argv[1], min_length_filter, stop_word_list, porter_stemmer)
        print(indexer.index)