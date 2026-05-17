import time
import random


def test():
    time.sleep(1)

    answers = []

    print('OK heres the test... \n')


    time.sleep(1)
    right_answer = 2
    print('\nWhat is my favorite food?\n')
    time.sleep(1)
    print('1: Pizza')
    print('2: Steak')
    print('3: Eggs')
    print('4: Cheese')
    option1 = int(input('Please choose an option: '))
    if option1 == right_answer:
        print('RIGHT')
        answers.append('RIGHT')
    else:
        answers.append('WRONG')




    time.sleep(1)
    right_answer = 4
    print('\nWhat is my favorite music?')
    time.sleep(1)
    print('1: Electric')
    print('2: Jazz')
    print('3: Rock')
    print('4: Classical')
    option2 = int(input('Please choose an option: '))
    if option2 == right_answer:
        print('RIGHT')
        answers.append('RIGHT')
    else:
        answers.append('WRONG')




    time.sleep(1)
    right_answer = 4
    print('\nWhat is my favorite number?')
    time.sleep(1)
    print('1: 999')
    print('2: 7')
    print('3: 0')
    print('4: 777')
    option3 = int(input('Please choose an option: '))
    if option3 == right_answer:
        print('RIGHT')
        answers.append('RIGHT')
    else:
        answers.append('WRONG')




    time.sleep(1)
    right_answer = 2
    print('\nWhat is my favorite color?')
    time.sleep(1)
    print('1: Red')
    print('2: Green')
    print('3: Gray')
    print('4: Blue')
    option4 = int(input('Please choose an option: '))
    if option4 == right_answer:
        answers.append('RIGHT')
    else:
        answers.append('WRONG')
    
    return answers



print('hello world! NICE TO MEET YOU!?\n')
time.sleep(1)

print('OH ok! umm...\n')
time.sleep(2)

name = input('Whats your name again...: ')
time.sleep(1)

print('OH THATS RIGHT!', name+'!\n')
time.sleep(1)

print('welp. do you really know me? ...\n')
time.sleep(1.5)

knowme = int(input('1: "YES"    2: "NO" \n  '))
if knowme == 1:
    print('Great so you would know my favorite number!?')
    number = random.randint(0,999)
    fav_num = int(input('Whats my favorite number?:  '))
    time.sleep(2)
    if fav_num == number:
        print('\nwow...I love you')
    else:
        print('\nHOW COULD YOU LIE TO ME!')
        print('MY FAVORITE NUMBER IS', number)
        print('I NEED TO RETEST YOUR KNOWLAGE!!!!!!')
        quiz = test()

if knowme == 2:
    print('Well im gonna test you anyways...')
    quiz = test()

else:
    print('that wasnt an option but..... heres the test anyways')
    quiz = test()

print(quiz)