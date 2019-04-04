import numpy as np
import matplotlib.pyplot as pl
import itertools

n = []
x = 1
#Enter the numeric values
while(x <=5):
    var = input("Enter exponent n (q to quit)> ")
    if(not(var.isnumeric()) and var != 'q'):
        print("That's not a number!!!")
        continue
    elif(var == 'q'):
        break
    else:
        x = x+1
        n.append(var)        


n = list(map(float,n))
np.array(n)

x = np.linspace(-10,10,num=201,endpoint=True)
my_list = []

for i in n:
    y = 1/(x**i + 1)
    my_list.append(y)     

np.array(my_list)

#Labels and title
title_str = ",".join(str(x) for x in n)
pl.title(r'1/x$^n$ + 1, n =[%s]' %title_str)
pl.xlabel("x")
pl.ylabel("f(x)")

#plot
colors = itertools.cycle(['b', 'r', 'g', 'c', 'm'])
for i in range(len(my_list)):
    color = next(colors)
    pl.plot(x,my_list[i],c=color)

print("Close plot window to continue...")
pl.show()
