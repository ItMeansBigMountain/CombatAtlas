import matplotlib.pyplot as plt
import datetime

def write_data():
	f = open("moodData.md","a")
	scale = int(input('From a scale of 1 - 10 , How do you feel today?'))
	f.write(str(datetime.datetime.now()))
	f.write('\n')
	f.write(str(scale))
	f.write('\n')
	f.close()
	print('done')

def display_data():
	f = open("moodData.md","r")
	read = f.readlines()
	ratings =[]
	compare = [1,2,3,4,5,6,7,8,9,10]
	displayArray = [0,0,0,0,0,0,0,0,0,0]
	
	for x in range(1,len(read),2):
		dailyRating = int(read[x])
		ratings.append(dailyRating)
	
	for x in ratings:
		for y in range(len(compare)):
			if x == compare[y]:
				displayArray[y] += 1
	print(displayArray)
	
	f.close()
	
	biggest_rating = max(displayArray)
	chart(displayArray,biggest_rating)

def choice():
	print('\n1. Enter mood for\n '+ str(datetime.datetime.now()))
	print('2. Pie chart')
	print('3. Bar chart')
	print('4. Read input history\n')
	
	choice = int(input('Please choose and option: '))
		
	if choice == 1:
		write_data()
	if choice ==2:
		display_data()
	if choice == 3:
		barChart()
	if choice == 4:
		read()

def chart(rating, biggest):
	# The slices will be ordered and plotted counter-clockwise.
	labels = '1', '2', '3', '4', '5', '6', '7', '8', '9','10'
	sizes = rating
	colors = ['maroon', 'red', 'firebrick', 'lightcoral', 'honeydew', 'greenyellow', 'lawngreen','lime', 'limegreen','#059b30']
	
	
	for x in rating:
		if int(x) == int(biggest):
			subindex = rating.index(biggest)
	
	newlist = [0,0,0,0,0,0,0,0,0,0]
	newlist[subindex] = .1
	explode = tuple(newlist)
	#explode = (0,0,0,0,0,0,0,0,0,0)

	
	plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90)
	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')
	plt.show()

def main():
	endprogram = False
	while endprogram == False:
		choice()
		
		endIt = input('Do you want to end the program (TYPE : "yes")')
		if endIt == 'yes':
			endprogram = True

def read():
	f = open("moodData.md","r")
	print('\n_______INPUT HISTORY_______\n')
	print(f.read())


def barChart():
	f = open("moodData.md","r")

	read = f.readlines()
	for x in range(0 , len(read) , 1):
		read[x] = read[x].replace("\n", "")



	dates = []
	ratings =[]

	for x in range(0 , len(read) , 2):
		print(read[x])

	for x in range(1 , len(read) , 2):
		print(read[x])


	print(dates)
	print(ratings)







	

	print(read)
	f.close()




main()
