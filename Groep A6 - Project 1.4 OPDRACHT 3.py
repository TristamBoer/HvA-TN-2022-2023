import numpy as np
import matplotlib.pyplot as plt

# Constanten
m = 5.1e-06
k = 0.2013
y = 4.9299e-07
F0 = 60e-06
o = np.sqrt(k/m)

# Bepalen tijd
trillingen = 5000
trillingstijd = 2*np.pi*np.sqrt(m/k)
Nstap = trillingen*100
tijd = np.linspace(0, trillingstijd*trillingen, Nstap)
dt = trillingstijd*trillingen / Nstap

a = (k - 2*m / (dt**2)) / (m / (dt**2) + y / (2*dt))
b = ( m / (dt**2) - y / (2*dt)) / (m / (dt**2) + y / (2*dt))
F0e = F0 / (m / (dt**2) + y / (2*dt))

# Begin waarden
x0 = 0
v0 = 0 

# Posities en eerste stap
x = np.zeros_like(tijd)
x[0] = 0
x[1] = x0 + dt * v0

for ti in range(1, Nstap-1):
    #x[ti+1] = -a*x[ti] - b*x[ti-1] + F0e                       # Statische kracht
    x[ti+1] = -a*x[ti] - b*x[ti-1] + F0e*np.sin(o*tijd[ti])     # Oscillerende kracht
   
maximum = np.amax(x)
minimum = np.amin(x)

#print(maximum)
#print(minimum)

amplitude = (maximum - minimum) / 2

print(amplitude)

plt.plot(tijd, x)
plt.title("Horizontale uitwijking tegen de tijd")
plt.xlabel('tijd [s]')
plt.ylabel('horizontale uitwijking [m]')
plt.show