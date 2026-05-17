import watson
import discord
import json
from discord.ext import commands

from pprint import pprint
import datetime

now = datetime.datetime.now()

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import statistics

# CHECK LINE 270S FOR TONE DATA STORAGE
# CHECK IF TONE DATA SAVED IN USERJSON THE WAY WE WANTED TO .... SAVE ALL NAMES AND MAKE DICT OF THE NAME : FREQUENCY
'''
we create user model in:
  def on_ready
  def on_member_join


SET API KEYS AS VARIABLES AT THE TOP SO WE CAN SET ENV VARIABLES LATER


DATA MODEL

/////////////  analyze text  ///////////////// (138)
resonse = {
   "usage":{},
   "language":"en",


  SENTIMENT ITEM KEYS
  document['label]
   "sentiment":{},


  SEMANTIC ROLES ITEM KEYS
  subject
  object
  action
   "semantic_roles":[],



  RELATIONS ITEM KEYS
  type
  sentence
  arguments
  arguments[text]
   "relations": [],


  KEYWORDS ITEM KEYS
  type
  text
  sentiment['label']
  sentiment['emotion']
  relevance
  count
   "keywords":{},



  ENTITIES ITEM KEYS
  type
  text
  sentiment['label']
  sentiment['emotion']
  relevance
   "entities":[],



  EMOTIONS
   "emotion":{
    "document": {
      "emotion": {
        "sadness": 0.035355,
        "joy": 0.889904,
        "fear": 0.016269,
        "disgust": 0.023896,
        "anger": 0.031936
      },



  text
   "concepts":[],



  label
   "categories":[],



  document_tone['tones']
  sentences_tone['sentence_id']
  sentences_tone['text']
  sentences_tone['tones']
  sentences_tone['tones']['tone_name']
    "syntax" : {}



  warnings.keys()
   "warnings":[]
}


/////////////  TONE  /////////////////

tone = {
  'document_tone': {},
  'tones': [
    {
      'score': 0.657267,
      'tone_id': 'anger',
      'tone_name': 'Anger'
    }
  ],
}






userJSON
  model = {
  'overallMessageEmotion_arr': [],
  'overallMessageEmotion_current': {},
  'commonConcepts_arr' : [],
  'commonConcepts_current' : {},
  'topicalData_arr' : [],
  'topicalData_current' : {},
  'tones_avg' : [],
  'tones_avg' : "",
  'message_log' : [],
  'message_count': 0,
  'message_archive': []
  }




TODO
- for every message received, analyze then update the data model

'''


# Discord Settings
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

# IBM LOGIN
ai_Login = watson.login()
tone_login = watson.toneLogin()


# TODO : save this data using json
server_settings = {}







# Helper functions
def create_userModel(member, server_id):
  print(f'{member} model has been created')
  # create model
  model = {
    'username': f'{member.name}#{member.discriminator}',
    'userId': member.id,
    'date_created' : str(datetime.datetime.now()),
    'overallMessageEmotion_arr': [], 
    'overallMessageEmotion_current': {}, 
    'relations' : {},
    'sentiment' : {},
    'entities' : {},
    'keywords' : {},
    'concepts' : {},
    'subjects' : {},
    'tones_avg' : {} ,
    'message_log' : [],
    'message_count' : 0,
    'message_archive' : []
  }
  # save to json
  with open(f'{server_id}_users.json') as json_file:
      json_decoded = json.load(json_file)
  json_decoded[str(member.id)] = model

  with open(f'{server_id}_users.json', 'w') as json_file:
      json.dump(json_decoded, json_file)

  return model





# IBM functions
def ai_to_Text(message):
  response = watson.analyzeText(ai_Login, message)
  response = json.loads(response)

  emotion = response['emotion']['document']['emotion'] #dict
  entities = response['entities'] #list
  keywords = response['keywords'] #list
  relations = response['relations'] #list
  semantic_roles = response['semantic_roles'] #list
  sentiment = response['sentiment'] #dict
  concepts = response['concepts'] #list
  categories = response['categories'] #list
  # syntax = response['syntax'] #dict
  # warnings = response['warnings']

  #////////////////////////////////////////////////////////////////////
  clean_relations = []
  # Cleans the relation data for only the type and text of the relation
  for r in relations:
    for a in r['arguments']:
      for e in a['entities']:
        clean_relations.append(  (  e['type'] , e['text'])  )

  # wowowowowoww
  lolz = [ (e['type'] , e['text']) for r in relations for a in r['arguments'] for e in a['entities']]


  # each message inside ["message_logs"]['anylizeText']
  model = {
    'overall_emotion' : emotion,
    'relations' : clean_relations,
    'sentiment' :  sentiment['document']['label']  ,
    'entities' : [  (  i['text'] , i['type']  , i['sentiment']['label']  ) for i in entities  ],
    'keywords' : [  (  i['text'] , i['sentiment']['label']   ) for i in keywords  ],
    'subjects' : [  (  i['subject']['text'] , i['action']['verb']['tense'] ) for i in semantic_roles  ],
    'concepts' : [  i['label']  for i in categories  ],
  }
  #////////////////////////////////////////////////////////////////////

  return model
def ai_tone(message):
  response = watson.tone_CLIENT(tone_login , message)
  response = json.loads(response)
  return response  





# CALCULATIONS
def averages_calc(userJSON, settingsJSON):
  print("calculating...")


  # dict_keys   ['overall_emotion', 'relations', 'subjects', 'entities', 'keywords', 'concepts']
  text_Models = [ i['textAnalysis'] for i in userJSON['message_log']  ] 
  
  #add "if ai/tone data" 
  # keys : document_tone , sentene_tone
  
  # userJSON['tones_avg']
  # userJSON['tones_avg']
  tone_models = [ i['tone']['document_tone']['tones'] for i in userJSON['message_log']  ] 


  # TODO : every item in tone models needs to be put into an even bigger array that holds all the tone names for this calculation... then we can find their frequencies and save the frequencies to the userJSON
  

  # userJSON['tones_avg']
  tone_frequencies = {}
  for item in tone_models:
      for toneData in item:
        if toneData['tone_name'] not in tone_frequencies:
          tone_frequencies[toneData['tone_name']] = 0
        tone_frequencies[toneData['tone_name']]+=1
  
  # dump tones in userJSON
  for x in tone_frequencies.keys():
    if x in userJSON['tones_avg']:
      userJSON['tones_avg'][x] += tone_frequencies[x]
    else:
      userJSON['tones_avg'][x] = tone_frequencies[x]

  print(userJSON['tones_avg'])




  overallEmotion = {
    'anger': [],
    'disgust': [],
    'fear': [],
    'joy': [],
    'sadness': []
  }
  allRelations = []
  allSentiments = []
  allEntities = []
  allKeywords = []
  allConcepts = []
  allSubjects = []


  for i in text_Models:
    # OVERALL EMOTION
    overallEmotion['anger'].append(i['overall_emotion']['anger'])
    overallEmotion['disgust'].append(i['overall_emotion']['disgust'])
    overallEmotion['fear'].append(i['overall_emotion']['fear'])
    overallEmotion['joy'].append(i['overall_emotion']['joy'])
    overallEmotion['sadness'].append(i['overall_emotion']['sadness'])
    # relations
    for r in i['relations']:
      allRelations.append(r)
    # # sentiment
    allSentiments.append(i['sentiment'])
    # entities
    for e in i['entities']:
      allEntities.append(e)
    # keywords
    for k in i['keywords']:
      allKeywords.append(k)
    # keywords
    for l in i['concepts']:
      allConcepts.append(l)
    # subject
    for s in i['subjects']:
      allSubjects.append(s)





  # OVERALL EMOTION AVERAGES
  overallEmotion['anger'] = statistics.mean(overallEmotion['anger'])
  overallEmotion['disgust'] = statistics.mean(overallEmotion['disgust'])
  overallEmotion['fear'] = statistics.mean(overallEmotion['fear'])
  overallEmotion['joy'] = statistics.mean(overallEmotion['joy'])
  overallEmotion['sadness'] = statistics.mean(overallEmotion['sadness'])





  # RELATIONS 
  relationsfrequencies = {}
  for item in allRelations:
      if item[0] in relationsfrequencies:
          relationsfrequencies[item[0]].append(item[1])
      else:
          relationsfrequencies[item[0]] = [ item[1] ]

  # dump relations in userJSON

  for x in relationsfrequencies.keys():
    if x in userJSON['relations']:
      userJSON['relations'][x].extend(relationsfrequencies[x])
    else:
      userJSON['relations'][x] = relationsfrequencies[x]

  # print('\n\n-------- relations ---------')
  # pprint(userJSON['relations'])



  # sentiment
  sentiment_frequencies = {}
  for item in allSentiments:
      if item in sentiment_frequencies:
          sentiment_frequencies[item] += 1
      else:
          sentiment_frequencies[item] = 1
  
  # dump sentiment in userJSON
  for x in sentiment_frequencies.keys():
    if x in userJSON['sentiment']:
      userJSON['sentiment'][x] += sentiment_frequencies[x]
    else:
      userJSON['sentiment'][x] = sentiment_frequencies[x]

  # print('\n\n-------- sentiment ---------')
  # pprint( userJSON['sentiment'])





  # NOTE check if entities and keywords have duplicates
  removes = []
  if len(allEntities) > 0 and len(allKeywords) > 0:
    keywords_Length = len(allKeywords)
    for x in range(len(allEntities)):
      for y in range(keywords_Length):
        if allEntities[x][0] == allKeywords[y][0]:
          removes.append(allKeywords[y])
          
    # remove the item and handle key error if duplicates of multiples
    if len(removes) > 0:
      for y in removes:
        try:
          allKeywords.remove(y)
        except ValueError:
          pass
        except:
          print('\n\n################## ERROR in calculations ##################\n\n')



  # entities
  # ( word , type of thing it is...  )
  entityfrequencies = {}
  for item in allEntities:
      if item[2] in entityfrequencies:
          entityfrequencies[item[2]].append(  ( item[0] , item[1])  )
      else:
          entityfrequencies[item[2]] = [ ( item[0] , item[1])  ] 

  # dump entities in userJSON
  for x in entityfrequencies.keys():
    if x in userJSON['entities']:
      userJSON['entities'][x].extend(entityfrequencies[x])
    else:
      userJSON['entities'][x] = entityfrequencies[x]

  # print('\n\n-------- entities ---------')
  # pprint(userJSON['entities'])
  
  



  # keywords
  #  i['text'] , i['sentiment']['label'] , i['emotion'] 
  keywordfrequencies = {}
  for item in allKeywords:
      if item[1] in keywordfrequencies:
          keywordfrequencies[item[1]].append(item[0])
      else:
          keywordfrequencies[item[1]] = [item[0]]

  # dump keywords in userJSON
  for x in keywordfrequencies.keys():
    if x in userJSON['keywords']:
      userJSON['keywords'][x].extend(keywordfrequencies[x])
    else:
      userJSON['keywords'][x] = keywordfrequencies[x]
      
  # print('\n\n-------- keywords ---------')
  # pprint(userJSON['keywords'])



  # Concepts
  # allConcepts = set(allConcepts)    #//no duplicates

  conceptfrequencies = {}
  for x in allConcepts:
    x = x.split("/")[1:]
    if x[0] in conceptfrequencies:
      if len(x[1:]) > 0:
        conceptfrequencies[x[0]].append( x[1:] )
    else:
      conceptfrequencies[x[0]] = [ x[1:]  ] 

  # dump concepts in userJSON
  for x in conceptfrequencies.keys():
    if x in userJSON['concepts']:
      userJSON['concepts'][x].extend(conceptfrequencies[x])
    else:
      userJSON['concepts'][x] = conceptfrequencies[x]

  # print('\n\n-------- concepts ---------')
  # pprint(userJSON['concepts'])





  # subjects
    #  i['subject']['text'] , i['action']['verb']['tense']
  subjectsfrequencies = {}
  for item in allSubjects:
      if item[1] in subjectsfrequencies:
          subjectsfrequencies[item[1]].append(item[0])
      else:
          subjectsfrequencies[item[1]] = [item[0]]

  # dump sentiment in userJSON
  for x in subjectsfrequencies.keys():
    if x in userJSON['subjects']:
      userJSON['subjects'][x].extend(subjectsfrequencies[x])
    else:
      userJSON['subjects'][x] = subjectsfrequencies[x]

  # print('\n\n-------- subjects ---------')
  # pprint(userJSON['subjects'])


  # CLEAN AVERAGE DATA MODELS
  # averageEmotion
  # relationsfrequencies
  # sentiment_frequencies
  # entityfrequencies
  # keywordfrequencies
  # conceptfrequencies
  # subjectsfrequencies




  # Add timestamp
  overallEmotion['timeCalculated'] = str(datetime.datetime.now())

  userJSON['overallMessageEmotion_arr'].append(overallEmotion)






  # getting the averages of averages EMOTION
  if len(userJSON['overallMessageEmotion_arr']) > 1:
    cur_anger = []
    cur_disgust  = []
    cur_fear  = []
    cur_joy  = []
    cur_sadness  = []
    for x in userJSON['overallMessageEmotion_arr']:
      cur_anger.append(x['anger'])
      cur_disgust.append(x['disgust'])
      cur_fear.append(x['fear'])
      cur_joy.append(x['joy'])
      cur_sadness.append(x['sadness'])

    overallMessageEmotion_current = {
      'anger' : statistics.mean(cur_anger),
      'disgust' : statistics.mean(cur_disgust),
      'fear' : statistics.mean(cur_fear),
      'joy' : statistics.mean(cur_joy),
      'sadness' : statistics.mean(cur_sadness)
    }



    # saves current
    userJSON['overallMessageEmotion_current'] = overallMessageEmotion_current


  # if we save it ... then it exponentially increases 

  # userJSON['message_archive'] == []




  # # clean / clear message_lo
  
  userJSON['message_log'] = []
    

  # return New userJSON with update averages...
  return userJSON







# SERVER COMMANDS
@client.command()
async def settings(ctx):
  server_id = ctx.guild.id
  with open(f'{server_id}_settings.json', 'r') as f:
    settingsJSON = json.load(f)
  embed = discord.Embed(title="Settings", description="Here are your settings")
  embed.add_field(name="Save Messages?", value=settingsJSON['saveMessages'])
  await ctx.send(embed=embed)


@client.command()
async def until_calc(ctx , arg):
  server_id = ctx.guild.id
  with open(f'{server_id}_settings.json', 'r') as f:
    settingsJSON = json.load(f)
  # ...
  with open(f'{server_id}_settings.json', 'w') as f:
    pass

  await ctx.send()





# core functions
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
      print('\n \t' , guild)

      # checks for user database
      if os.path.exists('{}_users.json'.format(guild.id)):
        pass
      else:
        with open('{}_users.json'.format(guild.id), 'a') as f:
          f.write("{}")

      # check for server settings
      if os.path.exists('{}_settings.json'.format(guild.id)):
        pass
      else:
        with open('{}_settings.json'.format(guild.id), 'a') as f:
          f.write('{"saveMessages": false}')

      for member in guild.members:
        if member.bot: 
          continue
        with open('{}_users.json'.format(guild.id)) as json_file:
          json_decoded = json.load(json_file)
          if str(member.id) in json_decoded:
            print(f"{member} ----> previous user ")
            pass
          else:
            print(f'{member} model has been created')
            model = {
              'username': f'{member.name}#{member.discriminator}',
              'userId': member.id,
              'date_created' : str(datetime.datetime.now()),
              'overallMessageEmotion_arr': [], 
              'overallMessageEmotion_current': {},
              'relations' : {},
              'sentiment' : {},
              'entities' : {},
              'keywords' : {},
              'concepts' : {},
              'subjects' : {},
              'tones_avg' : {} ,
              'message_log' : [],
              'message_count' : 0,
              'message_archive' : []
            }
            json_decoded[str(member.id)] = model
            with open('{}_users.json'.format(guild.id), 'w') as json_file:
                json.dump(json_decoded, json_file)

@client.event
async def on_message(message):
  #if message was from bot(s), do nothing
  if message.is_system():
    return
  if message.author == client.user:
    return 
  if message.author.bot: 
    return
  if not message.guild:
    return

  await client.process_commands(message)

  server_id = message.guild.id
  # check if json db exists
  # if it doesnt then make one and add user as the model...
  if not os.path.exists(f'{server_id}_users.json'):
    with open(f'{server_id}_users.json', 'a') as f:
      f.write("{}")

    

  # anylize message
  # TODO: make checks for messages and ai bot errors
    # links
    # files
    # ...
  if len(message.content.split()) >= 3:

    try:
      ai_tone_analysis = ai_tone(message.content)


      ai_text_analysis = ai_to_Text(message.content)
    except Exception as e:
      print("ERROR:" , e)
      return

    #adding data into json Database <user.json>
    with open(f'{server_id}_users.json', 'r') as f:
      userDatabaseLoaded = json.load(f)
      userJSON = userDatabaseLoaded[str(message.author.id)]

    with open(f'{server_id}_settings.json', 'r') as f:
      settingsJSON = json.load(f)


    userJSON['message_count'] += 1

    # use userDatabaseLoaded as update model then dump it at the end of our calculations, per message

    # calculations are saved here....
    userJSON['message_log'].append({
      'content': message.content,
      'id': message.id,
      'tone': ai_tone_analysis,       
      'textAnalysis': ai_text_analysis,
      "timeSent": str(datetime.datetime.now())
    })



    # handling message archive
    if not settingsJSON['saveMessages']:
        # userJSON['message_archive'] = []
        pass
    else:
      userJSON['message_archive'].append({
        'content': message.content,
        'timeSent' :  str(datetime.datetime.now())
      })


    # what happens to message logs?

    if userJSON['message_count'] >= 5:
      userJSON['message_count'] = 0
      userJSON = averages_calc(userJSON, settingsJSON)
      

    userDatabaseLoaded[str(message.author.id)] = userJSON
    #update json
    with open(f'{server_id}_users.json', 'w') as f:
      json.dump(userDatabaseLoaded, f) 



  #specific channel commands
  if (message.channel.id == 'channel id'):
    pass

  if message.content.startswith('.help'):
    await message.channel.send("HELP ME " )









# event functions

@client.event
async def on_guild_join(guild):
  server_id = guild.id
  if os.path.exists(f'{server_id}_users.json'):
    pass
  else:
    with open(f'{server_id}_users.json', 'a') as f:
      f.write("{}")

@client.event
async def on_member_join(member):
  print(member)
  server_id = member.guild.id

  if os.path.exists(f'{server_id}_users.json'):
    pass
  else:
    with open(f'{server_id}_users.json', 'a') as f:
      f.write("{}")

  create_userModel(member, server_id)

  await member.send("Welcome!")















#logs into discord
client.run(os.environ["WATSON_DISCORD_BOT_TOKEN"])



