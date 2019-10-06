#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 20:53:53 2019

@author: reshirazdan
"""

import numpy as np


Freq = 1000 #MHz
Height_Mobile = 1.7 #in mtrs
Height_BS = 50 # in mtrs
EIRP_BS = 55 #dBm





def calc_OH(dist): #distance in mtrs
    dist = dist/1000
    a = 0.8 + (1.1 * np.log10(Freq) - 0.7) * Height_Mobile - (1.56 * np.log10(Freq))
    path_loss = 69.55 + (26.16*np.log10(Freq)) - (13.82*np.log10(Height_BS)) - a + ((44.9 - 6.55*np.log10(Height_BS))*np.log10(dist))
    return path_loss
     


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


def calc_RSL(dist,Shadowing_list):
    RSL = EIRP_BS - calc_OH(dist) + Shadowing_list[int(dist/10)] + calc_Fading()
    return RSL