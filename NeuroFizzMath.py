#!/usr/bin/env python
# NeuroFizzMath - NeuroFizzMath
# Copyright (C) 2016 Zechariah Thurman
# GNU GPLv2

from __future__ import division
import numpy as np
import math as mt


# class Neuron:
#     def __init__(self):


def modelSelector(modelname):
    if modelname is None:
        raise TypeError
    if modelname == 'VDP':
        return 1
    elif modelname == 'LIF':
        return 2
    elif modelname == 'FN':
        return 3
    elif modelname == 'ML':
        return 4
    elif modelname == 'IZ':
        return 5
    elif modelname == 'HR':
        return 6
    elif modelname == 'HH':
        return 7
    else:
        return 0


def solverSelector(solvername):
    if solvername is None:
        raise TypeError
    if solvername == 'euler':
        return 1
    elif solvername == 'ord2':
        return 2
    elif solvername == 'rk4':
        return 3
    else:
        return 0


def Euler(t0=0, x0=np.array([1]), t1=5, dt=0.01, model=None):
    tsp = np.arange(t0, t1, dt)
    nsize = np.size(tsp)
    X = np.empty((nsize, np.size(x0)))
    X[0] = x0
    for i in range(0, nsize - 1):
        k1 = model(X[i], tsp[i])
        X[i + 1] = X[i] + k1 * dt
    return X


def SecondOrder(t0=0, x0=np.array([1]), t1=5, dt=0.01, model=None):
    tsp = np.arange(t0, t1, dt)
    nsize = np.size(tsp)
    X = np.empty((nsize, np.size(x0)))
    X[0] = x0
    for i in range(0, nsize - 1):
        k1 = model(X[i], tsp[i])
        k2 = model(X[i], tsp[i]) + k1 * (dt / 2)
        X[i + 1] = X[i] + k2 * dt
    return X


def RungeKutte4(t0=0, x0=np.array([1]), t1=5, dt=0.01, model=None):
    tsp = np.arange(t0, t1, dt)
    nsize = np.size(tsp)
    X = np.empty((nsize, np.size(x0)))
    X[0] = x0
    for i in range(1, nsize):
        k1 = model(X[i-1], tsp[i-1])
        k2 = model(X[i-1] + dt/2*k1, tsp[i-1] + dt/2)
        k3 = model(X[i-1] + dt/2*k2, tsp[i-1] + dt/2)
        k4 = model(X[i-1] + dt*k3, tsp[i-1] + dt)
        X[i] = X[i-1] + dt/6*(k1 + 2*k2 + 2*k3 + k4)
    return X


def VanDerPol(x, t):
    return np.array([x[1],
                    -x[0] + x[1]*(1-x[0]**2)])


def LeakyIntegrateandFire(x, t, u_th=-55, u_reset=-75, u_eq=-65, r=10, i=1.2):
    if x[0] >= u_th:
        x[0] = u_reset
    return np.array([-(x[0] - u_eq) + r*i])


def FitzhughNagumo(x, t, a=0.75, b=0.8, c=3, i=-0.40):
    return np.array([c*(x[0] + x[1] - x[0]**3/3 + i),
                    -1/c*(x[0] - a + b*x[1])])


def MorrisLecar(x, t, c=20, vk=-84, gk=8, vca=130, gca=4.4, vl=-60, gl=2, phi=0.04, v1=-1.2, v2=18, v3=2, v4=30,
                iapp=80):
    return np.array([(-gca*(0.5*(1 + mt.tanh((x[0] - v1)/v2)))*(x[0]-vca) - gk*x[1]*(x[0]-vk) - gl*(x[0]-vl) + iapp),
                    (phi*((0.5*(1 + mt.tanh((x[0] - v3)/v4))) - x[1]))/(1/mt.cosh((x[0] - v3)/(2*v4)))])


def Izhikevich(x, t, a=0.02, b=0.2, c=-65, d=2, i=10):
    if x[0] >= 30:
        x[0] = c
        x[1] = x[1] + d
    return np.array([0.04*(x[0]**2) + 5*x[0] + 140 - x[1] + i,
                    a*(b*x[0] - x[1])])


def HindmarshRose(x, t, a=1.0, b=3.0, c=1.0, d=5.0, r=0.006, s=4.0, i=1.3, xnot=-1.5):
    return np.array([x[1] - a*(x[0]**3) + (b*(x[0]**2)) - x[2] + i,
                    c - d*(x[0]**2) - x[1],
                    r*(s*(x[0] - xnot) - x[2])])


def HodgkinHuxley(x, t, g_K=36, g_Na=120, g_L=0.3, E_K=12, E_Na=-115, E_L=-10.613, C_m=1, I=-10):
    alpha_n = (0.01*(x[0]+10))/(mt.exp((x[0]+10)/10)-1)
    beta_n = 0.125*mt.exp(x[0]/80)
    alpha_m = (0.1*(x[0]+25))/(mt.exp((x[0]+25)/10)-1)
    beta_m = 4*mt.exp(x[0]/18)
    alpha_h = (0.07*mt.exp(x[0]/20))
    beta_h = 1 / (mt.exp((x[0]+30)/10)+1)
    return np.array([(g_K*(x[1]**4)*(x[0]-E_K) + g_Na*(x[2]**3)*x[3]*(x[0]-E_Na) + g_L*(x[0]-E_L) - I)*(-1/C_m),
                    alpha_n*(1-x[1]) - beta_n*x[1],
                    alpha_m*(1-x[2]) - beta_m*x[2],
                    alpha_h*(1-x[3]) - beta_h*x[3]])


def solutionGenerator(modelname, solvername):
    if int(modelSelector(modelname)) and modelSelector(modelname) in np.arange(1, 8):
        if int(solverSelector(solvername)) and solverSelector(solvername) in np.arange(1, 4):
            if solverSelector(solvername) == 1 and modelSelector(modelname) == 1:
                solution = Euler(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=VanDerPol)
                return solution
            elif solverSelector(solvername) == 2 and modelSelector(modelname) == 1:
                solution = SecondOrder(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=VanDerPol)
                return solution
            elif solverSelector(solvername) == 3 and modelSelector(modelname) == 1:
                solution = RungeKutte4(x0=np.array([0.01, 0.01]), t1=100, dt=0.01, model=VanDerPol)
                return solution
            elif solverSelector(solvername) == 1 and modelSelector(modelname) == 2:
                solution = Euler(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=LeakyIntegrateandFire)
                return solution
            elif solverSelector(solvername) == 2 and modelSelector(modelname) == 2:
                solution = SecondOrder(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=LeakyIntegrateandFire)
                return solution
            elif solverSelector(solvername) == 3 and modelSelector(modelname) == 2:
                solution = RungeKutte4(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=LeakyIntegrateandFire)
                return solution
            elif solverSelector(solvername) == 1 and modelSelector(modelname) == 3:
                solution = Euler(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=FitzhughNagumo)
                return solution
            elif solverSelector(solvername) == 2 and modelSelector(modelname) == 3:
                solution = SecondOrder(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=FitzhughNagumo)
                return solution
            elif solverSelector(solvername) == 3 and modelSelector(modelname) == 3:
                solution = RungeKutte4(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=FitzhughNagumo)
                return solution
            elif solverSelector(solvername) == 1 and modelSelector(modelname) == 4:
                solution = Euler(x0=np.array([0, 0]), t1=100, dt=0.02, model=MorrisLecar)
                return solution
            elif solverSelector(solvername) == 2 and modelSelector(modelname) == 4:
                solution = SecondOrder(x0=np.array([0, 0]), t1=100, dt=0.02, model=MorrisLecar)
                return solution
            elif solverSelector(solvername) == 3 and modelSelector(modelname) == 4:
                solution = RungeKutte4(x0=np.array([0, 0]), t1=100, dt=0.02, model=MorrisLecar)
                return solution
            elif solverSelector(solvername) == 1 and modelSelector(modelname) == 5:
                solution = Euler(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=Izhikevich)
                return solution
            elif solverSelector(solvername) == 2 and modelSelector(modelname) == 5:
                solution = SecondOrder(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=Izhikevich)
                return solution
            elif solverSelector(solvername) == 3 and modelSelector(modelname) == 5:
                solution = RungeKutte4(x0=np.array([0.01, 0.01]), t1=100, dt=0.02, model=Izhikevich)
                return solution
            elif solverSelector(solvername) == 1 and modelSelector(modelname) == 6:
                solution = Euler(x0=np.array([0.01, 0.01, 0.01]), t1=100, dt=0.02, model=HindmarshRose)
                return solution
            elif solverSelector(solvername) == 2 and modelSelector(modelname) == 6:
                solution = SecondOrder(x0=np.array([0.01, 0.01, 0.01]), t1=100, dt=0.02, model=HindmarshRose)
                return solution
            elif solverSelector(solvername) == 3 and modelSelector(modelname) == 6:
                solution = RungeKutte4(x0=np.array([0.01, 0.01, 0.01]), t1=100, dt=0.02, model=HindmarshRose)
                return solution
            elif solverSelector(solvername) == 1 and modelSelector(modelname) == 7:
                solution = Euler(x0=np.array([0.01, 0.01, 0.01, 0.01]), t1=100, dt=0.02, model=HodgkinHuxley)
                return solution
            elif solverSelector(solvername) == 2 and modelSelector(modelname) == 7:
                solution = SecondOrder(x0=np.array([0.01, 0.01, 0.01, 0.01]), t1=100, dt=0.02, model=HodgkinHuxley)
                return solution
            elif solverSelector(solvername) == 3 and modelSelector(modelname) == 7:
                solution = RungeKutte4(x0=np.array([0.01, 0.01, 0.01, 0.01]), t1=100, dt=0.02, model=HodgkinHuxley)
                return solution
            else:
                solution = "Cheese please!"
                return solution


if __name__ == '__main__':
    x = modelSelector('ML')
    print(x)
    y = solverSelector('rk4')
    print(y)
    z = solutionGenerator('HH', 'rk4')
    print(z)