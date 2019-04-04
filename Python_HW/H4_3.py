import numpy as np 
import matplotlib.pyplot as pl

mu = 0
sigma = 1/np.sqrt(2)
x = np.random.normal(mu,sigma, 100000)
y = np.random.normal(mu,sigma, 100000)

z = x + y*(1j)

abs_arr = np.abs(z)

pl.hist(abs_arr,100,edgecolor='black')
pl.xlabel('distribution value')
pl.ylabel('number of occurences')
pl.title('Rayleigh distribution histogram, 100000 samples')
pl.grid(True)
pl.show()   