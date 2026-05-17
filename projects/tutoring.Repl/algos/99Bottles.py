for i in range( 99, -1 , -1 ):
  if  i > 1 :
    print(f"{i} bottles of beer on the wall,\n{i} bottles of beer.\nTake one down, pass it around,\n{i-1} bottles of beer on the wall.\n\n")
  else: 
    if i == 0:
      print("1 bottle of beer on the wall,\n 1 bottle of beer. Take one down,\n pass it around,\n 1 bottle of beer on the wall.\n\n")
      print( "No bottles of beer on the wall, no bottles of beer. It's closing time.")
  