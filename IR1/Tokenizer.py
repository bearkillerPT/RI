import sys
import Parser
from nltk.stem import PorterStemmer

from Parser import Parser
class Tokenizer:
    def __init__(self, filename, min_length_filter, stop_word_list, porter_stemmer):
        self.parsedDoc = Parser(filename)
        if not self.parsedDoc.dataFile or len(self.parsedDoc.documents.keys()) == 0:
            self = None
            return None
        self.min_length_filter = min_length_filter
        self.stop_word_list = stop_word_list
        self.porter_stemmer = porter_stemmer
        self.tokenize()
        print(self.tokens)
    
    def tokenize(self):
        self.tokens = {}
        for doc in self.parsedDoc.documents.keys():
            for review in self.parsedDoc.documents[doc]:
                text = review['product_title'] + ' '
                text += review['review_headline'] + ' '
                text += review['review_body']
                tokens = text.split(' ')
                for token in tokens:
                    to_insert = token
                    if self.porter_stemmer:
                        ps = PorterStemmer()
                        to_insert = ps.stem(token)
                    if to_insert in self.stop_word_list or len(token) < self.min_length_filter: 
                        continue
                    if to_insert in self.tokens.keys():
                        self.tokens[to_insert].append(int(doc))
                    else:
                        self.tokens.setdefault(to_insert, [int(doc)])
        for token in self.tokens:
            self.tokens[token].sort()
            
                
        

if __name__=='__main__':
    min_length_filter=0
    stop_word_list = []
    porter_stemmer = True
    print(sys.argv)
    if len(sys.argv) == 1:
        usage = 'Usage:\n\tpython3 Tokenizer.py filename [options]*'
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
        tokenizer = Tokenizer(sys.argv[1], min_length_filter, stop_word_list, porter_stemmer) 