import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')

# Aflezen van de .txt bestanden.
lijst1 = np.loadtxt('posities_1_Team_A6.txt')
lijst2 = np.loadtxt('posities_2_Team_A6.txt')

afstand1 = lijst1[:, 1]
afstand2 = lijst2[:, 1]


# Berekenen van versnelling
def versnelling(afstand):
    versnelling_lijst = []
    for i in range(len(afstand) - 1):
        versnelling = (afstand[i+1] - 2*afstand[i] + afstand[i-1]) / (3e-2/5e4)**2
        versnelling_lijst.append(versnelling)
    return np.array(versnelling_lijst)


versnelling1 = np.delete(versnelling(afstand1), 0)
versnelling2 = np.delete(versnelling(afstand2), 0)

# Constanten
m = 1845e-9
k = 40
y1 = np.sqrt(4*m*k)
y2 = 0.42953
y3 = 0.2

# Bepalen tijd
t_eind = 0.03
N_stap = len(afstand1) - 2
tijd = np.linspace(0, t_eind, N_stap)
dt = t_eind / (N_stap-1)


def a_constant(y):
    a = (k - 2*m/dt**2)/(m/dt**2 + y/(2*dt))
    return a

def b_constant(y):
    b = (m/dt**2 - y/(2*dt))/(m/dt**2 + y/(2*dt))
    return b


a1 = a_constant(y1)
a2 = a_constant(y2)
a3 = a_constant(y3)

b1 = b_constant(y1)
b2 = b_constant(y2)
b3 = b_constant(y3)

# Begin condities
x0 = 0
v0 = 0

# Posities en eerste stap
x = np.zeros_like(tijd)
x[0] = x0
x[1] = x0 + dt*v0


# Berekenen van uitwijkingen van de versnellingen
def uitwijking(a, b, versnelling_profiel):
    for i in range(1, N_stap-1):
        x[i+1] = -a*x[i] - b*x[i-1] + versnelling_profiel[i]
    return x


x1 = uitwijking(a1, b1, versnelling1)
x2 = uitwijking(a1, b1, versnelling2)       # Kritisch gedempt
x3 = uitwijking(a2, b2, versnelling2)       # Over gedempt
x4 = uitwijking(a3, b3, versnelling2)       # Onder gedempt

fig1, ax1 = plt.subplots()
ax1.set_xlabel('time [s]')
ax1.set_ylabel('versnelling [$m/s^2$]', color='tab:red', weight='bold')
ax1.plot(tijd, versnelling1, color='tab:red', label='versnelling')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax2 = ax1.twinx()
ax2.set_ylabel('uitwijking [m]', color='tab:blue', weight='bold')
ax2.plot(tijd, x1, color='tab:blue', label='uitwijking')
ax2.tick_params(axis='y', labelcolor='tab:blue')
plt.title("Uitwijking bij versnellingsprofiel 1")
fig1.tight_layout()

fig2, ax1 = plt.subplots()
ax1.set_xlabel('time [s]')
ax1.set_ylabel('versnelling [$m/s^2$]', color='tab:red', weight='bold')
ax1.plot(tijd, versnelling2, color='tab:red', label='versnelling')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax2 = ax1.twinx()
ax2.set_ylabel('uitwijking [m]', color='tab:blue', weight='bold')
ax2.plot(tijd, x2, color='tab:blue', label='uitwijking')
ax2.tick_params(axis='y', labelcolor='tab:blue')
plt.title("Uitwijking bij versnellingsprofiel 2")
fig2.tight_layout()

fig3 = plt.figure()
plt.plot(tijd, x2, color='tab:red', label='kritisch gedempt')
plt.plot(tijd, x3, color='tab:blue', label='over gedempt')
plt.plot(tijd, x4, color='tab:green', label='onder gedempt')
plt.xlabel('tijd [s]')
plt.ylabel('uitwijking [m]')
plt.legend()
plt.title("Uitwijking bij verschillende dempingen")
fig3.tight_layout()

if __name__ == "__main__":
    fig1.show()
    fig2.show()
    fig3.show()
