from utils.assignment_11_2 import palindrome
import os

# starting_directory = input("Enter the starting directory")
STARTING_DIRECTORY = "/Users/vino/Assingment2/"


def ReadPlaindrome():
    palindrome_dict = {}
    for filename in os.listdir(STARTING_DIRECTORY):
        file = os.path.join(STARTING_DIRECTORY, filename)
        if filename not in '.DS_Store':
            with open(file) as f:
                for lines in f:
                    lines = lines.replace('\n','')
                    if palindrome(lines):
                        if lines in palindrome_dict:
                            palindrome_dict[lines] += 1
                        else:
                            palindrome_dict[lines] = 1

    return palindrome_dict



if __name__ == '__main__':
    dict = ReadPlaindrome()
    for key,value in dict.items():
        print(key,"in",value,"files")