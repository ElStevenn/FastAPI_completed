import numpy as np
from sklearn.model_selection import train_test_split

array = np.arange(0,3*10).reshape(10,3)
print(array,"\n***")

train, test = train_test_split(array)
print("Train (80%):\n",train)
print("Test (20%):\n",test)