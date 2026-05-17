import datetime


def body_fat_detector():
  weight=float(input("please enter your weight: "))
  height=float(input("please enter height in inches: "))
  bmi=(weight*703)/ (height * height)
  print(bmi)
  return bmi



def water_calculator():
  weight=float(input("please enter your weight: "))
  ounces=weight*.67 
  gallons=ounces*.0078125
  print(gallons)
  return ounces


def save_data():
  now=datetime.now()
  current_time=now.strftime("%H:%M:%S")
  with open("weightdata.txt", "a",encoding ="utf-8") as f:
    f.write(str(current_time))
    


    
def main_menu():
  print("\n1 - body fat detector ")
  print("2 - water calculator : calculats how much water ")
  option=input("please enter an option: ")
  
  if option=="1":
    body_fat_detector()
  if option=="2":
    water_calculator()
  else:
    print("invalid option")
    main_menu()

main_menu()