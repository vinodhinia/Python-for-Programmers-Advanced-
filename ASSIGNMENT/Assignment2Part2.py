import string
def palindrome(input):
    input = input.lower()
    input.replace(' ','')
    if input == input[::-1]:
        exclude = set(string.punctuation)
        return ''.join(c for c in input if c not in exclude)
    return None