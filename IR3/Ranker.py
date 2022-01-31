#Gil Teixeira - 88194
from ast import parse
from collections import OrderedDict
from datetime import datetime
from click import parser
from nltk.downloader import FinishCollectionMessage
from Indexer import Indexer
import sys
from os import system
import copy
import time
import math
from nltk import PorterStemmer

class Ranker:

    def __init__(self, filename,min_length_filter = 0,stop_word_list = [],porter_stemmer=True):
        self.init_timer = datetime.now()
        self.indexer = Indexer(filename, min_length_filter,stop_word_list,porter_stemmer) 
        self.ps = PorterStemmer()

    def tfIdfRanker(self, query, boost=None):
        query_wt = {}
        for token in query.split(' '):
            to_insert = self.ps.stem(token)
            if to_insert in query_wt.keys():
                query_wt[to_insert] += 1
            else:
                query_wt[to_insert] = 1
        documents = {}
        query_normal = 0
        for token in query_wt:
            query_wt[token] = 1 + math.log10(query_wt[token])
            query_normal += math.pow(query_wt[token], 2)
        query_normal = math.sqrt(query_normal)
        for token in query_wt:
            try:
                fp = open(self.indexer.filename[:-4] + "_index/" + token[0] + ".block", 'r', encoding='utf-8')
                postings_yielder = self.indexer.loadBlock(fp)
                found = False
                for block in postings_yielder:
                    if list(block.keys())[0] == token:
                        documents[token] = copy.deepcopy(block[token])
                        found = True
                        break
                if not found:
                    documents[token] = {}
                fp.close()
            except Exception as e:
                print(e)
                documents[token] = {}
            query_wt[token] /= query_normal
            
        res = self.calculateDocQueryWeight(query_wt, documents, boost)
        fp = open(self.indexer.filename[:-4] + "_index/" + query +  ".top100docs", 'w')
        self.indexer.writeSearch(res, fp)
        fp.close()
        return res


    def calculateDocQueryWeight(self, query_wt, documents, boost):
        docs = set()
        for token in documents:
            for doc in documents[token]:
                docs.add(doc)
        res = {}
        for doc in docs:
            for token in query_wt:
                if doc not in res:
                    res[doc] = {}
                if token in documents:
                    if doc in documents[token]:
                        res[doc][token] = float(documents[token][doc]["weight"]) * query_wt[token]
                    else:
                        res[doc][token] = 0
                else:
                    res[doc][token] = 0
        res_sum = {}
        for doc in res:
            total = 0
            for token in res[doc]:
                total += res[doc][token]
            res_sum[doc] = total 
            if boost:
                res_sum[doc] += self.boost(doc, res[doc], query_wt.keys(), documents)
        
        return dict(sorted(res_sum.items(), key=lambda item: item[1], reverse=True)[:100])


    def boost(self, target_doc, doc_index, query_tokens, documents,q_window=5):
            print("boost")
            res = 0
            q_doc_count = 0
            for token in doc_index:
                if token in query_tokens:
                    q_doc_count += 1
            if q_doc_count >= 2:
                last_pos = 0
                query_doc_pos = {}
                for token in doc_index:
                    if target_doc in documents[token]:
                        if token in query_doc_pos:
                            query_doc_pos[token].append(documents[token][target_doc]["pos"])
                        else:
                            query_doc_pos[token] = documents[token][target_doc]["pos"]
                        for pos in query_doc_pos[token]:
                            if int(pos) > last_pos:
                                last_pos = int(pos)
                max_tokens_in_win = 0
                i = 0
                while(i < last_pos):
                    current_window_tokens = 0
                    for token in query_doc_pos:
                        for pos in query_doc_pos[token]:
                            if int(pos) >= i or int(pos) < i + q_window:
                                current_window_tokens += 1
                    if current_window_tokens > max_tokens_in_win:
                        max_tokens_in_win = current_window_tokens            
                    i += q_window
                return q_window/(last_pos+1)   
                                
            else:                    
                return 0


def parseRelevance(relevance_filename):
    res = {}
    current_querie = None
    try:
        fp = open(relevance_filename, 'r')
        while line := fp.readline():
            if line == "\n":
                continue
            elif line[0:2] == 'Q:':
                current_querie = line[2:-1]
                res[current_querie] = {}
            else: 
                [token, relevance] = line.split('\t')
                res[current_querie][token] = relevance[:-1]


    except Exception as e:
        print(e.__traceback__())
    return res

if __name__=='__main__':
    test_file_names = ["amazon_reviews_us_Digital_Video_Games_v1_00.tsv","amazon_reviews_us_Digital_Music_Purchase_v1_00.tsv", "amazon_reviews_us_Music_v1_00.tsv", "amazon_reviews_us_Books_v1_00.tsv" ] 
    min_length_filter=2
    stop_word_list = []
    porter_stemmer = False
    if len(sys.argv) == 1:
        usage = 'Usage:\n\tpython3 Ranker.py queries.txt (--boost queries.relevance.txt)?'
        print(usage)
    else:
        boost = False
        relevance = None
        if len(sys.argv) == 4:
            boost = True
            relevance_filename = sys.argv[3]
            relevance = parseRelevance(relevance_filename)
        
        for test_file_name in test_file_names:
            time.sleep(1)
            system('del *.block')  
            print(test_file_name[:-4])
            searcher = Ranker(test_file_name, min_length_filter, stop_word_list, porter_stemmer)
            merge_time =  datetime.now() - searcher.init_timer
            print("IndexMergeTime: " + str(merge_time))
            try: 
                fp = open(sys.argv[1],'r')
                for line in fp.readlines():
                    query = line.strip(' \n')
                    searcher.tfIdfRanker(query, boost)
                    print("SearchTime: " + str(datetime.now() - (searcher.init_timer + merge_time)))
            except Exception as e:
                print(e)
                print(e.with_traceback())
                
