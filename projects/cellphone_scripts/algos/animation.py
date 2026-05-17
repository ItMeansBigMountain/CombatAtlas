arr = [ '☁'  ,' ' , ' ' ,' ' , ' ' ,' ' , ' ' ,' ' , ' ']
position = 0

forward = True
while True:
    print(arr)
    if forward:
        temp = arr[position + 1  ]
        arr[position + 1] = arr[position]
        arr[position] = temp
        position += 1
    else:
        temp = arr[position - 1  ]
        arr[position - 1] = arr[position]
        arr[position] = temp
        position -= 1
    if position == 0:
        forward = True
    elif position == len(arr) - 1:
        forward = False
