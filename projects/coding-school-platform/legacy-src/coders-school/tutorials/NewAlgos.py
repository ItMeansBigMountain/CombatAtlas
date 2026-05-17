'''
#skip
def evaluate():
    print('PROBLEM 1')
    numbers = []
    x= float( input("Please enter value of - X : ")  )
    numbers.append(x)
    y= float( input("Please enter value of - Y : ")  )
    numbers.append(y)
    z= float( input("Please enter value of - Z : ")  )
    numbers.append(z)

    print(    "\nYou have entered: \nX - {} \nY - {}  \nZ - {} ".format(x,y,z)    )

    avg = sum(numbers) / len(numbers)
    guess = float( input("Please enter what you think the average of X , Y , & Z is going to be: ") )

    if guess == avg :
        print('\n\nGOOD JOB!')
    else:
        print('\n\nYour average is in-correct')
        print('The correct average is {}'.format(avg)  )
    

    print(  'Min: {}'.format(min(numbers))   )
    print( 'Max: {}'.format(max(numbers))   )

def printDigits(num):
    if num < 10:
        print(num)
    else:
        printDigits(num // 10)
        print(num % 10)

#PROBLEM 1
evaluate() 

# PROBLEM 2
num = int(input("Enter n: "))
printDigits(num)
'''






def returnN( s , n ):
    if n > len(s):
        print("number bigger than string")
    else:
        print(s[:n]) 

def weekPay(rate , hours):
    #overtime is 1.5
    overtime = 0
    pay = 0
    if hours >40:
        overtime = hours - 40
        hours -= overtime
        
        overtime = overtime * 1.5

        pay += (rate *overtime) + (rate * hours)

        print('WEEKLY PAYMENT: ' +  str(pay))

    else:
        pay = rate * hours
        print('WEEKLY PAYMENT: ' +  str(pay))

def partition(lst , let1 , let2 ):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    let1 = let1.lower()
    let2 = let2.lower()


    for x in range(len(lst)):
        firstLetter = lst[x][0]
        firstLetter = firstLetter.lower()

        if alphabet.index(  firstLetter ) >= alphabet.index(let1) and alphabet.index(  firstLetter) <= alphabet.index(let2):
            print(lst[x]) 




# PROBLEM 3
returnN('hello world' , 5) 

# PROBLEM 4
weekPay(10 , 41)

# PROBLEM 5
partition(['abdur' , 'Timmy' , 'mike' , 'rachel' , 'Larry' , 'Amy', 'bob' , 'zenaido'] , 'r' , 'z')
