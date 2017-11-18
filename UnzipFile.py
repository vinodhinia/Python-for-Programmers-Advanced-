import zipfile
import os

dir_path = "/Users/vino/workspace/documentClassifier/SharedFile/data/"
dest_file_path = "/Users/vino/workspace/documentClassifier/SharedFile/client/"
files_list = os.listdir(dir_path)
count =0
for file in files_list:
    # import pdb;pdb.set_trace()
    dest_file_name = os.path.splitext(file)[0]
    iszip = os.path.splitext(file)[1]

    # print(dest_file_name)
    zip_file_path = dir_path+file
    print(zip_file_path)
    # import pdb;pdb.set_trace()
    if(iszip == '.zip'):
        print("It is a zip file")
        try:
            # import pdb;pdb.set_trace()
            # zipfile.ZipFile(zip_file_path,'r')
            # zip_ref = zipfile.ZipFile(zip_file_path)
            if not os.path.exists(dest_file_path + dest_file_name):
                os.makedirs(dest_file_path + dest_file_name)
                import pdb;pdb.set_trace()
                zip_ref = zipfile.ZipFile(zip_file_path)
                zip_ref.extractall("/Users/vino/workspace/documentClassifier/SharedFile/client/" + dest_file_name)
                zip_ref.close()
        except zipfile.BadZipFile:
            pass
    else:
        count = count +1
        # import pdb;pdb.set_trace()
        # os.remove(dir_path+file)
        print("Its not a zip file")

    print (count)





#
# zip_ref = zipfile.ZipFile("/Users/vino/workspace/documentClassifier/SharedFile/data"+"/Abdul Latiff, Khadijah (6597).zip")
# if not os.path.exists("/Users/vino/workspace/documentClassifier/SharedFile/UnzipData"+"Abdul Latiff, Khadijah (6597)"):
#     os.makedirs("/Users/vino/workspace/documentClassifier/SharedFile/UnzipData/"+"Abdul Latiff, Khadijah (6597)")
#     zip_ref.extractall("/Users/vino/workspace/documentClassifier/SharedFile/UnzipData/"+"Abdul Latiff, Khadijah (6597)")
#     zip_ref.close()
