import matplotlib.pyplot as plt

def pie_chart():

  labels = 'jack', 'Hogs', 'Dogs', 'Affan'

  sizes = [150, 30, 45, 10]

  explode = (0.1, 0, 0, 0) 

  fig1, ax1 = plt.subplots()

  #this part of the code creates the graph
  ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
          shadow=True, startangle=90)
  ax1.axis('equal')

  plt.show()



def bar_graph():
  # creating the dataset 
  data = {'Python':100,'C':20, 'C++':75, 'Java':50} 


  programing_lang = list(data.keys()) 

  values = list(data.values()) 
    
  fig = plt.figure(figsize = (13, 10)) 
    
  # creating the bar plot 
  plt.bar(programing_lang, values, color ='red',  
          width = 0.2) 
    
  plt.xlabel("Programming Languages") 
  plt.ylabel("Ratings") 
  plt.title("Rating of different Programming Languages") 
  plt.show() 


def main_menu():
  print('1 - pie chart' )
  print('2 - bar graph' )

  option = int(input("Please choose a option: "))

  if option == 1:
    pie_chart()

  if option == 2:
    bar_graph()


main_menu()
