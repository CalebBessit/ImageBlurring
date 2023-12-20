#Using the numerically computed heat equation to blur images
#Caleb Bessit
#19 November 2023

import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

#Global variables
rows, cols          = 0,0
time                = 100
imageData           = []

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
    for i in range(len(imageData)):
        imageData[i] = int(imageData[i])

    
    imageData = np.array(imageData).reshape((cols,rows))
    imageData = np.pad(imageData, 1, 'constant')
    original  = imageData.copy()

    rows, cols = cols, rows

    
    fig, ax = plt.subplots()
 

    ax.set_title('Image At 0 Time Steps',fontsize=18)
    image = plt.imshow(imageData, cmap=plt.cm.gray)
    plt.colorbar(image)
    
    metadata    = dict(title="Movie", artist="Caleb")
    writer      = PillowWriter(fps=15, metadata=metadata)

    t_vals      = []
    image_vals   = []


    savePath = "BlurredImages/BlurringGrey{}.gif".format(fileNames[index])
    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    with writer.saving(fig,savePath,150):
        for t in tqdm(range(1, time + 1), desc='Processing image', unit=' still images'):
            t_vals.append(t)

            left, right = imageData[1:rows+1,0:cols], imageData[1:rows+1,2:cols+2]
            top, bottom = imageData[0:rows,1:cols+1], imageData[2:rows+2,1:cols+1]
            current     = imageData[1:rows+1, 1:cols+1]
            imageData = np.pad(timeStepUpdate(current, left, right, top, bottom), 1, 'constant')

            image_vals.append(imageData)
            ax.set_title('Blurring {} using heat equation'.format(fileNames[index]),fontsize=18)
            ax.set_xlabel("Time steps: {}".format(t))
            image = plt.imshow(imageData, cmap=plt.cm.gray)

            # print("Processed {}".format(t))

            #Stitching
            writer.grab_frame()
            plt.cla()

        print("Saving data as a .GIF to file...")
    
    print("Done.")
#Current is the center pixel in an image, the other variables represent the pixels in that direction
#with respect to the current pixel
def timeStepUpdate(current, left, right, top, bottom, dt=0.1):
    laplacian = left + right + top + bottom -4*current
    return current + dt*laplacian

if __name__ == "__main__":
    main()
