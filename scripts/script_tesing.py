import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# ReLU
Y = np.maximum(np.linspace(-1,1,10),0)
X = np.arange(-5,5)
print(Y)
print(X)

fig, ax = plt.subplots()

ax.plot(X,Y)
plt.show()