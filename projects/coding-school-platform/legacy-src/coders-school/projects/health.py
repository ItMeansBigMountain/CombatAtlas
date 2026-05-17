import numpy as np
import pandas as pd
import math
import datetime

def body_mass_index():
    weight = int(input('Please enter weight in pounds: '))
    height = int(input('Please enter height in inches: '))
    weight = weight * 703
    height = height * height
    bmi = weight/height
    print(bmi)
    return bmi

def water_calc():
    weight = int(input('Please enter weight in pounds: '))
    no_activity_oz = weight*.67
    no_activity_oz = math.ceil(no_activity_oz)
    s = {
        '0' : str(no_activity_oz)+'oz',
        '30': str(no_activity_oz+12)+'oz',
        '60': str(no_activity_oz+24)+'oz',
        '120': str(no_activity_oz+36)+'oz',
        '160' : str(no_activity_oz+48)+'oz'
        }
    s = pd.Series(s)
    print('\nOUNCES RECOMMENDED PER 30 MINUTES OF ACTIVITY\n')
    print(s.to_string())

def main():
    print('Welcome to the health app')
    print('1 : BMI calculator')
    print('2 : Water Calculator')
    option = int(input('Please choose an option!: '))
    if option == 1:
        body_mass_index()
    if option == 2:
        water_calc()

def save_BMI_data(weight, bmi ):

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)

    with open('user_BMI_data.txt', 'a', encoding='utf-8') as f:
        f.write(str(now))
        f.write('\n')
        f.write('\n')
        f.write(str(weight))
        f.write('\n')
        f.write('\n')
        f.write(str(bmi))
        f.write('\n')
        f.write('\n')
        f.close()



main()