import numpy as np
import matplotlib.pyplot as plt

# Constanten Stap 1
V0          = 15
V_drive     = 1.5
l_drive     = 200e-6
d_drive     = 2e-6
w_drive     = 3e-6
A_drive     = l_drive * w_drive
N_drive     = 100
kappa       = 1.00059
epsilon0    = 8.854e-12

# Constanten stap 2
m_drive      = 5.1e-09                                         
k_drive      = 0.2013                                          
y_drive      = 4.9299e-07                                      
omega0_drive = np.sqrt(k_drive / m_drive)                            

# Constanten stap 3
ohm = 1/6

# Constanten stap 4
m_sense       = 6.12e-9
k_sense       = 0.9664
y_sense       = 1.538e-6
omega0_sense  = np.sqrt(k_sense / m_sense)

# Constanten stap 5
l_sense = 200e-6
d_sense = 2-6
w_sense = 3e-6
A_sense = l_sense * w_sense
N_sense = 40
Vdc     = 15                     

# Bepalen tijd drive mode
trillingen    = 500
trillingstijd = 2 * np.pi * np.sqrt(m_drive / k_drive)
Nstap         = trillingen * 300 
tijd          = np.linspace(0, trillingstijd * trillingen, Nstap)
dt            = trillingstijd * trillingen / Nstap

V = V0 + V_drive * np.cos(omega0_drive * tijd) 

plt.plot(tijd, V, 'r')
plt.xlabel('Tijd [s]')
plt.ylabel('$Spanning_{drive mode}$ [V]')
plt.title("Wisselspanning tegen de tijd")
plt.grid()
plt.show()

def Berekenen_Fel(V0, omega0_drive, tijd, epsilon0, kappa, A_drive, d_drive):
    V      = V0 + V_drive * np.cos(omega0_drive * tijd) 
    Fel0c = N_drive * 0.5 * V**2 * kappa * epsilon0 * A_drive / d_drive 
    return Fel0c

Fel0c = Berekenen_Fel(V0, omega0_drive, tijd, epsilon0, kappa, A_drive, d_drive)

plt.plot(tijd, Fel0c, 'c')
plt.xlabel('Tijd [s]')
plt.ylabel('$Aandrijvingskracht_{drive mode}$ [N]')
plt.title("$Aandrijvingskracht_{drive mode}$ tegen de tijd")
plt.grid()
plt.show()

a   = (k_drive - 2 * m_drive / (dt**2)) / (m_drive / (dt**2) + y_drive / (2 * dt))
b   = (m_drive / (dt**2) - y_drive / (2 * dt)) / (m_drive / (dt**2) + y_drive / (2 * dt))
Fele = Fel0c / (m_drive / (dt**2) + y_drive / (2 * dt))

# Begin waarden
x0 = 0
v0 = 0 

# Posities en eerste stap
x1     = np.zeros_like(tijd)
x1[0]  = 0
x1[1]  = x0 + dt*v0

x2     = np.zeros_like(tijd)
x2[0]  = 0
x2[1]  = x0 + dt*v0

# Berekenen van de uitwijking drive mode
for i in range(1, Nstap-1):
    x1[i+1] = -a * x1[i] - b * x1[i-1] + Fele[i] #* np.cos(omega0_drive * tijd[i])

plt.plot(tijd, x1)
plt.xlabel('Tijd [s]')
plt.ylabel('$Uitwijking_{drive mode}$ [m]')
plt.title("$Uitwijking_{drive mode}$ tegen de tijd")
plt.grid()
plt.show()

# Bepalen tijd sense mode
trillingen    = 500
trillingstijd = 2 * np.pi * np.sqrt(m_sense / k_sense)
Nstap         = trillingen * 300
tijd          = np.linspace(0, trillingstijd * trillingen, Nstap)
dt            = trillingstijd * trillingen / Nstap

def Berekenen_Fcor(x1, m_sense, dt):
    for i in range(1, Nstap-1):
        snelheid_drive = (x1[i+1] - x1[i-1]) / dt * 2
    
    fcor = -2 * ohm * m_drive * snelheid_drive
    return fcor

fcor = Berekenen_Fcor(x1, m_sense, dt)

a   = (k_sense - 2 * m_sense / (dt**2)) / (m_sense / (dt**2) + y_sense / (2 * dt))
b   = (m_sense / (dt**2) - y_sense / (2 * dt)) / (m_sense / (dt**2) + y_sense / (2 * dt))
Fcore = fcor / (m_sense / (dt**2) + y_sense / (2*dt))

# Berekenen van de uitwijking sense mode
for i in range(1, Nstap-1):
    x2[i+1] = -a * x2[i] - b * x2[i-1] + Fcore * np.cos(omega0_sense * tijd[i])
    
plt.plot(tijd, x2)
plt.xlabel('Tijd [s]')
plt.ylabel('$Uitwijking_{sense mode}$ [m]')
plt.title("$Uitwijking_{sense mode}$ tegen de tijd")
plt.grid()
plt.show()

def Berekenen_stroom(kappa, epsilon0, A_drive, d_drive, Vdc, omega0_sense):
    Capaciteit = kappa * epsilon0 * A_drive / (d_drive - x2)
    
    stroomsterkte = Capaciteit * Vdc * omega0_sense * np.cos(omega0_sense)
    
    return stroomsterkte

stroom = Berekenen_stroom(kappa, epsilon0, A_drive, d_drive, Vdc, omega0_sense)


plt.plot(tijd, stroom, 'y')
plt.xlabel('Tijd [s]')
plt.ylabel('$Stroomsterkte_{sense mode}$ [A]')
plt.title("$Stroomstertke_{sense mode}$ tegen de tijd")
plt.grid()
plt.show()

# Berekenen transfercoëfficenten:
Fel_max = np.max(Fel0c)
V_drive_max = np.max(V_drive * np.cos(omega0_drive * tijd))
eta1 = Fel_max / V_drive_max

x1_max = np.max(x1)
eta2 = x1_max/Fel_max

Fcor_max = np.max(Fcore)
eta3 = Fcor_max/x1_max

x2_max = np.max(x2)
eta4 = x2_max/Fcor_max

I_max = np.max(stroom)
eta5 = I_max/x2_max

print("Transfercoëfficiënt 1 (η1) tussen Fel en V: ", eta1)
print("Transfercoëfficiënt 2 (η2) tussen x1 en Fel: ", eta2)
print("Transfercoëfficiënt 3 (η3) tussen Fcor en x1: ", eta3)
print("Transfercoëfficiënt 4 (η4) tussen x2 en Fcor: ", eta4)
print("Transfercoëfficiënt 5 (η5) tussen I en x2: ", eta5)