#Print 1 - 255
def algo1():
  for i in range(1, 256, 1):
    print(i)

#Print all odd numbers from 1 - 255
def algo2():
  for i in range(1, 256, 2):
    print(i)

#Print the sum of all numbers from 1 - 255
def algo3():
  i = 0
  for x in range(1, 256, 1):
    i+=x 
  print(i)

#Print all values in array
def algo4():
  arr = [1, 13, 18, 24, 29, 47, 53, 78, 91, 102,60,9,5,4]
  #SUBSCRIPT EXAMPLE
  #print(arr[5]) 
  #^^ prints "47" ^^
  for i in range(0, len(arr),1):
    print(arr[i])
    
#find the max value inside the array
def algo5():
  arr = [1, 13, 18, 24, 29, 47, 53, 78, 91, 102,60,9,5,4]

  max_val = 0
  for i in range(0, len(arr), 1):
    if arr[i] > max_val:
      max_val = arr[i]
  print(max_val)

  #SHORTCUT
  print(max(arr))


# print the average of the array
def algo6():
  arr = [1, 13, 18, 24, 29, 47, 53, 78, 91, 102,60,9,5,4]

  arr_sum = 0
  for x in range(1, len(arr), 1):
    arr_sum  +=   arr[x] 
    
  average = arr_sum / len(arr) 
  print(average)
  

# push all odd numbers from 1-255 into an array
def algo7():
  arr = []
  print(arr)
  for i in range(1, 256, 2):
    arr.append(i)
  print(arr)


#square all values inside of an array
def algo8():
  arr = [1, 13, 18, 24, 29, 47, 53, 78, 91, 102,60,9,5,4]

  #iterate through the array
  for x in range(0,len(arr), 1):
    #square each value of the array
    arr[x] = arr[x] * arr[x]

  print(arr)


#print how many items are bigger than a number (y)
def algo9():
  arr = [1, 130, 18, 240, 29, 47, 53, 78, 91, 102,60,9,5,4]
  y = 100
  count = 0
  #iterate through the array
  for x in range(0, len(arr), 1):
    if arr[x] > y:
      print(arr[x])
      count = count + 1
  print("Numbers bigger than "+ str(y) + ": ", count)
    
#  turn all negative numbers in array to zero
def algo10():
  arr = [-1, -130, 18, 240, 29, -47, 53, 78, 91, -102,60,9,-5,4]
  for x in range(0, len(arr), 1):
    if arr[x] < 0:
      arr[x] = 0
  print(arr)


#print the MIN , MAX , AVERAGE of an array
def algo11():
  arr = [-1, -130, 18, 240, 29, -47, 53, 78, 91, -102,60,9,-5,4]
  minimum = 0
  maximum = 0
  total = 0
  average = 0

  #iterate through the array
  #add all the numbers up and find our average
  #find the max
  #find the min

  for x in range( len(arr) ):
    total += arr[x]
    if arr[x] < minimum:
      minimum = arr[x]
    if arr[x] > maximum:
      maximum = arr[x]
    
  average = total / len(arr)

  print("average: " + str(average))
  print("minimum: " + str(minimum))
  print("maximum: " + str(maximum))


#shift array values to the right and first value becomes zero
def algo12():
  arr = [-1, -130, 18, 240, 29, -47, 53, 78, 91, -102,60,9,-5,4]
  print(arr)

  for x in range(0, len(arr) -1 , 1):
    arr[x] = arr[x+1]
  
  arr[len(arr)-1] = 0
  print(arr)


  #coding fundementals
  #loops
  #variables
  #[arrays] 
  #{dictionaries}
  # (tuples)


