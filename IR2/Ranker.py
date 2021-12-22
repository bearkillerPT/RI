#Gil Teixeira - 88194
import codecs
from collections import OrderedDict
from datetime import datetime
from re import T
from nltk.downloader import FinishCollectionMessage
from Indexer import Indexer
import sys
from os import system
import json
import time
import math
from nltk import PorterStemmer

class Ranker:

    def __init__(self, filename,min_length_filter = 0,stop_word_list = [],porter_stemmer=True):
        self.init_timer = datetime.now()
        self.indexer = Indexer(filename, min_length_filter,stop_word_list,porter_stemmer) 
        self.ps = PorterStemmer()

    def getIndex(self, filename): 
        if self.indexer.tokenizer.parsedDoc.dataFile and not len(self.indexer.tokenizer.parsedDoc.documents.keys()) == 0:
            index_file = open(filename + '_index', 'r')
            return json.load(index_file)

    def tfIdfRanker(self, query):
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
                fp = open(self.indexer.filename[:-4] + "_index/" + token[0] + ".block", 'r')
                postings_yielder = self.indexer.loadBlock(fp)
                found = False
                for block in postings_yielder:
                    if list(block.keys())[0] == token:
                        documents[token] = block[token]
                        found = True
                        break
                if not found:
                    documents[token] = {}
                fp.close()
            except Exception as e:
                documents[token] = {}
            query_wt[token] /= query_normal
            
        res = self.calculateDocQueryWeight(query_wt, documents)
        fp = open(self.indexer.filename[:-4] + "_index/" + query +  ".top100docs", 'w')
        self.indexer.writeBlock(res, fp)
        fp.close()
        return res


    def calculateDocQueryWeight(self, query_wt, documents):
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
                        res[doc][token] = float(documents[token][doc]) * query_wt[token]
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
            
        return dict(sorted(res_sum.items(), key=lambda item: item[1], reverse=True)[:100])

                
                    
    def searchToken(self, token):
        if token in self.indexer.index.keys():
            self.tokenizer_timer = str(datetime.now() - self.init_timer)
            return self.indexer.index[token]
        else:
            return []
        


    

if __name__=='__main__':
    test_file_names = ["amazon_reviews_us_Digital_Video_Games_v1_00.tsv","amazon_reviews_us_Digital_Music_Purchase_v1_00.tsv", "amazon_reviews_us_Music_v1_00.tsv", "amazon_reviews_us_Books_v1_00.tsv" ] 
    min_length_filter=2
    stop_word_list = []
    porter_stemmer = True
    if len(sys.argv) == 1:
        usage = 'Usage:\n\tpython3 Ranker.py queries.txt'
        print(usage)
    else:
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
                    searcher.tfIdfRanker(query)
                    print("SearchTime: " + str(datetime.now() - (searcher.init_timer + merge_time)))
            except Exception as e:
                print(e)
                
