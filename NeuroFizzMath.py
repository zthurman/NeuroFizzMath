#!/usr/bin/env python
#  Classes for different differential eqn models. All the math
# resides here

from __future__ import division
from scipy import *
import numpy as np
import pylab
import matplotlib as mp
from matplotlib import pyplot as plt  
import sys
import math as mt

# global Runge-Kutte solver

def rk4(t0 = 0, x0 = np.array([1]), t1 = 5 , dt = 0.01, ng = None):
    tsp = np.arange(t0, t1, dt)
    Nsize = np.size(tsp)
    X = np.empty((Nsize, np.size(x0)))
    X[0] = x0
    for i in range(1, Nsize):
        k1 = ng(X[i-1],tsp[i-1])
        k2 = ng(X[i-1] + dt/2*k1, tsp[i-1] + dt/2)
        k3 = ng(X[i-1] + dt/2*k2, tsp[i-1] + dt/2)
        k4 = ng(X[i-1] + dt*k3, tsp[i-1] + dt)
        X[i] = X[i-1] + dt/6*(k1 + 2*k2 + 2*k3 + k4)
    return X

# FN neuron model

class FN():
    name = "Fitzhugh-Nagumo"
    x0 = np.array([0.01,0.01])

    def __init__(self, name):
        self.name = name

    def model(self,x,t, a = 0.75, b = 0.8, c = 3,  i = -0.39):
        return np.array([c*(x[0]+ x[1]- x[0]**3/3 + i),
                         -1/c*(x[0]- a + b*x[1])])

# ML neuron model

class ML():
    name = 'Morris-Lecar'
    x0 = np.array([0,0])
    def __init__(self, name):
       self.name = name

    def model(self,x,t,c = 20,vk=-84,gk = 8,vca = 130,gca = 4.4,vl = -60,gl = 2,phi = 0.04,v1 = -1.2,v2 = 18,v3 = 2,v4 = 30,i = 79):
        return np.array([(-gca*(0.5*(1 + mt.tanh((x[0] - v1)/v2)))*(x[0]-vca) - gk*x[1]*(x[0]-vk) - gl*(x[0]-vl) + i),
                        (phi*((0.5*(1 + mt.tanh((x[0] - v3)/v4))) - x[1]))/(1/mt.cosh((x[0] - v3)/(2*v4)))])

# IZ neuron model

class IZ():
    name = 'Izhikevich'
    x0 = np.array([0,0])
    def __init__(self, name):
       self.name = name

    def model(self,x,t, a = 0.02, b = 0.2, c = -65, d = 2, i = 10):
        if x[0] >= 30:
            x[0] = c
            x[1] = x[1] + d
        return np.array([0.04*(x[0]**2) + 5*x[0] + 140 - x[1] + i,
                        a*(b*x[0] - x[1])])

# HR neuron model

class HR():
    name = 'Hindmarsh-Rose'
    x0 = np.array([3, 0, -1.2])
    def __init__(self, name):
       self.name = name

    def model(self,x,t, a = 1.0, b = 3.0, c = 1.0, d = 5.0, r = 0.006, s = 4.0, I = 1.84, xnot = -1.5, k = 0.05):
        return np.array([x[1] - a*(x[0]**3) + (b*(x[0]**2)) - x[2] + I + k*(x[3] - x[0]),
                        c - d*(x[0]**2) - x[1],
                        r*(s*(x[0] - xnot) - x[2]),
                        x[4] - a*(x[3]**3) + (b*(x[3]**2)) - x[5] + I + k*(x[0] - x[3]),
                        c - d*(x[3]**2) - x[4],
                        r*(s*(x[3] - xnot) - x[5])])

# HH neuron model

class HH():
    name = 'Hodgkins-Huxley'
    x0 = np.array([0.01,0.01,0.01,0.01])
    def __init__(self, name):
       self.name = name

    def model(self,x,t, g_K=36, g_Na=120, g_L=0.3, E_K=12, E_Na=-115, E_L=-10.613, C_m=1, I=-10):
        alpha_n = (0.01*(x[0]+10))/(exp((x[0]+10)/10)-1)
        beta_n = 0.125*exp(x[0]/80)
        alpha_m = (0.1*(x[0]+25))/(exp((x[0]+25)/10)-1)
        beta_m = 4*exp(x[0]/18)
        alpha_h = (0.07*exp(x[0]/20))
        beta_h = 1 / (exp((x[0]+30)/10)+1)
        return np.array([(g_K*(x[1]**4)*(x[0]-E_K) + g_Na*(x[2]**3)*x[3]*(x[0]-E_Na) + g_L*(x[0]-E_L) - I)*(-1/C_m),
                        alpha_n*(1-x[1]) - beta_n*x[1],
                        alpha_m*(1-x[2]) - beta_m*x[2],
                        alpha_h*(1-x[3]) - beta_h*x[3]])

# RD model for geomagnetic reversal

class RD():
    name = 'Rikitake Dynamo'
    x0 = np.array([-1.4, -1, -1, -1.4, 2.2, -1.5])
    def __init__(self, name):
       self.name = name

    def model(self, x,t, m = 0.5, g = 50, r = 8, f = 0.5):
        return np.array([r*(x[3] - x[0]),
                         r*(x[2] - x[1]),
                         x[0]*x[4] + m*x[1] - (1 + m)*x[2],
                         x[1]*x[5] + m*x[0] - (1 + m)*x[3],
                         g*(1 - (1 + m)*x[0]*x[2] + m*x[0]*x[1]) - f*x[4],
                         g*(1 - (1 + m)*x[1]*x[3] + m*x[1]*x[0]) - f*x[5]])

    # will need this later for making plots of this:
    # X = rk4(x0 = np.array([-1.4, -1, -1, -1.4, 2.2, -1.5]), t1 = 100, dt = 0.0001, ng = model)

# W neuron model

class W():
    name = 'Wilson Model'
    def __init__(self, name):
       self.name = name

    def model(self, x, t):
        pass

# L atmospheric model

class L():
    name = 'Lorenz Equations'
    x0 = np.array([1.0, 2.0, 1.0])
    def __init__(self, name):
        self.name = name

    def model(self, x, t, sigma = 10.0, rho = 28.0, beta = 10.0/3):
        return np.array([sigma * (x[1] - x[0]),
                         rho*x[0] - x[1] - x[0]*x[2],
                         x[0]*x[1] - beta*x[2]])


class R():
    name = 'Robbins Equations'

    def __init__(self, name):
        self.name = name

    def model(x,t, V = 1, sigma = 5, R = 13):
        return np.array([R - x[1]*x[2] - V*x[0],
                         x[0]*x[2] - x[1],
                         sigma*(x[1] - x[2])])
