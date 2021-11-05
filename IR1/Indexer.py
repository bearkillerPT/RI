from datetime import datetime
from Tokenizer import Tokenizer
import sys
class Indexer:
    def __init__(self, filename):
        init_timer = datetime.now()
        tokenizer = Tokenizer(filename, 0, [], True)
        self.tokenizer_timer = str(datetime.now() - init_timer)
        self.indexed_size = sys.getsizeof(tokenizer) #Bytes
        if(tokenizer.parsedDoc.dataFile and not len(tokenizer.parsedDoc.documents.keys()) == 0):
            self.vocabulary_size = len(tokenizer)
        else:
            self.vocabulary_size = 0





if __name__=='__main__':
    test_file_names = [  "amazon_reviews_us_Digital_Video_Games_v1_00.tsv.gz", "amazon_reviews_us_Digital_Music_Purchase_v1_00.tsv.gz", "amazon_reviews_us_Music_v1_00.tsv.gz", "amazon_reviews_us_Books_v1_00.tsv.gz" ] 
    for test_file_name in test_file_names:
        indexer = Indexer(test_file_name)
        print(indexer.indexed_size)
        print(indexer.vocabulary_size)
        print(indexer.tokenizer_timer)
