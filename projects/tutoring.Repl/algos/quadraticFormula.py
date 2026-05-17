import math
a = 5
b = 7
c = 1

posx = ( (-1*b) +  math.sqrt( (b**2) - (4*a*c) )  / (2*a)  )
negx = ( (-1*b) -  math.sqrt( (b**2) - (4*a*c) )  / (2*a)  )
print(posx, negx)