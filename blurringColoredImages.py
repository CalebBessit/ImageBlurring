#Using the heat equation to blur color images
#Caleb Bessit
#20 November 2023

'''Imports'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

'''Global variables'''
R, G, B     = [], [], []
imageData   = []
rows, cols  = 0,0
time        = 100

#Current is the center pixel in an image, the other variables represent the pixels in that direction
#with respect to the current pixel
def timeStepUpdate(current, left, right, top, bottom, dt=0.1):
    laplacian = left + right + top + bottom -4*current
    return current + np.rint(dt*laplacian).astype(int)

def extract(array, rows, cols):
    return array[1:rows+1,1:cols+1]

def main():
    global R,G,B, imageData, rows, cols

    #File processing
    fileNames = ["","IronValiant","SmolPikachu","TestPikachu","TestIshigami"]
    index = 4
    file = open("TestImages\Grey{}.ppm".format(fileNames[index]),"r")

    #Load image data from file
    imageData = [s.replace("\n", '') for s in file.readlines()]

    #Close file and extract pixel and heading characters
    file.close()
    imageData= imageData[2:]
    rows, cols = imageData[0].split(" ")
    rows, cols = int(rows), int(cols)

    imageData = imageData[2:]

    #Convert pixel values to integers
    imageData = list(map(int, imageData))
    
    #Split image data into red, green and blue pixels
    R, G, B = imageData[::3], imageData[1::3], imageData[2::3]

    

    #Convert to 2D arrays and pad

    R, G, B = np.array(R).reshape((rows, cols)), np.array(G).reshape((rows, cols)), np.array(B).reshape((rows, cols))
    R, G, B = np.pad(R,1,'constant'), np.pad(G,1,'constant'), np.pad(B,1,'constant')
    

    #Swap rows and columns to extract data logically
    # rows, cols = cols, rows

    #Display initial image
    fig, ax = plt.subplots()
    ax.set_title('Image At 0 Time Steps',fontsize=18)
    R, G, B = extract(R,rows,cols)  ,  extract(G,rows,cols),   extract(B,rows,cols)

    #Swap back rows and columns to display correctly
    rows, cols = cols, rows
    R, G, B = R.reshape((1,rows*cols))[0], G.reshape((1,rows*cols))[0], B.reshape((1,rows*cols))[0]
    result = np.vstack(( R, G, B ))
    result = result.T
    result = result.reshape(rows,cols,3)

    rows, cols = cols, rows

    #Display image
    plt.imshow(result)
    R, G, B = np.ndarray.tolist(R), np.ndarray.tolist(G), np.ndarray.tolist(B)
    

    
    metadata    = dict(title="Movie", artist="Caleb")
    writer      = PillowWriter(fps=15, metadata=metadata)

    t_vals      = []
    image_vals   = []
    with writer.saving(fig,"BlurringColor{}.gif".format(fileNames[index]),100):

        for t in range(1,time+1):
            t_vals.append(t)

            #Convert to 2D arrays and pad
            R, G, B = np.array(R).reshape((rows, cols)), np.array(G).reshape((rows, cols)), np.array(B).reshape((rows, cols))
            R, G, B = np.pad(R,1,'constant'), np.pad(G,1,'constant'), np.pad(B,1,'constant')
            

            #Perform and return calculations:

            # Processing red pixels
            leftR, rightR   = R[1:rows+1,0:cols], R[1:rows+1,2:cols+2]
            topR, bottomR   = R[0:rows,1:cols+1], R[2:rows+2,1:cols+1]
            currentR        = R[1:rows+1, 1:cols+1]
            R               = np.pad(timeStepUpdate(currentR, leftR, rightR, topR, bottomR), 1, 'constant')

            #Processing blue pixels
            leftB, rightB   = B[1:rows+1,0:cols], B[1:rows+1,2:cols+2]
            topB, bottomB   = B[0:rows,1:cols+1], B[2:rows+2,1:cols+1]
            currentB        = B[1:rows+1, 1:cols+1]
            B               = np.pad(timeStepUpdate(currentB, leftB, rightB, topB, bottomB), 1, 'constant')

            #Processing green pixels
            leftG, rightG   = G[1:rows+1,0:cols], G[1:rows+1,2:cols+2]
            topG, bottomG   = G[0:rows,1:cols+1], G[2:rows+2,1:cols+1]
            currentG        = G[1:rows+1, 1:cols+1]
            G               = np.pad(timeStepUpdate(currentG, leftG, rightG, topG, bottomG), 1, 'constant')

            #Extract unpadded 
            R, G, B = extract(R,rows,cols)  ,  extract(G,rows,cols),   extract(B,rows,cols)

            #Swap back rows and columns to display correctly
            rows, cols = cols, rows
            R, G, B = R.reshape((1,rows*cols))[0], G.reshape((1,rows*cols))[0], B.reshape((1,rows*cols))[0]
            result = np.vstack(( R, G, B ))
            result = result.T
            result = result.reshape(rows,cols,3)
            rows, cols = cols, rows

            #Display image
            plt.imshow(result)
            image_vals.append(result)
            ax.set_title('Blurring {} using heat equation'.format(fileNames[index]),fontsize=18)
            ax.set_xlabel("Time steps: {}".format(t))
            print("Processing step: {}".format(t))

            #Stitching
            writer.grab_frame()
            plt.cla()

            #Reconvert to arrays for next iterations
            R, G, B = np.ndarray.tolist(R), np.ndarray.tolist(G), np.ndarray.tolist(B)
            


            



    


if __name__=="__main__":
    main()