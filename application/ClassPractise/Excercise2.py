while True:
    try:
        number =  int(input("Enter the Number"))
        break
    except ValueError:
        print("Please try again later")

print("Octal value = ",oct(number))
print("Hexa Decimal Value =",hex(number))