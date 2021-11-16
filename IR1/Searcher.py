#Gil Teixeira - 88194
from datetime import datetime
from Indexer import Indexer
import sys

class Searcher:
    def __init__(self, filename):
        self.indexer = Indexer(filename) 
        self.init_timer = datetime.now()
    def searchToken(self, token):
        if self.indexer.tokenizer.parsedDoc.dataFile and not len(self.indexer.tokenizer.parsedDoc.documents.keys()) == 0:
            if token in self.indexer.index.keys():
                self.tokenizer_timer = str(datetime.now() - self.init_timer)
                return self.indexer.index[token]
            else:
                return []
        else:
            self.tokenizer_timer = str(datetime.now() - self.init_timer)
            return []




if __name__=='__main__':
    if len(sys.argv) == 1:
        usage = 'Usage:\n\tpython3 Search.py token'
        print(usage)
    elif len(sys.argv) == 2:
        test_file_names = ["test.tsv",  "amazon_reviews_us_Digital_Video_Games_v1_00.tsv", "amazon_reviews_us_Digital_Music_Purchase_v1_00.tsv"]#, "amazon_reviews_us_Music_v1_00.tsv", "amazon_reviews_us_Books_v1_00.tsv" ] 
        for test_file_name in test_file_names:
            searcher = Searcher(test_file_name)
            if searcher.indexer.vocabulary_size > 0:
                print("Indexed Efective Size (Bytes): " + str(searcher.indexer.indexed_size))
                print("Vocabulary Size (Tokens): " + str(searcher.indexer.vocabulary_size))
                print("Temporary indexed segments: " + str(searcher.indexer.total_blocks))
                print("Token frequency: " + str(len(searcher.searchToken(sys.argv[1]))))
                print("Search time: " + str(searcher.indexer.tokenizer_timer))
                print("\n")
