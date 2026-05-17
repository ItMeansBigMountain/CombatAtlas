from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from collections import Counter
import warnings
style.use('fivethirtyeight')

dataset = {
    'k' : [[1,2],[2,3],[3,1]],  #categories are colors
    'r' : [[6,5],[7,7],[8,6]],
}
new_features = [4.5,4] #predicted/challenged data

# for x in dataset: 
#     for y in dataset[x]:
#         plt.scatter(y[0],y[1], s=100 , color = x)
##FORLOOP IS THE SAME AS COMP. LIST BELOW
# [  [plt.scatter(y[0],y[1], s=100 , color = x) for y in dataset[x]]   for x in dataset]
# #DISPLAY
# plt.scatter(new_features[0], new_features[1])
# plt.show()


def k_nearest_neighbors(data , predict, k=3):
    if len(data) >= k:
        warnings.warn('K is set to value less than total voting groups!')

    distances = []
    for group in data:
        for features in data[group]:       #norm is another way of saying euclid distance
            euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
            # euclidean_distance = np.sqrt(np,sum((np.array(features)-np.array(predict))**2))
            distances.append([euclidean_distance,group])

    votes = [i[1] for i in sorted(distances)[:k]]     #last two sub-Indexes because
    vote_result = Counter(votes).most_common(1)[0][0] # most_common() Returns tuple
    return vote_result


result = k_nearest_neighbors(dataset , new_features, k=3)
print(result) #result is the color of the group because we mentioned 'r' and 'k'

[[plt.scatter(ii[0],ii[1], s = 100 , color = i) for ii in dataset[i]]     for i in dataset]
plt.scatter(new_features[0] , new_features[1] , color = result , s = 150)
plt.show()