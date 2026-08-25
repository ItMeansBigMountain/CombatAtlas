from time import sleep
import tweepy

'''
RUN THIS ON AWS EC2 INSTANCE AND THEN HAVE IT EMAIL YOU THE JSON OUTPUT OR HOST ON REST/FLASK

'''



# AUTH
consumer_key = "wt6Nq4RTTHUXsyEaWcl8b9p2m" 
consumer_secret = "goZiuvzsv3KsDpAZun0nn6Xo0nvFszq9P5pxTXQrgMgfLKC7LQ"
access_key = "444144269-s9agQgdQujtygHUPn1x5KfkLzn6YquTIeQgoGhXf"
access_secret = "CeC6W0j5Md5dYgZ3wx88PqEgQWZd7HtlcyOrSxpaG5mZq"

# OAUTH
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key,access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True  )



def each_country_trends(api):
    availabe_countries = api.available_trends()
    print(f"{len(availabe_countries)}  countries\n" , "each_country_trends() fails due to api limit")
    exit()

    output = {}
    for i in range(0,len(availabe_countries),1):
        NAME = availabe_countries[i]['name']
        WOEID = availabe_countries[i]['woeid']
        
        output[NAME] = []
        country_data = api.get_place_trends( WOEID )
        for t in range(0 , len(country_data) , 1):
            print(NAME ,  country_data[t]['as_of'])
            
            for trend_item in country_data[t]['trends']:
                output[NAME].append(trend_item['name'])
                print(trend_item['name'])
        # print("----------")

    return output




def fetch_global(api):
    global_trends = api.get_place_trends(1)
    all_trends = {}
    for x in global_trends:
    # 'trends', 'as_of', 'created_at', 
        for i in x['trends']:
            # 'name', 'url', 'promoted_content', 'query', 'tweet_volume'
            print( i['name'] ,  i['tweet_volume']  )
            all_trends[i['name']] = i['tweet_volume']

    return all_trends



# TOP TRENDS OF A COUNTRY
def fetch_country(api):
    availabe_countries = api.available_trends()
    for x in range(0,len(availabe_countries),1):
        NAME = availabe_countries[x]['name']
        WOEID = availabe_countries[x]['woeid']
        print( f"{NAME} : {WOEID}"  )
    user_input = input("\nPlease enter id number for country\n>")
    
    try:
        selected_trends = api.get_place_trends(int(user_input))
        all_trends = {}
        for x in selected_trends:
            for i in x['trends']:
                all_trends[i['name']] =  i['tweet_volume']
        return all_trends
    except Exception as e:
        print("invalid parameters")





# calling functions down here
o =  each_country_trends(api)
# o =  fetch_global(api)
# o =  fetch_country(api)
print( o )