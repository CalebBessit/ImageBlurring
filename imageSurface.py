#Plotting an image as a 2D surface


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

#Global variables
xExtent, yExtent    = 0,0
terms               = 10
imageData           = []

def u(x,y,t):
    global terms, xExtent, yExtent
    result = 0

    for n in range(0,terms):
        for m in range(0,terms):
            result += C(n,m) * np.cos( (n*np.pi*x)/xExtent) * np.cos( (m*np.pi*y)/yExtent) * np.exp( Lambda(n,m)*t)

    return result

def Lambda(n,m):
    global xExtent, yExtent
    return  ( (n*np.pi)/xExtent)**2   + ( (m*np.pi)/yExtent)**2 

def C(n,m):
    global imageData, xExtent
    # return ((4* (imageData)) /(m*n*np.pi**2)) * (1 - np.cos(n*np.pi)) * (1-np.cos(m*np.pi)) 
    if (n==0 and m==0):
        return imageData
    else:
        return 0

def main():
    global imageData, xExtent, yExtent

    #File processing and management
    fileNames = ["Test16","Explosion","Fence","Heh","Ishigami","Pikachu","PowerLines","Shirogane","Tower","Tree"]
    index = 5
    file = open("TestImages\Grey{}.ppm".format(fileNames[index]),"r")

    #Load image data from file and remove newline characters
    for line in file.readlines():
        line = line.replace("\n","")
        imageData.append(line)

    #Close file and extract pixel and heading characters
    file.close()
    imageData= imageData[2:]
    xExtent, yExtent = imageData[0].split(" ")
    xExtent, yExtent = int(xExtent), int(yExtent)

    imageData = imageData[2:]

    #Convert pixel values to integers
    for i in range(len(imageData)):
        imageData[i] = int(imageData[i])

    fig, ax = plt.subplots()

    #Convert linear array to 2D np array
    imageData = np.array(imageData).reshape((yExtent, xExtent))
    # print(imageData)

    #Convert back to regular 2D list, then reverse rows so that values displayed correctly
    # imageData =  np.ndarray.tolist(imageData)
    # imageData.reverse()
    # imageData = np.array(imageData)

    # print("xExtent: {}, yExtent: {}".format(xExtent, yExtent))

    '''Iterations of heat equation'''
    x_vals, y_vals = np.linspace(0,xExtent-1,xExtent).astype(int), np.linspace(0,yExtent-1,yExtent).astype(int)

    X, Y = np.meshgrid(x_vals, y_vals)

    # print("Image data:", imageData)
    # print("X:", X,"Y:", Y)
    
    # imageDistribution = imageData
    #Display image
    # ax.set_xlim(xmin=0, xmax=xExtent)
    # ax.set_ylim(ymin=0, ymax=yExtent)
    # print(imageDistribution)

    # print(np.shape(np.array(X)))
    # print(np.shape(np.array(Y)))
    # print(np.shape(np.array(imageDistribution)))

    imageDistribution = u(X,Y,0)
    ax.set_title("{} under the influence of the heat equation".format(fileNames[index]))
    
    ax.set_xlim(xmin=0, xmax=xExtent)
    ax.set_ylim(ymin=0, ymax=yExtent)
    imageDisplay =  np.ndarray.tolist(imageDistribution)
    imageDisplay.reverse()
    imageDisplay = np.array(imageDisplay)
    imagePlot = plt.imshow(imageDisplay, cmap='gray', vmin=0, vmax=255, origin='upper')
    plt.colorbar(imagePlot)

    metadata    = dict(title="Movie", artist="Caleb")
    writer      = PillowWriter(fps=15, metadata=metadata)

    t_vals      = []
    image_vals   = []

    with writer.saving(fig,"{}ImageUnderHeatNeumann1.gif".format(fileNames[index]),100):
    
        for t in np.linspace(0,15000,100):
            #Get value and update
            t_vals.append(t)
            print("Processing {}".format(t))
            imageDistribution = u(X,Y,t)
            image_vals.append(imageDistribution)

            ax.set_title("{} under the influence of the heat equation".format(fileNames[index]))
            ax.set_xlabel("t={:.3f} seconds".format(t))
            ax.set_xlim(xmin=0, xmax=xExtent)
            ax.set_ylim(ymin=0, ymax=yExtent)
            imageDisplay =  np.ndarray.tolist(imageDistribution)
            imageDisplay.reverse()
            imageDisplay = np.array(imageDisplay)
            imagePlot = plt.imshow(imageDisplay, cmap='gray', vmin=0, vmax=255, origin='upper')
            
            #Stitching
            writer.grab_frame()
            plt.cla()


if __name__ == "__main__":
    main()



