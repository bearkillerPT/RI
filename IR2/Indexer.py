#Gil Teixeira - 88194
from datetime import date, datetime
from Tokenizer import Tokenizer
import json
import sys
import math
import os
from collections import OrderedDict 
from splitstream import splitfile



class Indexer:
    def __init__(self, filename, min_len_filter=0, stop_words_list=[], porter_stemmer=True):
        self.filename = filename
        self.init_timer = datetime.now()
        self.tokenizer = Tokenizer(filename, min_len_filter, stop_words_list, porter_stemmer)
        self.tokenizer_timer = 0
        self.index_SPIMI()
        self.vocabulary_size = len(self.tokenizer.indexable_tokens)
        self.index_time = datetime.now() - self.init_timer

            
    def index_SPIMI(self, block_memory=5000000, block_postings=1000000): #~12MB each block
        token_yielder = self.tokenizer.token_yielder()
        current_block_postings = 0
        index = {}
        current_block = OrderedDict()
        total_blocks = 0
        for (token, doc) in token_yielder: #get_size(current_block) >= block_memory was a condition but too slow
            if current_block_postings >= block_postings:
                try:
                    fp = open(token[0].lower() + ".block", 'r')
                    tmp_dict = json.load(fp)
                    if token not in tmp_dict.keys():
                        tmp_dict[token] = current_block[token]
                    else:
                        for doc in current_block[token]:
                            if doc in tmp_dict[token].keys():
                                tmp_dict[token][doc] += current_block[token][doc]
                            else:
                                tmp_dict[token][doc] = current_block[token][doc]
                    fp.close()
                except:
                    tmp_dict = {token: current_block[token]}
                finally:
                    fp = open(block_token[0].lower() + ".block", 'w')
                    json.dump(tmp_dict, fp)
                    fp.close()
                    total_blocks += 1
                current_block_postings = 0
                current_block = OrderedDict()

            if token in current_block.keys():
                if doc in current_block[token].keys(): 
                    current_block[token][doc] += 1
                else:
                    current_block[token][doc] = 1
                index[token] += 1
            else:
                index[token] = 1
                current_block[token] = {doc: 1}
                current_block_postings += 1
            
            
        if current_block_postings > 0:
            for block_token in current_block:
                try:
                    fp = open(block_token[0].lower() + ".block", 'r')
                    tmp_dict = json.load(fp)
                    if block_token not in tmp_dict.keys():
                        tmp_dict[block_token] = current_block[block_token]
                    else:
                        for doc in current_block[block_token]:
                            if doc in tmp_dict[block_token].keys():
                                tmp_dict[block_token][doc] += current_block[block_token][doc]
                            else:
                                tmp_dict[block_token][doc] = current_block[block_token][doc]
                    fp.close()
                except:
                    tmp_dict = {block_token: current_block[block_token]}
                finally:
                    fp = open(block_token[0].lower() + ".block", 'w')
                    json.dump(tmp_dict, fp)
                    fp.close()
                    total_blocks += 1
        self.total_blocks = total_blocks
        #merge
        self.mergeIndex()

    def mergeIndex(self):
        index = OrderedDict({})
        for token in sorted(list(self.tokenizer.indexable_tokens)):
            try:
                fp = open(token[0].lower() + ".block", 'r')

                tmp_dict = json.load(fp)
                if token not in index:
                    index[token] = {}
                for key in tmp_dict[token]: 
                    index[token][key] = (1 + math.log10(tmp_dict[token][key])) 
                fp.close()
            except:
                index[token] = OrderedDict({})
        l2_normal = {}
        ## Vector length normalization
        for token in index.keys():        
            for doc in index[token].keys():
                if doc in index[token].keys():
                    if token not in l2_normal.keys():
                        print(token)
                        l2_normal.setdefault(token, math.pow(index[token][doc], 2))
                    else:
                        l2_normal[token] += math.pow(index[token][doc], 2)
        print(l2_normal)
        for token in index.keys():
            l2_normal[token] = math.sqrt(l2_normal[token]) 

        for token in index:
            if doc in index[token].keys():
                index[token][doc] = index[token][doc] / l2_normal[token]

        ##
        self.index = index
        print(index)
        self.save_index(index, {})

    def yield_json_line(self, file):
        for jsonstr in splitfile(file, format="json"):
            yield json.loads(jsonstr)

    def save_index(self, index, postings):
        index_file = open(self.filename + '_index', 'w')
        json.dump(index, index_file)
        index_file.close()
        if postings != {}:
            postings_file = open(self.filename + '_postings', 'w')
            json.dump(postings, postings_file)
            postings_file.close()
        
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
