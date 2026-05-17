user_board = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
]

for x in user_board:
    print(x)


def add_data(array):

    for x in range(9):
        user_row = input('\nPlease enter a row: ')
        user_col = input('Please enter a coloumn: ')
        user_input = input('Please input a number: ')
        array[int(user_row)-1][int(user_col)-1] = int(user_input)
            
        for x in user_board:
            print(x)


    return user_board


def results(array):
    comparison_list = []

    horizon_sum_1 = sum(array[0]) #horizontal
    horizon_sum_2 = sum(array[1])
    horizon_sum_3 = sum(array[2])
    comparison_list.append(horizon_sum_1)
    comparison_list.append(horizon_sum_2)
    comparison_list.append(horizon_sum_3)


    vert1 = []
    for x in range(len(array)):
        vert1.append(array[x][0])
    vert2 = []
    for x in range(len(array)):
        vert2.append(array[x][1])
    vert3 = []
    for x in range(len(array)):
        vert3.append(array[x][2])

    comparison_list.append(sum(vert1))
    comparison_list.append(sum(vert2))
    comparison_list.append(sum(vert3))


    diagnol_right = []
    for x in range(len(array)):
        diagnol_right.append(array[x][x])
    comparison_list.append(sum(diagnol_right))

    diagnol_left = []
    for x in range(len(array)):
        distance = len(array[x]) - x
        diagnol_left.append(array[x][distance-1])
    comparison_list.append(sum(diagnol_left))

    return comparison_list


def success(result_list):
    for x in range(len(result_list)):
        if result_list[0] != result_list[x]:
            return False



data = add_data(user_board)
comp_list = results(data)
success_or_fail = success(comp_list)
if success_or_fail == None:
    print('\nGOOD JOB')
else:
    print('\nFAILURE')

