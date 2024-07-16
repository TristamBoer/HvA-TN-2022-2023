import numpy as np
import matplotlib.pyplot as plt

# Constanten
nu_drive = 4000 
m = 4.9e-09
y = 1.7e-06
fcor = 8e-9
k = fcor**2 * 4*np.pi**2 * m
ohm = 1/6

# Bepalen tijd
trillingen = 5000
trillingstijd = 2*np.pi*np.sqrt(m/k)
Nstap = trillingen*100
tijd = np.linspace(0, trillingstijd*trillingen, Nstap)
dt = trillingstijd*trillingen / Nstap

a = (k - 2*m / (dt**2)) / (m / (dt**2) + y / (2*dt))
b = ( m / (dt**2) - y / (2*dt)) / (m / (dt**2) + y / (2*dt))
F0e = fcor * ohm / (m / (dt**2) + y / (2*dt))

# Begin waarden
x0 = 0
v0 = 0 

# Posities en eerste stap
x = np.zeros_like(tijd)
x[0] = 0
x[1] = x0 + dt * v0

for ti in range(1, Nstap-1):
    x[ti+1] = -a*x[ti] - b*x[ti-1] + F0e * np.cos(nu_drive*tijd[ti])
    
plt.plot(tijd,x)
plt.show()