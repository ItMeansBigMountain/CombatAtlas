# GIVEN A SENTANCE... WE NEED TO SCORE THE WORDS AND RETURN THE HIGHEST SCORED WORD....
# The scoring of words will be judged depending on the position of each letter within the alphabet

# RULES
# save capitalization
# check for special chars
# get the score non caps bias


# What was the person thinking when they discovered cow's milk was fine for human consumption... and why did they do it in the first place!?
# ANSWER = consumption

ALPHAbet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def word( putin : str ):
  # separate into words
  # calculate the score
  # figure out the word with the highest score
  # return that as it was originally

  score = 0
  temp = 0
  gw = '0'
  arr = putin.split( " " )
  print(arr , '\n\n\n\n\n')
  # EVERY WORD
  for ayl in arr:
    temp = 0
    #EVERY LETTER IN EVERY WORD
    for ayl2 in ayl:
      # checking alpha
      if ayl2.isalpha():
        for l in range( 0  ,  len(ALPHAbet) , 1  ):
          if ayl2.lower() == ALPHAbet[l]:
            temp += l+1
      else: 
        print(  f'{ayl2} beat the system'   )
      # CHECKING FOR THE SCORE 
      if temp > score:
        score = temp
        gw = str(  ayl   )
  # we need to check if gw has people who beat the system
  for xylozone in range(len(gw)):
      if gw[xylozone].lower() not in ALPHAbet:
        print(gw[xylozone])
        break
  gw = gw[:xylozone] #!
      
  

  print("         /\\        ")
  print(" And the word with the greatest score is... ")
  print(gw)

#print("sentence to be checked?")
#lol = input("")
# calling functions down here
lolol = "What was the person thinking when they discovered cow's milk was fine for human consumption... and why did they do it in the first place!?"
word(lolol)