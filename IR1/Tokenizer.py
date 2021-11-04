import sys
import Parser

from Parser import Parser
class Tokenizer:
    def __init__(self, filename):
        self.parsedDoc = Parser(filename)
        if len(self.parsedDoc.documents.keys()) == 0:
            return
        

if __name__=='__main__':
    min_length_filter = 0
    stop_word_list = []
    if len(sys.argv) == 1:
        usage = 'Usage:\n\tpython3 Tokenizer.py filename [options]*'
        usage += '\n\toptions:\n\t\t--min-length-filter value\t(default: disabled)\n'
        usage += '\n\t\t--stop-word-list [value (, value)*]]\t(default: [])\n'
    else:
        for arg_i in range(1, len(sys.argv) - 1):
            if arg_i % 2:
                continue
            if sys.argv[arg_i] == '--min-length-filter':
                min_length_filter = sys.argv[arg_i + 1]
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

    print(min_length_filter)
    print(stop_word_list)