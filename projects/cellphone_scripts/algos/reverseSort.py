def sortThisnumber(num):
    num = str(num)
    box = ''

    while len(num) > 0:
        for x in range (len(num)):
            tally = 0
            maximum = num[x]
            for y in range(len(num)):
                if int(num[y]) > int(maximum):
                    maximum = num[y]
                if int(num[y]) == int(maximum):
                    tally += 1
        
        box += maximum * tally
        num = num.replace(maximum , '')

    return int(box)


print(sortThisnumber(456456456456456))