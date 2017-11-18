while True:
    try:
        number_1 = int(input("Enter first Number"))
        break
    except ValueError:
        print("Please Try again")

while True:
    try:
        number_2 = int(input("Enterm the Second Number"))
        break
    except ValueError:
        print("Please try again")


if ((number_1 > number_2 and number_1%number_2) or (number_2> number_1 and number_2 %number_1)):
    print(number_1,"is a not multiple of",number_2)
else:
    print(number_1,"is a multiple of ",number_2)
