import string
START = 32
END = 126

def palindrome(input):
    input = str(input)
    input = input.lower()
    input = input.replace(' ','')
    if input == input[::-1]:
        exclude = set(string.punctuation)
        return ''.join(c for c in input if c not in exclude)
    return None


def main():
    DATA = ('Murder for a jar of red rum','12321','nope','abcbA',3443,'what','Never odd or even','Rats live on no evil star')
    for input in DATA:
        result = palindrome(input)
        if result:
            print(input," --> ",result)


if __name__ == '__main__':
    main()