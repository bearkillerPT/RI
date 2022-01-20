#Gil Teixeira - 88194
import sys

class Parser:
    def __init__(self, dataFileName=None):
        if not dataFileName:
            dataFileName = 'amazon_reviews_us_Camera_v1_00.tsv'
        try:
            self.dataFile  = open(dataFileName, encoding="utf-8")
        except Exception as e:
            self.dataFile = None
            print(e)
        #if self.dataFile:
            #self.parseDataFile()

    def parseAndYield(self):
        self.documents = {}
        self.headerData = []
        if self.dataFile == None:
            return None
        header = self.dataFile.readline().split('\t')
        for header_id in header:
            self.headerData.append(header_id.replace('\n', ''))
        while data := self.dataFile.readline().split('\t'):
            if not data or data==['']:
                break
            if len(data) != len(self.headerData):
                continue
            doc_id_i = self.headerData.index('customer_id')
            prod_title_i = self.headerData.index('product_title')
            review_headline_i = self.headerData.index('review_headline')
            review_body_i = self.headerData.index('review_body')
            review = {
                    'doc': data[doc_id_i],
                    'product_title': data[prod_title_i],
                    'review_headline': data[review_headline_i],
                    'review_body': data[review_body_i]
                }
            yield review
        

    def parseDataFile(self):
        self.documents = {}
        self.headerData = []
        header = self.dataFile.readline().split('\t')
        for header_id in header:
            self.headerData.append(header_id.replace('\n', ''))
        while data := self.dataFile.readline().split('\t'):
            if not data or data==['']:
                break
            if len(data) != len(self.headerData):
                continue
            doc_id_i = self.headerData.index('customer_id')
            prod_title_i = self.headerData.index('product_title')
            review_headline_i = self.headerData.index('review_headline')
            review_body_i = self.headerData.index('review_body')
            review = {
                    'product_title': data[prod_title_i],
                    'review_headline': data[review_headline_i],
                    'review_body': data[review_body_i]
                }
            if data[doc_id_i] not in self.documents.keys():
                self.documents[data[doc_id_i]] = [review]
            else:
                self.documents[data[doc_id_i]].append(review)



if __name__=='__main__':
    if len(sys.argv) == 1:
        usage = 'Usage:\n\t python3 Parser.py filename'
        print(usage)
    elif len(sys.argv) == 2:
        a = Parser(dataFileName=sys.argv[1])
        print(a.documents)
    