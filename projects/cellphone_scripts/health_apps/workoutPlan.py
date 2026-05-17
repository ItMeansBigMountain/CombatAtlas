import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np






# DEBUG
amount_of_training_days = 4
training_sessions = ["Chest" , "Shoulders" , "Back" , "Arms" , 'Cardio']
training_days = ["m" , "tu" ,"w" ,"th" , 'f']
volumes = [6,8,6,4 , 1]
intensites =    [5,4,3,6 , 9]



# # create training sessions
# training_sessions = []
# training_days = []
# volumes = []
# intensites = []
# amount_of_training_days = input("How many training days will you plan? ")
# for i in range(0 , int(amount_of_training_days) , 1):
#     training_sessions.append(
#         input(f"\nPlease enter training session {i+1}: ")
#     )
#     volumes.append(
#         input(f"Volue 1-10: ")
#     )
#     intensites.append(
#         input(f"Intesity 1-10: ")
#     )
#     training_days.append(
#         input("What day will this be on? [ex: TH]\n> ")
#     )





# build plan
week = {
    "Monday" : [],
    "Tuesday" : [],
    "Wednesday" : [],
    "Thursday" : [],
    "Friday" : [],
    "Saturday" : [],
    "Sunday" : [],
}
# sort week for plan
for x in range(0 , len(training_days) , 1):
    if training_days[x].upper().startswith("M"): week["Monday"].append(
        [training_sessions[x] , volumes[x] , intensites[x] ]
    )
    elif training_days[x].upper().startswith("W"): week["Wednesday"].append(
        [training_sessions[x] , volumes[x] , intensites[x]]
    )
    elif training_days[x].upper().startswith("F"): week["Friday"].append(
        [training_sessions[x] , volumes[x] , intensites[x]]
    )
    elif training_days[x].upper().startswith("T"):
        if training_days[x].upper().startswith("TU"):
            week["Tuesday"].append(
        [training_sessions[x] , volumes[x] , intensites[x]]
    )
        else:
            week["Thursday"].append(
        [training_sessions[x] , volumes[x] , intensites[x]]
    )
    elif training_days[x].upper().startswith("S"):
        if training_days[x].upper().startswith("SA"):
            week["Saturday"].append(
        [training_sessions[x] , volumes[x] , intensites[x]]
    )
        else:
            week["Sunday"].append(
        [training_sessions[x] , volumes[x] , intensites[x]]
    )






x_values = []
volume_values = []
intensity_values = []
counter = 0
for day in week:
    if not len(week[day]): week[day] = [["REST" , 1 , 1]]  
    x_values.append(  f"{day}\n"   )
    for plan in week[day]:
        x_values[counter] += f"{plan[0]}\n"
        volume_values.append(  plan[1]   )
        intensity_values.append(  plan[2]   )
        counter += 1








import pprint
pprint.pprint(volume_values)
pprint.pprint(intensity_values)


















# ************ CREATE GRAPH ************


labels = x_values

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars


fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, volume_values, width, label='Volume')
rects2 = ax.bar(x + width/2 , intensity_values, width, label='Intensity')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Volume / Intensity')
ax.set_title('Days')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()