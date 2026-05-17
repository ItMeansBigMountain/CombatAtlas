import numpy as np
import pandas as pd
import math

def body_mass_index():
    weight = float(input('Please enter weight in pounds: '))
    height = float(input('Please enter height in inches: '))
    weight = weight * 703
    height = height * height
    bmi = weight/height
    print(bmi)
    return bmi

def water_calc():
    weight = float(input('Please enter weight in pounds: '))
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

    option = float(input('Please choose an option!: '))
    if option == 1:
        body_mass_index()
    if option == 2:
        water_calc()



main()