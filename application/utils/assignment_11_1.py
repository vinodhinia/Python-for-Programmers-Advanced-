START = 32
END = 126

def GiveAscii(start = START,end=END):
    diff = start - end
    reminder = diff%4
    rows = int(diff / 4)
    x= start
    for y in range(0,rows):
        print(x," = ",chr(x),x+24," = ",chr(x+24),x+48," = ",chr(x+48),x+72, " = ",chr(x+96) )
        x +=1
    if reminder:
        print(x, " = ",chr(x),(x+24)," = ",chr(x+24),(x+48)," = ",chr(x+48))


def GiveAsciiChart(start = START, end = END):
    diff = end - start + 1
    cols = int(diff/4)
    charArr = []
    if(cols%4):
        cols +=1
    for row in range(cols):
        for column in range(4):
            entry = cols * column + row + start
            if entry > end:
                break
            charArr += ['{} = {}'.format(entry,chr(entry))]
            charArr += [' ']
        charArr += ['\n']
    return ''.join(charArr)


