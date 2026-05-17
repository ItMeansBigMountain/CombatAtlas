print("WELCOME TO OMEGA")
import requests #lets us go onto a website



this = requests.get('http://www.recipepuppy.com/api/?i=onions,garlic&q=omelet&p=3')

NVIDJFBFXGCABFSZA = this.text

print(NVIDJFBFXGCABFSZA)

