#Using the numerically computed heat equation to blur images: version with periodic boundary conditions
#Caleb Bessit
#20 December 2023

import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

#Global variables
rows, cols          = 0,0
time                = 500
imageData           = []

#Current is the center pixel in an image, the other variables represent the pixels in that direction
#with respect to the current pixel
def timeStepUpdate(current, left, right, top, bottom, dt=0.1):
    laplacian = left + right + top + bottom -4*current
    return current + dt*laplacian

#This method returns the array slice in the indicated direction. For pixels on the boundaries, it wraps 
#around in a virutal torus
def shift(centerImage, direction,rows,cols):
    if direction=="left":
        return np.hstack((centerImage[:,cols-1:cols], centerImage[:,:cols-1]))
    elif direction =="right":
        return np.hstack((centerImage[:,1:cols], centerImage[:,0:1])) 
    elif direction =="top":
        return np.vstack((centerImage[rows-1:rows,:],centerImage[:rows-1,:])) 
    elif direction =="bottom":
        return np.vstack((centerImage[1:rows,:],centerImage[0:1,:])) 

def main():
    global rows, cols, imageData
    #File processing and management
    fileNames = ["Test16","Explosion","Fence","Heh","Ishigami","Pikachu","PowerLines","Shirogane","Tower","Tree"]
    index = 5
    file = open("TestImages/Grey{}.ppm".format(fileNames[index]),"r")

    #Load image data from file and remove newline characters
    for line in file.readlines():
        line = line.replace("\n","")
        imageData.append(line)

    #Close file and extract pixel and heading characters
    file.close()
    imageData= imageData[2:]
    rows, cols = imageData[0].split(" ")
    rows, cols = int(rows), int(cols)

    imageData = imageData[2:]

    #Convert pixel values to integers
    imageData = [  int(i) for i in imageData  ]
    
    imageData = np.array(imageData).reshape((cols,rows))
    rows, cols = cols, rows

    fig, ax = plt.subplots()
 
    ax.set_title('Image At 0 Time Steps',fontsize=18)
    image = plt.imshow(imageData, cmap=plt.cm.gray)
    plt.colorbar(image)

    metadata    = dict(title="Movie", artist="Caleb")
    writer      = PillowWriter(fps=15, metadata=metadata)

    t_vals      = []
    image_vals   = []

    savePath = "BlurredImages/BlurringGrey{}Torus.gif".format(fileNames[index])
    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    with writer.saving(fig,savePath,150):
        for t in tqdm(range(1, time + 1), desc='Processing image', unit=' still images'):
            t_vals.append(t)

            left, right = shift(imageData,"left",rows,cols), shift(imageData,"right",rows,cols)
            top, bottom = shift(imageData,"top",rows,cols), shift(imageData,"bottom",rows,cols)
            imageData = timeStepUpdate(imageData, left, right, top, bottom)

            image_vals.append(imageData)
            ax.set_title('Blurring {} using torus boundaries'.format(fileNames[index]),fontsize=18)
            ax.set_xlabel("Time steps: {}".format(t))
            image = plt.imshow(imageData, cmap=plt.cm.gray)

            #Stitching
            writer.grab_frame()
            plt.cla()

        print("Saving data as a .GIF to file...")
    
    print("Done.")


if __name__ == "__main__":
    main()
