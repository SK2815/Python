import numpy as np
import matplotlib.pyplot as pl

x = np.linspace(0,2*np.pi,num=10000,endpoint=True)
mu, sigma,num = 0, 0.1,10000
n = np.random.normal(mu, sigma, num)
y = np.cos(x)
z = y + n

#Subplot 1
my_plot_1 = pl.subplot(211)
my_plot_1.set_ylabel('noises',fontsize = 8)
my_plot_1.set_xlabel('radians',fontsize = 8)
my_plot_1.set_title('cosine wave in noise[0:6]',fontsize = 8)
my_plot_1.plot(x,z,'-')
my_plot_1.plot(x,y,'--',c = 'w')

#Subplot 2
my_plot_2 = pl.subplot(223)
my_plot_2.set_ylabel('noises',fontsize = 8)
my_plot_2.set_xlabel('radians',fontsize = 8)
my_plot_2.set_title('cosine wave in noise[1:1.5]',fontsize = 8)
my_plot_2.set_xlim(1,1.5)
my_plot_2.set_ylim(0,1)
my_plot_2.plot(x,z,'-')
my_plot_2.plot(x,y,'--',c = 'w')

#Subplot 3
my_plot_3 = pl.subplot(224)
my_plot_3.set_ylabel('noises',fontsize = 8)
my_plot_3.set_xlabel('radians',fontsize = 8)
my_plot_3.set_title('cosine wave in noise[1:1.05]',fontsize = 8)
my_plot_3.set_xlim(1,1.05)
my_plot_3.set_ylim(0.2,1.2)
my_plot_3.plot(x,z,'-')
my_plot_3.plot(x,y,'--',c = 'r')

pl.show()
