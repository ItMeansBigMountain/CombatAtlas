import tmdbsimple as tmdb #<--- IMPORTS ROTTEN TOMATO API
import pprint # PRETTY PRINT makes our data look readable

#LOG INTO THE API
tmdb.API_KEY = os.getenv('TMDB_API_KEY', '')

#USE API FEATURE CALLED SEARCH
search = tmdb.Search()

#access database to search for movies
user_search_input = input("Please enter title of movie: ")
response = search.movie( query = user_search_input )
#pprint.pprint(response)

#create array with all search results
search_results_array = response["results"]

#loop through the array and clean the data
for search in search_results_array:
  #printing parameters for each item in list (search results)
   print(search['title'])
   print("ID: ",search['id'])
   print("Release Date: ",search['release_date'])
   print("Popularity: ",search['popularity'])
   print()


#PARAMETERS
  # "title"
  # "id"
  # "release_date"
  # "popularity"
  # "vote_count"
  # "overview"



#DOCUMENTATION
# https://pypi.org/project/tmdbsimple/#:~:text=tmdbsimple%20is%20a%20wrapper%2C%20written,out%20the%20overview%20and%20documentation

