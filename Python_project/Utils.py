import numpy as np
import random as random

Freq = 1000 #MHz
Height_Mobile = 1.7 #in mtrs
Height_BS = 50 # in mtrs
EIRP_BS = 55 #dBm





def calc_OH(dist): #distance in mtrs
    dist = dist/1000
    a = 0.8 + (1.1 * np.log10(Freq) - 0.7) * Height_Mobile - (1.56 * np.log10(Freq))
    path_loss = 69.55 + (26.16*np.log10(Freq)) - (13.82*np.log10(Height_BS)) - a + ((44.9 - 6.55*np.log10(Height_BS))*np.log10(dist))
    return path_loss
     

def calc_Shadowing():
    random_val = np.random.normal(0, 2, 1200)
    return random_val

Shadowing_BS_1 = calc_Shadowing()
Shadowing_BS_2 = calc_Shadowing()

mu = 0
sigma = 1
def calc_Fading():
    x = np.random.normal(mu,sigma, 10)
    y = np.random.normal(mu,sigma, 10)
    z = x + y*(1j)
    PL_Fading = np.abs(z)
    PL_Fading_dB = 10*np.log10(PL_Fading) 
    sorted_PL_Fading = np.sort(PL_Fading_dB,axis=None)  
    return sorted_PL_Fading[8]


def calc_RSL(dist):
    RSL = EIRP_BS - calc_OH(dist) + Shadowing_BS_1[int(dist/10)] + calc_Fading()
    return RSL
    


