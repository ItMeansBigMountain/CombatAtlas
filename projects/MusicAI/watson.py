import json
import os
from pathlib import Path
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions, EmotionOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions, SyntaxOptions

import statistics
import datetime
from pprint import pprint

# Environment variables
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DEFAULT_IBM_NLU_CREDENTIALS_FILE = '/opt/data/credentials/ibm-nlu-api-key.json'
DEFAULT_IBM_NLU_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/dd2384c5-cbf9-45c5-9dc8-fb9dd95dea56'


def _credentials_from_file():
  credentials_file = os.getenv('IBM_WATSON_CREDENTIALS_FILE') or os.getenv('WATSON_CREDENTIALS_FILE') or DEFAULT_IBM_NLU_CREDENTIALS_FILE
  path = Path(credentials_file)
  if not path.exists():
    return {}
  with path.open() as handle:
    return json.load(handle)


def _get_credentials():
  file_credentials = _credentials_from_file()
  api_key = (
    os.getenv('WATSON_API_KEY')
    or os.getenv('WATSON_APIKEY')
    or os.getenv('WATSON_NLU_APIKEY')
    or os.getenv('IBM_WATSON_API_KEY')
    or file_credentials.get('apikey')
  )
  url = (
    os.getenv('WATSON_SERVICE_URL')
    or os.getenv('WATSON_INSTANCE_URL')
    or os.getenv('WATSON_NLU_URL')
    or os.getenv('IBM_WATSON_SERVICE_URL')
    or file_credentials.get('url')
    or DEFAULT_IBM_NLU_URL
  )
  return api_key, url

'''
NOTE
in order to use properly ... 
  - log in function
  - gather corpus into array ... each item ==  ai_to_Text(message) 
  - run averages on the array ---> averages_calc( text_Models )
  -after you have the averaged array (input works with just one item as well.)... you will recieve a dictionary with all sentiment frequencies.
  -
'''

# Login to NLU service
def login():
  api_key, url = _get_credentials()
  if not api_key or not url:
    raise RuntimeError('IBM Watson NLU credentials are not configured')

  authenticator = IAMAuthenticator(api_key)
  natural_language_understanding = NaturalLanguageUnderstandingV1(
      version='2022-04-07',
      authenticator=authenticator)
  natural_language_understanding.set_service_url(url)
  return natural_language_understanding
def analyzeText(client, text):
  # Analyze Text
  response = client.analyze(
      text=text,
      features=Features(
          entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
          keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2),
          categories=CategoriesOptions(limit=100),
          concepts=ConceptsOptions(limit=100),
          emotion=EmotionOptions(),
          # emotion=EmotionOptions(targets=['apples','oranges'])
          relations=RelationsOptions(),
          semantic_roles=SemanticRolesOptions(keywords=True , entities=True),
          sentiment=SentimentOptions(),
          # sentiment=SentimentOptions(targets=['stocks']),
          syntax=SyntaxOptions(sentences=True),
          )
    ).get_result()
  return json.dumps(response, indent=2)








# CLEAN DATA
def ai_to_Text(message):
  response = analyzeText(nlu_client, message)
  response = json.loads(response)

  # MAKE A DICTIONARY THAT HOLDS THE AVERAGES OF THE OUTPUT
  # after saving the averages, refer to the message_Dictionary to get a total avg of all messages user sent

  emotion = response.get('emotion', {}).get('document', {}).get('emotion', {}) #dict
  entities = response.get('entities') or [] #list
  keywords = response.get('keywords') or [] #list
  relations = response.get('relations') or [] #list
  # Watson often omits semantic_roles/categories for short song-title strings.
  # Treat those sections as optional so short-title analysis still returns
  # sentiment/emotion instead of falling all the way back to local zeros.
  semantic_roles = response.get('semantic_roles') or [] #list
  sentiment = response.get('sentiment') or {} #dict
  concepts = response.get('concepts') or [] #list
  categories = response.get('categories') or [] #list



  # clean data
  clean_relations = []
  for r in relations:
    # print(r['sentence'])
    for a in r['arguments']:
      for e in a['entities']:
        clean_relations.append(  (e['type'] , e['text'])  )

  # # wowowowowoww
  # lolz = [ (e['type'] , e['text']) for r in relations for a in r['arguments'] for e in a['entities'] ]

  model = {
    'overall_emotion' : emotion,
    'relations' : clean_relations,
    'sentiment' :  sentiment.get('document', {}).get('label', 'neutral')  ,
    'entities' : [  (  i.get('text') , i.get('type')  , (i.get('sentiment') or {}).get('label', 'neutral')  ) for i in entities  ],
    'keywords' : [  (  i.get('text') , (i.get('sentiment') or {}).get('label', 'neutral')   ) for i in keywords  ],
    'subjects' : [  (  (i.get('subject') or {}).get('text') , ((i.get('action') or {}).get('verb') or {}).get('tense', 'unknown') ) for i in semantic_roles  ],
    'concepts' : [  i.get('label')  for i in (categories or concepts) if i.get('label')  ],
  }


  return model





# calculations of arr with ai outputs *** USING ai_to_Text ***
def averages_calc( text_Models ):
  # NOTE: TEXT MODEL ITEM KEYS
  # dict_keys   ['overall_emotion', 'relations', 'subjects', 'entities', 'keywords', 'concepts']

  

  # initialization of all model points through one loop
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
    # sentiment
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


  # OVER ALL EMOTION AVERAGE
  averageEmotion = {
    'Anger' :  sum(overallEmotion['anger']) / len(overallEmotion['anger'])   ,
    'Disgust': statistics.mean(overallEmotion['disgust']),
    'Fear': statistics.mean(overallEmotion['fear']),
    'Joy': statistics.mean(overallEmotion['joy']),
    'Sadness': statistics.mean(overallEmotion['sadness']),
  }






  # RELATIONS 
  relationsfrequencies = {}
  for item in allRelations:
      if item[0] in relationsfrequencies:
          relationsfrequencies[item[0]].append(item[1])
      else:
          relationsfrequencies[item[0]] = [ item[1] ]



  # sentiment
  sentiment_frequencies = {}
  for item in allSentiments:
      if item in sentiment_frequencies:
          sentiment_frequencies[item] += 1
      else:
          sentiment_frequencies[item] = 1
  




  # NOTE checks if entities and keywords have duplicates
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
  entityfrequencies = {}
  for item in allEntities:
      if item[2] in entityfrequencies:
          entityfrequencies[item[2]].append(  ( item[0] , item[1])  )
      else:
          entityfrequencies[item[2]] = [ ( item[0] , item[1])  ] 



  # keywords
  keywordfrequencies = {}
  for item in allKeywords:
      if item[1] in keywordfrequencies:
          keywordfrequencies[item[1]].append(item[0])
      else:
          keywordfrequencies[item[1]] = [item[0]]






  # Concepts
  allConcepts = set(allConcepts) 
  conceptfrequencies = {}
  for x in allConcepts:
    x = x.split("/")[1:]
    if x[0] in conceptfrequencies:
      if len(x[1:]) > 0:
        conceptfrequencies[x[0]].extend( x[1:] )
    else:
      conceptfrequencies[x[0]] = x[1:] 






  # subjects
    #  i['subject']['text'] , i['action']['verb']['tense']
  subjectsfrequencies = {}
  for item in allSubjects:
      if item[1] in subjectsfrequencies:
          subjectsfrequencies[item[1]].append(item[0])
      else:
          subjectsfrequencies[item[1]] = [item[0]]



  # CLEAN AVERAGE DATA MODELS
  # averageEmotion
  # relationsfrequencies
  # sentiment_frequencies
  # entityfrequencies
  # keywordfrequencies
  # conceptfrequencies
  # subjectsfrequencies
  
  sentiment_model = {
    'averageEmotion' : averageEmotion,
    'relationsfrequencies' : relationsfrequencies,
    'sentiment_frequencies' : sentiment_frequencies,
    'entityfrequencies' : entityfrequencies,
    'keywordfrequencies' : keywordfrequencies,
    'conceptfrequencies' : conceptfrequencies,
    'subjectsfrequencies' : subjectsfrequencies
  }


  return sentiment_model


# mood sentiment takes clean data from averages_calc
# averageEmotion
# relationsfrequencies
# sentiment_frequencies
# entityfrequencies
# keywordfrequencies
# conceptfrequencies
# subjectsfrequencies










# runs on import
nlu_client = login()

