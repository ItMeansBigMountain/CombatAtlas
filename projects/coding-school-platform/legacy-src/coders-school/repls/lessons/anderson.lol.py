#AVERAGE - DEFINITION
#average means to add all the numbers up, then divide by how many numbers there are
#also known as "mean"



# print AVERAGE of array filled with numbers
def algo6():
  #create an array that hold our data yeah and stuff like that
  scores = [75,80,100,90 ]
  
  #first this must equal 0 so that we can add to it...and stuff like that
  total = 0

  #go through each value in "scores" by using "x" and stuff like that
  for x in scores:
    total = total + x

  average = total / len(scores)
  print( "the average score is : " , average, "and stuff like that")




#print all odd numbers in the array
def algo7():
  arr = [75,1,3,7,9,63,12,10,9,8,5,4,0]

  #go through the array and see if the number is odd and stuff like that
  for x in arr:
    #remove if "x" is odd and stuff like that
    if x % 2 != 0:
      print(x, "and stuff like that")






#square array values and stuff like that
def algo8():
  lists = [75,11,34,76,0,63,12,10,9,8,5,4,0]
  newlistsandstufflikethat = []
  for y in lists:
    y =  y * y
    newlistsandstufflikethat.append(y)
  print (newlistsandstufflikethat)


def algo9():
  numb = 100
  count = 0
  ANDSTUFFLIKETHAT = [99,98,97,96,95,199,198,197,196,195]
  for z in ANDSTUFFLIKETHAT:
    if z > numb:
      count += 1
      print(str(z) +" is greater than and stuff like that  " + str(numb))

  print(count)


def andstufflikedaaat():
  hobbies = ["do nothing","sleep","not write"]
  for anything in hobbies:
    print ("I like to " + anything + " and stuff like that...")

  for loop in range(9999):
    print( 
    '''

                      .___           __            _____   _____  .__   .__  __               __   .__              __   
  _____     ____    __| _/   _______/  |_  __ __ _/ ____\_/ ____\ |  |  |__||  | __  ____   _/  |_ |  |__  _____  _/  |_ 
  \__  \   /    \  / __ |   /  ___/\   __\|  |  \\   __\ \   __\  |  |  |  ||  |/ /_/ __ \  \   __\|  |  \ \__  \ \   __\
  / __ \_|   |  \/ /_/ |   \___ \  |  |  |  |  / |  |    |  |    |  |__|  ||    < \  ___/   |  |  |   Y  \ / __ \_|  |  
  (____  /|___|  /\____ |  /____  > |__|  |____/  |__|    |__|    |____/|__||__|_ \ \___  >  |__|  |___|  /(____  /|__|  
      \/      \/      \/       \/                                               \/     \/              \/      \/       

    '''
      ) 
    




#turn any negative number into 0 inside the array
def algo10():
  box = [10,-90,50,-60,70,-100]
  print "Before: ", box

  







#calling functions here
algo10()

