from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import random

style.use('fivethirtyeight')
# RANDOM DATASET
def create_dataset(hm , variance  , step = 2  , correlation = False):
    val = 1
    ys = []
    for i in range(hm):
        y = val + random.randrange(-variance , variance)
        ys.append(y)
        if correlation and correlation == 'pos':
            val+=step
        elif correlation and correlation == 'neg':
            val -= step
    xs = [i for i in range (len(ys))]

    return np.array(xs, dtype = np.float64) , np.array(ys , dtype=np.float64)
#FUNCTION y = mx + b
def best_fit_slope_and_intercept(xs,ys):
    m = ( ((mean(xs) * mean(ys)) - mean(xs*ys)) / ((mean(xs)*mean(xs)) - mean(xs**2))) #best fit line (Y)
    b = mean(ys) - m * mean(xs) #y intercept
    return m, b
#FUNCTION r^2 = 1 - ((SEbestfitline)/SEmeadianLine)
def squared_error(ys_original , ys_line): # r^2 (Squared Error) 
    return sum((ys_line-ys_original)**2)  # 1 - ((SEbestfitline)/SEmeadianLine)
def coefficient_of_determination(ys_original , ys_line): 
    y_mean_line = [mean(ys_original) for y in ys_original] 
    sqared_error_regr = squared_error(ys_original, ys_line)
    sqared_error_mean = squared_error(ys_original, y_mean_line)
    return 1 - (sqared_error_regr / sqared_error_mean)


# ***Calling funcions (main)***

# DATA SET
xs, ys, = create_dataset(40, 100, 2,  correlation='pos') # 40 datapoints, 40 varience, 2 steps on graph
# xs = np.array([1,2,3,4,5,6] , dtype=np.float64)
# ys = np.array([5,4,6,5,6,7],  dtype=np.float64)

# Best Fit Slope and Y intercept  & REGRESSION LINE
m , b = best_fit_slope_and_intercept(xs,ys)
regression_line = [(m*x)+b for x in xs]

# PREDICTION TO CERTAIN X VALUE
predict_x = len(xs)*2
predict_y = (m*predict_x)+b #mx + b

#"how UN - LINEAR" the data set is
r_squared = coefficient_of_determination(ys, regression_line)
print(r_squared) #printing our linear score

plt.scatter(xs,ys)
plt.scatter(predict_x,predict_y,color = 'g', s = 50) #***keep prediction under core data model

plt.plot(xs,regression_line)
plt.show()