#Number game - Guess a number between 0 to 10
print("Guess a number between 0 to 10")

guess=0
high = 10
low =0
while(high >low):
    guess +=1
    guess = (high+low)/2
    print("Is the number",guess)
    while True:
        answer = input("If the answer is right enter \n"
                       "Y for Yes\n"
                       "N for No")
        if answer == 'Y' or answer =='y':
            print("Our guess is right")
            break
        else:
            high_or_low = input("Is the number high or low than my guess press \n"
                                "H if it is high\n"
                                "L if it is Low")
            if(high_or_low == 'H' or high_or_low == 'h'):
                guess = guess - 1
