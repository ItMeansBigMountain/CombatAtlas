from  gtts import gTTS
from random_word import RandomWords

#option 1
def ABC_speech():
  MYTEXT='A B C D E F G H I J K L M N O P Q R S T U V W X Y AND Z NOW I KNOW MY ABCS NEXT TIME WONT YOU SING WITH ME'
  language = 'en'
  say = gTTS(text = MYTEXT, lang = language, slow = True )
  say.save("welcome.mp3")



#option 2
def text_speech():
  MYTEXT=input('please enter words: 🆒')
  language = 'en'
  say = gTTS(text = MYTEXT, lang = language, slow = True )
  say.save("welcome.mp3")



#option 3
def secret_speech():
  r = RandomWords()
  MYTEXT='minecraft has a new update!!!!!'
  print(MYTEXT)
  language = 'en'
  say = gTTS(text = MYTEXT, lang = language, slow = True )
  say.save("welcome.mp3")



def mainmenu():
  print('welcome to text to sayyyyyyyy!!!!!!!\n')
  print('1 - Computer will say the ABCs')
  print('2 - text your own')
  print('3 - you get to hear a secret\n')
  option = input('Please choose an option!: ')
  
  if option == '1':
    ABC_speech()

    
  if option == '2':
    text_speech()
  
    
  if option == '3':
    secret_speech()




mainmenu()