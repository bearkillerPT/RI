#Gil Teixeira - 88194
from datetime import datetime
from Tokenizer import Tokenizer
import copy
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

            
    def index_SPIMI(self, block_memory=5000000, block_postings=100000): #~12MB each block
        token_yielder = self.tokenizer.token_yielder()
        current_block_postings = 0
        index = {}
        current_block = OrderedDict()
        total_blocks = 0
        last_seen = None
        for (token, doc, pos) in token_yielder: #get_size(current_block) >= block_memory was a condition but too slow
            if doc != last_seen:
                if current_block_postings >= block_postings:
                    l2_normal = {}
                    for token in current_block:
                        for doc_seen in current_block[token]:
                            if doc_seen not in l2_normal.keys():
                                l2_normal[doc_seen] = math.pow(current_block[token][doc_seen]["count"],2)
                            else:
                                l2_normal[doc_seen] += math.pow(current_block[token][doc_seen]["count"],2)
                    for token in current_block:
                        for doc_seen in current_block[token]:
                            current_block[token][doc_seen]["weight"] = (1 + math.log10(current_block[token][doc_seen]["count"])) / math.sqrt(l2_normal[doc_seen])
                    fp = open("" + str(total_blocks) + ".block", 'w', encoding='utf-8')
                    self.writeBlock(current_block, fp)
                    fp.close()
                    total_blocks += 1   
                    current_block_postings = 0
                    current_block = OrderedDict()
                last_seen = doc

            if token in current_block.keys():
                if doc in current_block[token].keys():
                    current_block[token][doc]["pos"].append(pos)
                    current_block[token][doc]["count"] += 1
                else:
                    current_block[token][doc] = {"pos":[pos], "count": 1}
                index[token] += 1
            else:
                index[token] = 1
                current_block[token] = {doc: {"pos":[pos], "count": 1}}
            current_block_postings += 1
            
        self.index = index
        
        if current_block_postings >= 0:
            l2_normal = {}
            for token in current_block:
                for doc_seen in current_block[token]:
                    if doc_seen not in l2_normal.keys():
                        l2_normal[doc_seen] = math.pow(current_block[token][doc_seen]["count"],2)
                    else:
                        l2_normal[doc_seen] += math.pow(current_block[token][doc_seen]["count"],2)
            for token in current_block:
                for doc_seen in current_block[token]:
                    current_block[token][doc_seen]["weight"] = (1 + math.log10(current_block[token][doc_seen]["count"])) / math.sqrt(l2_normal[doc_seen])
            fp = open("" + str(total_blocks) + ".block", 'w', encoding='utf-8')
            self.writeBlock(current_block, fp)
            fp.close()
            total_blocks += 1
            current_block_postings = 0
            current_block = OrderedDict()
        self.total_blocks = total_blocks
        #merge
        print("Merging!")
        self.mergeIndex(block_postings)

    def mergeIndex(self, block_postings):
        block_yielders = []
        for i in range(self.total_blocks):
            fp = open("" + str(i) + ".block", 'r', encoding='utf-8')
            block_yielders.append(self.loadBlock(fp))
        current_block = {}
        current_postings = 0
        current_keys = []       
        done = False
        for block_yielder in block_yielders:    
            for block in block_yielder:
                token = list(block.keys())[0]
                current_keys.append(token)
                if token not in current_block.keys():
                    current_block[token] = {}
                for doc in block[token]:
                    current_block[token][doc] = {}
                    count = len(block[token][doc]["pos"])
                    current_block[token][doc]["weight"] = block[token][doc]["weight"]
                    current_block[token][doc]["pos"] = block[token][doc]["pos"]
                    current_block[token][doc]["count"] = count
                    current_postings += count
                break
        if len(current_keys) == 0:
            return

        index_dir = self.filename[:-4] + "_index/"
        try: 
            os.mkdir(index_dir)    
        except:
            pass    
        while not done:
            #should be a prioritized key

            
            if all(x == None for x in block_yielders):
                done = True
            if current_postings >= block_postings or done:
                
                last_key = sorted(current_block.keys())[0]
                res = {}
                for key in sorted(current_block.keys()):
                    if key[0] != last_key[0]:
                        try:
                            self.writeBlock(res, open(index_dir + last_key[0] + ".block",'a', encoding='utf-8'))
                            last_key = key
                            res = {}
                        except Exception as e:
                            print(e)
                    if key not in res.keys():
                        res[key] = {}
                    for doc in current_block[key]:
                        res[key][doc] = current_block[key][doc]
                current_postings = 0
                try:
                    res = {last_key:{}}
                    for doc in current_block[last_key]:
                        res[last_key][doc] = current_block[last_key][doc]
                    self.writeBlock(res, open(index_dir + last_key[0] + ".block",'a', encoding='utf-8'))
                except Exception as e:
                    print(e)
                current_block={}
            else: #find the min token in the document yielders and yield the next
                
                min = None
                selected_i = 0
                for j, key in enumerate(current_keys):
                    if(block_yielders[j] == None):
                        continue
                    if min == None or key[0] < min[0]:
                        min = key
                        selected_i = j

                selected_block = {}
                for block in block_yielders[selected_i]:
                    selected_block = copy.deepcopy(block)
                    break
                if len(list(selected_block.keys())) != 0:
                    token = list(selected_block.keys())[0]
                    if token not in current_block.keys():
                        current_block[token] = {}
                    for sel_doc in selected_block[token]:
                        current_block[token][sel_doc] = selected_block[token][sel_doc]
                        count = len(current_block[token][sel_doc]["pos"])
                        current_block[token][sel_doc]["count"] = count
                        current_postings += count
                    current_keys[selected_i] = token
                else:
                    block_yielders[selected_i] = None


                    
                           

                    
        
    def writeSearch(self, block, fp):
        res = ""
        for token in block.keys():
            res += str(block[token])+ ";\n"
        return fp.write(res)

    def writeBlock(self, block, fp):
        res = ""
        for token in sorted(block.keys()):
            res += token + ";"
            if isinstance(block[token], dict):
                for doc in block[token]:
                    res += str(doc) + ":" + str(block[token][doc]["weight"]) + ":" 
                    res += str(block[token][doc]["pos"])[1:-1] + ";"
            res += "\n"
        return fp.write(res)

    def loadBlock(self, fp):
        for line in fp:
            res = {}
            values = line.split(';')
            token = values[0]

            res[token] = {}
            for i in range(1, len(values)-1):
                [doc, weight, pos] = values[i].split(':')
                res[token][doc] = {}
                res[token][doc]["weight"] = weight
                res[token][doc]["pos"] = [int(p) for p in pos.split(',')]
            yield res

    

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
