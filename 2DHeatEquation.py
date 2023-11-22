#Wave plotter
#Caleb Bessit
#13 November 2023

# import numpy as np
import matplotlib
# import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter


import matplotlib.pyplot as plt
import numpy as np

terms = 50      #Number of terms to sum to


def C(n,m):
    # return (200/(n*m * np.pi**2) )* np.power(-1,n) * np.power(-1,m)
    return (400/(n*m * np.pi**2) ) * (  np.cos(n*np.pi) -1 ) * (np.cos(m*np.pi) -1)

def Lambda(n,m):
    # return ( (m*np.pi)/5)**2 + ( (n*np.pi)/5)**2
    return ( (m*np.pi)/20)**2 + ( (n*np.pi)/10)**2

def u(x,y,t):

    result = 0

    for n in range(1,terms+1):
        for m in range(1,terms+1):
            result += C(n,m) * np.sin( (n*np.pi*x)/10) * np.sin( (m*np.pi*y)/20) * np.exp(-1* Lambda(n,m)*t)

    return result

x_vals, y_vals = np.linspace(0,10,200), np.linspace(0,20,200)

X, Y = np.meshgrid(x_vals, y_vals)

heatDistribution = u(X,Y,0)

fig, ax = plt.subplots()
im = ax.imshow(heatDistribution, cmap='viridis',extent=[0, 10, 0, 20], origin='lower')
ax.set_title('Heat Distibution using initial condition u(x,y,0)=100')

fig.colorbar(im, ax=ax, label='Temperatures')

# plt.show()

metadata    = dict(title="Movie", artist="Caleb")
writer      = PillowWriter(fps=15, metadata=metadata)

t_vals      = []
heat_vals   = []



with writer.saving(fig,"HeatDistribution100.gif",100):
    
    for t in np.linspace(0,5,100):
        #Get value and update
        t_vals.append(t)
        print("Processing {}".format(t))
        heatDistribution = u(X,Y,t)
        heat_vals.append(heatDistribution)

        im = ax.imshow(heatDistribution, cmap='viridis',extent=[0, 10, 0, 20], origin='lower')
        ax.set_title('Heat Distibution using initial condition u(x,y,0)=100')
        


        #Stitching
        writer.grab_frame()
        plt.cla()

