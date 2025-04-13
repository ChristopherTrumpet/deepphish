import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

df = pd.read_csv('data.csv')
x_col = 'TechScore'
y_col = 'Age'
z_col = 'Risk'

xi = np.linspace(df[x_col].min(), df[x_col].max(), 100)
yi = np.linspace(df[y_col].min(), df[y_col].max(), 100)
xi, yi = np.meshgrid(xi, yi)

zi = griddata((df[x_col], df[y_col]), df[z_col], (xi, yi), method='cubic')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xi, yi, zi, cmap='viridis', alpha=0.8)

ax.set_xlabel('Tech Score')
ax.set_ylabel(y_col)
ax.set_zlabel(z_col)
ax.set_title('3D Risk Surface')
plt.savefig('3d_risk_surface.png')
plt.show()