import os
sourceDir = '/Users/vino/workspace/documentClassifier/SharedFile/sample/'
uploadFileNames = []
dirpath=""
# for (sourceDir, dirname, filename) in os.walk(sourceDir):
#     for dir in dirname:
#         for file in filename:
#             if filename:
#
#                 filePath = os.path.abspath(file)
#                 print(filePath)


for dirpath,dirs,filenames in os.walk(sourceDir):
    for dir in dirs:
        print(dir)
        if os.path.i
            print("Directory Exists")
    # for f in filenames:
    #     path = os.path.abspath(os.path.join(dirpath, f))
    #     path = path.replace("/Users/vino/workspace/documentClassifier/SharedFile","")
    #     print(path)
#
