from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({'font.size': 12})

def dy(y, t, R, L, C):
    """
    RHS van bovenstaande vergelijkingen. y is een vector (x, p).
    """
    x, p = y[0] , y[1]
    dx = p
    dp = -(R/L)*p-(1/(C*L))*x
    return [dx,dp]

I0= 0.15 # stroom I(t=0) in Ampere
y0 = [I0,0] # randvoorwaarden x(t=0), p(t=0)

t = np.linspace(0,30,int(1e3))*1e-3

R = 45 # Ohm
L = 10e-3 # Henry's
C = 100e-6 # Farad

sol = odeint(dy, y0, t, args=(R, L, C)) # solution

plt.figure(dpi=300)
plt.plot(t*1e3, sol[:,0]*1e3/R, 'r') # sol[:,0] is de stroom I(t)
plt.grid()
plt.xlabel(r"Tijd $t$ [ms]")
plt.ylabel(r"$V(t)$ [mV]")