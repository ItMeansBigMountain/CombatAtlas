import requests
import os
import json
import dateutil

import matplotlib.pyplot as plt

import pprint

from datetime import datetime, timezone, timedelta
from pytz import timezone
import pytz


debug_timeZone = 'Central'

def unix_timeZoneConverter(timezone_str, time):
    utc = timezone('UTC')
    zone = timezone(f'US/{timezone_str}')
    utc_time = time.replace(tzinfo=utc)
    rel_time = utc_time.astimezone(zone)


    return rel_time  


# HELPER functions
def bar_chart(x , y , X_label , Y_label, Title , color_input):
    plt.style.use('ggplot')
    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, y, color= color_input ) #STR ex: "green"
    plt.xlabel(X_label)
    plt.ylabel(Y_label)
    plt.title(Title)
    plt.xticks(x_pos, x)
    # manage picture scale 
    # plt.subplots_adjust(left=None, bottom=0, right=None, top= 0.5, wspace=None, hspace=None)
    plt.xticks(rotation=90)
    plt.show()
def piechart(labels , sizes):
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
def linePlot(xList, yList, title, xLabel, yLabel):
    plt.plot(xList, yList)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()

#plt.plot(xList, yList)
#plt.title('Activity this week')
#plt.xlabel('Day of the week')
#plt.ylabel('Number of messages')
#plt.grid(True) //adds points
#plt.show()





# CORE FUNCTIONALITY
def displayCurrentEmotionPieForUser(data, user):
    labels = (data[user]["overallMessageEmotion_current"].keys())
    sizes = []
    for key in data[user]["overallMessageEmotion_current"].keys():
        sizes.append(data[user]["overallMessageEmotion_current"][key]*100)
    piechart(labels, sizes)



def displayCurrentEmotionPieForServer(data):
    serverEmotions = {
      "anger": [], 
      "disgust": [], 
      "fear": [], 
      "joy": [], 
      "sadness": [], 
    }
    for x in data:
      for emotion in data[x]["overallMessageEmotion_arr"]:
        for emote in emotion.keys():
          if emote in serverEmotions:
            serverEmotions[emote].append(emotion[emote]*100)
    sizes = []
    for i in serverEmotions.keys():
      sum = 0
      for emotions in serverEmotions[i]:
        sum += emotions
      serverEmotions[i] = sum / len(serverEmotions[i])
      sizes.append(serverEmotions[i])
    print(serverEmotions)

      #serverEmotions[emote] = 
        #print(emotion, "\n")
    piechart(serverEmotions.keys(), sizes)


def messageCountBarGraph(data, user):
    if len(data[user]['message_archive']) > 0:
        times = []
        for item in data[user]['message_archive']:
            #times.append(item['timeSent'])
            specialTime = dateutil.parser.parse(item['timeSent'])
            stamp = unix_timeZoneConverter(debug_timeZone, specialTime)
            times.append(stamp)
        pprint.pprint(times)
        #TODO:
            #create two bar graphs - one server wide one per user
            #the "server-wide" graph will have dates on x-axis and message count on y-axis
            #the "per user" graph will have usernames on x-axis and message count on y-axis
    else:
        print('Not enough messages')


data = requests.get("http://18.118.194.70:8080/?server=837445544326463518").json()
#displayCurrentEmotionPieForUser(data, "219376861866754049")
#linePlot([1,2], [2,3], "testing plot", "x", "y")
messageCountBarGraph(data, '289894338132180992')
#displayCurrentEmotionPieForServer(data)
# main
# bar_chart([0,1,2,3] , [9,8,7,6] , "x" , "y" , "random", "blue")
#piechart( labels, sizes)#[data["219376861866754049"]["overallMessageEmotion_current"]["anger"]*100, data["219376861866754049"]["overallMessageEmotion_current"]["disgust"]*100])