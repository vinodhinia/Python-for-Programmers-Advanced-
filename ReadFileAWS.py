import magic
import Enum
import boto3
import boto
import requests
from botocore.client import Config
import magic
from tesserocr import PyTessBaseAPI, RIL
import subprocess
import os,sys
import json
import PyPDF2

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

def classifier(file, file_name):
    fileType = identifyFileType(file)
    file_classification=analyser(fileType,file)
    result[file_name] = file_classification
    json_data = json.dumps(result)

def identifyFileType(file):
    mimeType = magic.from_file(file,mime=True)
    index = mimeType.index('/')
    fileType = mimeType[index+1:len(mimeType)]
    # print (fileType)
    return fileType

def analyser(fileType,file):
    file_classification = ""
    if fileType=='pdf':
        try:
            pdfReader = PyPDF2.PdfFileReader(open(file, 'rb'))
        except PyPDF2.utils.PdfReadError:
            print("Invalid PDF File")
            pass

        if(pdfReader.isEncrypted):
            file_classification = "Password Protected"
        else:
            file_classification = pdfAnalyser(file)
    elif fileType in imageTypes:
        file_classification = imageAnalyser(file)
    return file_classification

def pdfAnalyser(file):
    process = subprocess.Popen(['/usr/local/bin/pdftotext',  file , '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    parsedText, err = process.communicate()
    parsedText = parsedText.decode("utf-8", 'backslashreplace')
    # import pdb;pdb.set_trace()
    if (len(parsedText)):
        if classifyFile(bankTransactionStatement,parsedText):
            return "Bank Statement"
        elif classifyFile(w2FormElements,parsedText):
            return "W-2 Forms"
    else:
        print("Unable to read the file")

def imageAnalyser(file):
    with PyTessBaseAPI() as api:
        api.SetImageFile(file)
        parsedText = api.GetUTF8Text()
        if classifyFile(bankTransactionStatement,parsedText):
            return "Bank Statement"
        elif classifyFile(w2FormElements,parsedText):
            return "W-2 Forms"

def classifyFile(list, fileContent):
    for item in list:
        if item in fileContent.lower():
            return True
    return False

LOCAL_PATH = "/Users/vino/Test/"
for file_key in b.list():
    file_name = os.path.basename(file_key.name)
    if file_key.name != '.DS_Store':
        url = client.generate_presigned_url(ClientMethod='get_object',Params={'Bucket': bucket,'Key': file_key.name}, ExpiresIn=expiry)
        r = requests.get(url, stream=True)
        content = r.content
        file_key.get_contents_to_filename(LOCAL_PATH + file_name)
        classifier(LOCAL_PATH + file_name, file_name)
        os.remove(LOCAL_PATH + file_name)



class DocumentClassifier(Enum):
    BANK_INTREST_STATEMENT = 1
    BANK_TRANSACTION_STATEMENT = 2
    TAX_RETURN = 3
    W2 = 4
    PASSPORT = 5
    DRIVING_LICENSE = 6
    STATE_ID = 7
    SOCIAL_SECURITY_CARD = 8
    FORM_1095C_HEALTH_INSURANCE =9
    FORM_1090_TUTION_STATEMENT = 10
