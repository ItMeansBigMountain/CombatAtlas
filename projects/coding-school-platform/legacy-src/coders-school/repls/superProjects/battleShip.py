from random import randint

# TODO LIST
# Add label on coordinates
# Add different modes
# Add more things to the shop
# When Game Over appears or WIN appears then ask the player for which mode they want
# Make the home screen
# Error Check

bc = 10
 # keeps track of Battlecoins
multiplier = 1
turn_limit = 10
have_missile = False
missile_type = "normal"
have_torpedo = False
torpedo_type = "vertical"
have_radar = False
have_nuke = False
board = [] 
ship_rows = []
ship_cols = []
not_found = True
discount = False



discount_turns = 0


board_size = 10


def home_screen():
  print("""
 _           _   _   _           _     _       
| |         | | | | | |         | |   (_)      
| |__   __ _| |_| |_| | ___  ___| |__  _ _ __  
| '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
| |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |
|_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                        | |    
                                        |_|                                         
  """)
  play_again = raw_input("DO YOU WANT TO PLAY DOOD?!")
  if play_again == "yes":
    return True
  else:
    return False

for x in range(board_size):
  board.append(["O"] * board_size)

def print_board(board):
  for row in board:
    print (" ".join(row))



def random_row(board):
  return randint(0, len(board) - 1)

def random_col(board):
  return randint(0, len(board[0]) - 1)
for ws in range(5):
  ship_rows.append(random_row(board))
  ship_cols.append(random_col(board))

def hit():
  global bc
  global not_found
  not_found = False
  print ("Congratulations! You sunk my battleship! A+ for sinking my battleship dood! You will be moving on to College at Harvard University!!!!!")
  bc += (1 * multiplier)

def regenerate_ship(i):
  global ship_cols
  global ship_rows
  ship_rows[i] =  random_row(board)
  ship_rows[i] =  random_col(board)



def hir(x, y, w, h):
  for si in range(5):
    for i in range(x - (w / 2),x + (w / 2) + 1):
      for j in range(y - (h / 2),y + (h/2) + 1):
        if(i < len(board) and j < len(board) and i >= 0 and j >= 0):
          #print(str(x) + " " + y)
          if i == ship_rows[si] and j == ship_cols[si]:
            board[i][j] = "+"
            # Regenerate
            regenerate_ship(si)
            hit()
            #return
          elif board[i][j] != "+":
            #mark the square as an X
            board[i][j] = "X"

def check_win(board):
  for i in range(board_size):
    for j in range(board_size):
      if board[i][j] != 'X' and board[i][j] != '+':
        return False
    return True
      

ship_row = random_row(board)
ship_col = random_col(board)

# Everything from here on should go in your for loop!
# Be sure to indent four spaces!


while home_screen():
  print_board(board)
  turn = 0
  while(turn < turn_limit):
    print ("Turn", turn + 1, "of", turn_limit)
    turn += 1
    print(have_missile)
    print ("Currency is", bc, "Battlecoins")
    #get user input on the shop
    shop = raw_input("Would you like to go to the weapon shop BOISSS!")
    if shop == "yes":
      print("""
  1 - 2 Extra turns - 1 BC (Gives you 2 more turns)
  2 - 1 Missile - 2 BC (3x3 Blast)
  3 - Upgrade your Battlecoin multiplier - 3 BC (give + 1 BC per ship)
  4 - Shop discount for 2 turns - 4 BC (- 2 BC to everything in the shop [WARNING right after you buy this your discount starts])
  5 - Torpedo -  5 BC (10 x 1 Blast)
  6 - Dual missile - 7 BC (5x5 Blast)
  7 - Radar for 1 turn - 10 BC (show all ships for 1 turn)
  8 - Nuke - 12 BC (7x7 Blast)\n""")
      choice = raw_input("Which one you want to buy boissss! Remember use your money wisely dood!\n")
      if discount and discount_turns >0:
        bc += 2
        discount_turns -= 1
      if discount and discount_turns == 0:
        discount = False
      if choice == "1" and bc - 1 >= 0:
        turn_limit += 2
        bc -= 1 
      if not have_missile and choice == "2" and bc - 2 >= 0:
        have_missile = True
        bc -= 2
      if choice == "3" and bc - 3 >= 0:
        multiplier += 1
        bc -= 3 
      if not have_missile and choice == "6" and bc - 7 >= 0:
        have_missile = True
        missile_type = "dual"
        bc -= 7
      if not have_torpedo and choice == "5" and bc - 5 >= 0:
        have_torpedo = True
        bc -= 5
      if not have_radar and choice == "7" and bc -10 >= 0:
        have_radar = True
        bc -= 10
        print('\n ----Rows----')
        print(ship_rows)
        print(' ----Columns----')
        print(ship_cols)
        have_radar = False
      if not have_nuke and choice == "8" and bc -12 >= 0:
        have_nuke = True
        bc -= 12
      if not discount and choice == "4" and bc -4 >= 0:
        discount = True
        bc -= 4
        discount_turns = 2

        
    missile = "no"
    torpedo = "no"
    if have_missile:
      missile = raw_input("Would you like to use your missile dood yes or no?")
    
    if have_torpedo:
      torpedo = raw_input("Would you like to use your torpedo dood yes or no?")
    
    
    guess_row = int(raw_input("Guess Row: ")) - 1
    guess_col = int(raw_input("Guess Col: ")) - 1
    not_found = True

    if check_win(board):
      print("Yay you win so today you will able to get a job that pays a blillion dollars a day and you will get a Tesla and drivers license! ")

    if torpedo == "yes" and have_torpedo:
      direction = raw_input("Which direction would you like to blast your torpedo in boissssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss type vertical to make your torpedo to go vertical otherwise type horizontal for your torpedo to go horizontal   ")
      if direction == "vertical":
        hir(guess_row,guess_col, board_size * 2,1)
      else:
        hir(guess_row,guess_col, 1, board_size * 2) 

      have_torpedo = False

    elif missile == "yes"and have_missile:
      #variable missile_type tells us what missile we have
      if missile_type == "dual":
        hir(guess_row,guess_col, 5,5)
        missile_type = ""
      else:
        hir(guess_row, guess_col, 3, 3)
      have_missile = False 
    else:
      hir(guess_row,guess_col, 1, 1)
    if(not_found):
      if (guess_row < 0 or guess_row >= board_size) or (guess_col < 0 or guess_col >= board_size ):
        print ("Oops, that's not even in the ocean sucka! Man you should be very proud of yourself because... you got an F- !!.")
      else:
        print ("You missed my battleship booger face! Great job you got an F- for your aim!")
    else:
      print (not_found)
      # Print (turn + 1) here!
    print_board(board)

    if have_nuke:
      activate = raw_input("Say 'yes'  to activate your nuke boisssssssssssssss? If you don't want to activate your nuke say 'no'")
      if activate == "yes" and have_nuke:
        hir(4,4, 7, 7)
        have_nuke = False

        #replace pass with code
        #hir(location of nuke [center of screen])
        #blows up in the middle of the map

  #double check on radar to see if it always works or doesnt work

  print ("Game Over You will be going back to high school until you get better doii!")
















