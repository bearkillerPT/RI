from datetime import datetime
from Tokenizer import Tokenizer
import sys
class Indexer:
    def __init__(self, filename):
        self.init_timer = datetime.now()
        self.tokenizer = Tokenizer(filename, 0, [], True)
        self.tokenizer_timer = 0
        
        if(self.tokenizer.parsedDoc.dataFile and not len(self.tokenizer.parsedDoc.documents.keys()) == 0):
            self.vocabulary_size = len(self.tokenizer.tokens.keys())
            self.indexed_size = sys.getsizeof(self.tokenizer.tokens) #Bytes

        else:
            self.indexed_size = 0
            self.vocabulary_size = 0
            

    def searchToken(self, token):
        if self.tokenizer.parsedDoc.dataFile and not len(self.tokenizer.parsedDoc.documents.keys()) == 0:
            if token in self.tokenizer.tokens.keys():
                self.tokenizer_timer = str(datetime.now() - self.init_timer)
                return self.tokenizer.tokens[token]
        else:
            self.tokenizer_timer = str(datetime.now() - self.init_timer)
            return []




if __name__=='__main__':
    if len(sys.argv) == 1:
        usage = 'Usage:\n\tpython3 Search.py token'
        print(usage)
    elif len(sys.argv) == 2:
        test_file_names = ["test.tsv",  "amazon_reviews_us_Digital_Video_Games_v1_00.tsv", "amazon_reviews_us_Digital_Music_Purchase_v1_00.tsv", "amazon_reviews_us_Music_v1_00.tsv", "amazon_reviews_us_Books_v1_00.tsv" ] 
        for test_file_name in test_file_names:
            indexer = Indexer(test_file_name)
            if indexer.vocabulary_size > 0:
                print("Indexed Efective Size (Bytes): " + str(indexer.indexed_size))
                print("Vocabulary Size (Tokens): " + str(indexer.vocabulary_size))
                print("Inndex + Search time: " + str(indexer.tokenizer_timer))
                print("Token frequency: " + str(len(indexer.searchToken(sys.argv[1]))))
                print("\n")
