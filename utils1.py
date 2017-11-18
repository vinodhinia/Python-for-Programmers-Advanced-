import magic
import nltk
import boto3
import boto
import requests
from botocore.client import Config
import magic
from tesserocr import PyTessBaseAPI, RIL
import subprocess
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import os,sys
import json
import PyPDF2
from shutil import copyfile
from nltk.util import ngrams as nltk_ngrams
# from document_classifier.models import ClassifierResult

AWS_ACCESS_KEY_SECRET = 'S6Yz2L1a4/aJq4Th5Mrts4ddbX0gmHLPKIfHsDIO'
AWS_ACCESS_KEY_ID = 'AKIAJMENREMHZ4LTTHXA'
S3_REGION='us-west-2'
bucket_name = 'dump-fileit-client-2016-as-of-20170413'

client = boto3.client(aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_ACCESS_KEY_SECRET,
                              region_name=S3_REGION, service_name='s3',
                              config=Config(s3={'addressing_style': 'path'}))

bucket = 'dump-fileit-client-2016-as-of-20170413'

conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY_SECRET)

expiry = 3600
b = conn.get_bucket(bucket_name)

imageTypes = ['jpg', 'jpeg', 'tif', 'gif', 'bmp']

docTypes = ['doc','docx']

bankTransactionStatement = [
    'transaction','payments','transfers','account summary',
    'deposits','withdrawals', 'account statement','balance',
    'account name','account type','account','transfers'
]
w2FormElements = [
        'form','form w—2 wage', 'w 2','social','secutriy'
        'wage and tax','tax','federal','eid','return','employee',
        'employeridnumber', 'Dept. of the Treasury','w-2','earnings'
    ]

result = {}


class DocumentClassifier(object):

    def classifier(self,file, file_name):
        fileType = self.identifyFileType(file)
        parsedText=self.analyser(fileType,file)
        # print(file_classification)
        # result[file_name] = file_classification
        # json_data = json.dumps(result)
        return parsedText


    def identifyFileType(self,file):
        mimeType = magic.from_file(file,mime=True)
        index = mimeType.index('/')
        fileType = mimeType[index+1:len(mimeType)]
        # print (fileType)
        return fileType

    def analyser(self,fileType,file):
        file_classification = ""
        if fileType=='pdf':
            parsedText = self.pdfAnalyser(file)
        elif fileType in imageTypes:
            parsedText = self.imageAnalyser(file)
        return parsedText

        # ClassifierResult.objects.create(validationmessage=validation_message, isValid=isValid,categorization=categorization)
        # ClassifierResult.save()

    def pdfAnalyser(self,file):
        process = subprocess.Popen(['/usr/local/bin/pdftotext',  file , '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        parsedText, err = process.communicate()
        parsedText = parsedText.decode("utf-8", 'backslashreplace')
        dst = "/Users/vino/SampleData/Parse/"
        print(file)
        # if (len(parsedText) > 10):
            # copyfile(file, dst+os.path.basename(file))
        return parsedText
        # else:
        #     self.checkIfScannedImage(file)

    def parsePDfText(self, file):
        import codecs
        process = subprocess.Popen(['/usr/local/bin/pdftotext', file, '-'], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        parsedText, err = process.communicate()
        parsedText = parsedText.decode("utf-8", 'backslashreplace')
        #file_contents = codecs.open(file, "r", encoding='utf-8', errors='ignore').read()

        tokens = nltk.word_tokenize(parsedText)
        # sentence_tokenize =nltk.sent_tokenize(parsedText)
        return tokens

    def removePunuationandStopWrds(self, parsedText):
        parsedText = parsedText.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        token = tokenizer.tokenize(parsedText)
        filtered_words = [w for w in token if not w in stopwords.words('english') ]
        token = nltk.word_tokenize(filtered_words)
        return " ".join(filtered_words)


    def checkIfScannedImage(self,file):
        import pdb;
        pdb.set_trace()
        index = file.rfind(".")
        if index != -1:
            dest_filename = file[:index]
            dest_filename = dest_filename + '.jpg'
            my_env = os.environ.copy()
            my_env["PATH"] = "/usr/local/bin:" + my_env["PATH"]
            process = subprocess.Popen(['convert', file, dest_filename], env=my_env)
            self.imageAnalyser(dest_filename)


    def imageAnalyser(self,file):
        import pdb;pdb.set_trace()
        with PyTessBaseAPI() as api:
            api.SetImageFile(file)
            parsedText = api.GetUTF8Text()
            # print(parsedText)
            return parsedText

    def classifyFile(self,list, fileContent):
        for item in list:
            if item in fileContent.lower():
                return True
        return False

    def runClassifier(self):
        LOCAL_PATH = "/Users/vino/Test/"
        for file_key in b.list():
            file_name = os.path.basename(file_key.name)
            if file_key.name != '.DS_Store':
                url = client.generate_presigned_url(ClientMethod='get_object',Params={'Bucket': bucket,'Key': file_key.name}, ExpiresIn=expiry)
                r = requests.get(url, stream=True)
                content = r.content
                file_key.get_contents_to_filename(LOCAL_PATH + file_name)
                self.classifier(LOCAL_PATH + file_name, file_name)
                os.remove(LOCAL_PATH + file_name)

    def runLocalClassifier(self):
        LOCAL_PATH = "/Users/vino/SampleData/W2Forms/"
        for fileName in os.listdir(LOCAL_PATH):
            self.classifier(LOCAL_PATH+fileName, fileName)

    def docCategories(self):
        category_list = ['Bank Statement', 'W2 Form', 'Bank Intrest Statement', 'Driving License', 'Passport', '1095C', 'Tax Return']
        return category_list

    def common_ngram_txt(self,tokens1, tokens2, size=15):
        print('Checking ngram length {}'.format(size))
        ng1 = set(nltk_ngrams(tokens1, size))
        ng2 = set(nltk_ngrams(tokens2, size))

        match = set.intersection(ng1, ng2)
        print('..found {}'.format(len(match)))

        return match

    def trainClassifier(self):
        LOCAL_PATH = "/Users/vino/SampleData/Parse/"
        train = []
        for fileName in os.listdir(LOCAL_PATH):
            parsedText = self.classifier(LOCAL_PATH+fileName, fileName)
            train.append((parsedText , "W2 Form"))


#doc = DocumentClassifier()
#doc.runLocalClassifier()
# doc.pdfAnalyser("/Users/vino/SampleData/W2Forms/Invesco W-2.pdf")
