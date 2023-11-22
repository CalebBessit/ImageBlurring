#2D Wave equation
#Caleb Bessit
#14 November 2023

import numpy as np
import matplotlib.cm as cm
import scipy.special as special
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from matplotlib.animation import PillowWriter

#Globals
a       = 2
c       = 1
terms   = 10
lambda_n  = np.ndarray.tolist(    special.jn_zeros(0,terms)/a    )


#Helping methods for conversion to polar coordinates
def calcR(angle, x=2, y=2):
  return np.sqrt((x*y)/(x*np.cos(angle)**2 + y*np.sin(angle)**2))
def stretch_mesh(r, theta):
  return [ r[i] * calcR(theta[i][0]) for i in range(len(r)) ]


def R(x,y):
  return np.sqrt( x*x + y*y )

#Coefficients
def a_n(n):
  global a
  numerator = integrate.quad(lambda x: alpha(x)*special.j0(lambda_n[n-1]*x)*x,0,a)[0]

  denominator = integrate.quad(lambda x: (special.j0(lambda_n[n-1]*x)**2) *x,0,a)[0]

  return numerator/denominator

def b_n(r):
  pass

#Initial functions
def alpha(r):
  global a
  return np.cos(  (np.pi/a)*r  ) +1


#Wave calculation
def u(x,y,t):
  r = R(x,y)

  result = 0
  
  for n in range(1,terms+1):
    result += a_n(n) * np.cos(c* lambda_n[n-1]*t) * special.j0(lambda_n[n-1]*r)


  return result


#Create polar mesh
r = np.linspace(0, a, 100)
theta = np.linspace(0, 2*np.pi, 100)
r, theta = np.meshgrid(r, theta)
# Stretch Function
r= stretch_mesh(r, theta)
# Transform to Cartesian
X = r * np.sin(theta)
Y = r * np.cos(theta)
wave = u(X,Y,0)

# fig = plt.figure(figsize=(10, 11))
# ax = fig.add_subplot(111, projection='3d')
# ax.set_zlim(0, 3)

# # Plot the initial surface
# surf = ax.plot_surface(X, Y, wave, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
# m = plt.cm.ScalarMappable(cmap='viridis')
# m.set_array(wave)
# plt.colorbar(m)

fig = plt.figure(figsize=(10, 11))
ax = fig.add_subplot(111, projection='3d')
ax.set_zlim(0, 2)

# Plot the initial surface
surf = ax.plot_surface(X, Y, wave, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
m = plt.cm.ScalarMappable(cmap='viridis')
m.set_array(wave)
plt.colorbar(m)


# Function to update the plot for each frame
def update_plot(t):
    wave = u(X, Y, t)
    surf = ax.plot_surface(X, Y, wave, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_title("Wave equation, with cosine-like initial condition")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return surf

# Animation settings
metadata = dict(title="Wave Animation", artist="Caleb")
writer = PillowWriter(fps=15, metadata=metadata)

# Generate and save the animation
with writer.saving(fig, "2DWave.gif", 100):
    for t in np.linspace(0, 3, 20):
        print("Processing {}".format(t))
        surf.remove()  # Remove the previous surface for the next frame
        surf = update_plot(t)
        writer.grab_frame()
        








# #Producing and saving gif to file
# metadata    = dict(title="Movie", artist="Caleb")
# writer      = PillowWriter(fps=15, metadata=metadata)
# t_vals = []
# wave_vals = []

# with writer.saving(fig,"2DWave.gif",100):
  
#     for t in np.linspace(0,3,20):
#       t_vals.append(t)
#       print("Processing {}".format(t))

#       wave = u(X,Y,t)
#       wave_vals.append(wave)
#       ax.set_title("Wave equation, with cosine-like initial condition")
#       ax.set_xlabel("x")
#       ax.set_ylabel("y")
#       surf = ax.plot_surface(X, Y, wave, rstride=1, cstride=1, cmap='viridis', edgecolor='none');
#     #   m = cm.ScalarMappable(cmap=surf.cmap, norm=surf.norm)

#       writer.grab_frame()
#       plt.cla()








