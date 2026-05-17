import requests
from bs4 import BeautifulSoup
import json





# INITIALIZE VARIABLES
output = {
    'Abs' : [],
    'Arms' : [],
    'Back' : [],
    'butt-hips' : [],
    'Chest' : [],
    'full-body-integrated' : [],
    'legs-calves-and-shins' : [],
    'Neck' : [],
    'Shoulders' : [],
    'legs-thighs' : [],
}

base_url = 'https://www.acefitness.org/resources/everyone/exercise-library/body-part/'






# loop through body parts
for slug in output:
    print("searching: " , slug , "...")

    # fetch data page 1
    data = requests.get( base_url + slug )
    page = 1
    repeats = 0
    repeat_threashold = 20
    
    # while no duplicates
    end = False
    while not end:
        # convert html into soup
        html_data = BeautifulSoup( data.text , features="html.parser" )
        
        # search / loop  soup for workout titles
        page_exercises = html_data.findAll( class_ = "exercise-card-grid__cell" )  
        for e in range(0 , len(page_exercises) , 1):
            title = page_exercises[e].find(class_ = "exercise-card__title").get_text(strip=True)
            image = page_exercises[e].find(class_ = "exercise-card__image lazybg lazybg-inline") 
            image = image['data-lazybg']
            https_link = a = page_exercises[e].find('a', href=True)['href']
            https_link = f"https://www.acefitness.org{https_link}"


            # if title not in array
            json_addition = [title , image , https_link]
            if json_addition not in output[slug]:
                output[slug].append(   json_addition    )
            else:
                # else add to repeat tally (too many repeats means pages reset)
                repeats += 1   
            # close the loop of items
            
            # EXIT STRATEGY
            if repeats > repeat_threashold: end = True
            if end: break
        
        # close the page loop
        if end:
            break
        else:
            # go to page 2
            page += 1
            data = requests.get( base_url + slug + f"/?page={page}" )
            print( "*" * page)







# WRITE TO FILE
with open( "workouts.json" , "w" , encoding="utf-8" ) as f:
    output_json = json.dump( output , f )




