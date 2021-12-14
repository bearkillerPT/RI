#Gil Teixeira - 88194
from datetime import datetime
from Indexer import Indexer
import sys
from os import system
import json
import time

class Searcher:

    def __init__(self, filename,min_length_filter = 0,stop_word_list = [],porter_stemmer=True):
        self.indexer = Indexer(filename, min_length_filter,stop_word_list,porter_stemmer) 
        self.init_timer = datetime.now()

    def getIndex(self, filename): 
        if self.indexer.tokenizer.parsedDoc.dataFile and not len(self.indexer.tokenizer.parsedDoc.documents.keys()) == 0:
            index_file = open(filename + '_index', 'r')
            return json.load(index_file)

    def searchToken(self, token):
        if token in self.indexer.index.keys():
            self.tokenizer_timer = str(datetime.now() - self.init_timer)
            return len(self.indexer.index[token].keys())
        else:
            return []
        


    

if __name__=='__main__':
    test_file_names = ["test.tsv","amazon_reviews_us_Digital_Video_Games_v1_00.tsv", "amazon_reviews_us_Digital_Music_Purchase_v1_00.tsv" , "amazon_reviews_us_Music_v1_00.tsv", "amazon_reviews_us_Books_v1_00.tsv" ] 
    min_length_filter=0
    stop_word_list = []
    porter_stemmer = True
    if len(sys.argv) == 1:
        usage = 'Usage:\n\tpython3 Searcher.py token [options]*'
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
        for test_file_name in test_file_names:
            time.sleep(1)
            system('del *.block')
            searcher = Searcher(test_file_name, min_length_filter, stop_word_list, porter_stemmer)
            if searcher.indexer.vocabulary_size > 0:
                print("Indexed Efective Size (Bytes): " + str(sys.getsizeof(searcher.indexer.index)))
                print("Vocabulary Size (Tokens): " + str(searcher.indexer.vocabulary_size))
                print("Temporary indexed segments: " + str(searcher.indexer.total_blocks))
                print("Token frequency: " + str(searcher.searchToken(sys.argv[1])))
                print("Search time: " + str(searcher.indexer.tokenizer_timer))
                print("\n")
