import sys
import Parser

from Parser import Parser
class Tokenizer:
    def __init__(self, filename, min_length_filter=0, stop_word_list=[]):
        self.parsedDoc = Parser(filename)
        if len(self.parsedDoc.documents.keys()) == 0:
            return
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
                    if token in stop_word_list or len(token) < min_length_filter: 
                        continue
                    if token in self.tokens.keys():
                        self.tokens[token].append(int(doc))
                    else:
                        self.tokens.setdefault(token, [int(doc)])
        for token in self.tokens:
            self.tokens[token].sort()
                
                
        

if __name__=='__main__':
    min_length_filter=0
    stop_word_list = []
    if len(sys.argv) == 1:
        usage = 'Usage:\n\tpython3 Tokenizer.py filename [options]*'
        usage += '\n\toptions:\n\t\t--min-length-filter value\t(default: disabled)\n'
        usage += '\n\t\t--stop-word-list [value (, value)*]]\t(default: [])\n'
        print(usage)
    else:
        for arg_i in range(2, len(sys.argv) - 1):
            if arg_i % 2:
                continue
            if sys.argv[arg_i] == '--min-length-filter':
                min_length_filter = int(sys.argv[arg_i + 1])
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
        tokenizer = Tokenizer(sys.argv[1], min_length_filter, stop_word_list) 