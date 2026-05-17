
const random = require('random')
var answers = [
    'function',
    'console',
    'Desktop',
    'loop',
    'acceptable',
    ' Java Script',
    'Chair',
    'gossip',
    'mystify',
    'vortex',
    'xylophone',
    'wizard',
    'jackpot',
    'joyful',
    'jigsaw',
    'luxury',
    'kiwi',
    'jazzy',
    'saxophone',
    'Chair',
]





count = 0
word = answers[random.int(min = 0, max = answers.length)]
str = '________________________'
var lengthWORD = word.length
var lengthSTR = str.length
var shave = lengthSTR - lengthWORD
str = str.substring(lengthWORD, -1)
index = 0;
while (count < 8) {
    guess = prompt('Guess a letter?')
    if (word.indexOf(guess) >= 0) {
        console.log('That is correct!')
        index = word.indexOf(guess)
        str = str.substring(0, index) + guess + str.substring
            (index + 1);
        console.log(str)
        if (str == word) {
            console.log('You win! The word was ' + str)
            break
        }
    }

    else {
        count++
        console.log('You have guessed' + ' ' + count + ' ' + 'letters wrong')
        if (count == 8) {
            console.log('You lose!')
        }
    }
}