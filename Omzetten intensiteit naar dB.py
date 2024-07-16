import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(1*10**-12,100,1000)
y =  10 * np.log10(x / (1 * 10**-12))

plt.plot(x,y)
plt.xlabel('Gemeten Intensiteit (W/m^2)')
plt.ylabel('Geluidssterkte (dB)')
plt.show()
