import pygame
from pygame.locals import *

import pyopencl as cl
import pyopencl.array as pycl_array

import numpy as np
import threading

# Initialize Pygame
pygame.init()

# Set up the screen
w,h = 800, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Wave Equation Visualizer")

# Create an OpenCL context and command queue
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)

#x string base [0,1]
x_start, x_end, numpts = 0,1,10000

host_data = np.linspace(x_start,x_end,numpts).astype(np.float32)
ys = np.linspace(0,1,numpts).astype(np.float32)

#kernel data buffers
x_buffer = cl.Buffer(context,  cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=host_data)
y_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, ys.nbytes)

# Read the OpenCL kernel code from an external file
with open('compute_kernel.cl', 'r') as kernel_file:
    kernel_code = kernel_file.read()


# Compile the OpenCL kernel
program = cl.Program(context, kernel_code).build()

#pygame objs
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 12)


lock = threading.Lock()

def compute_and_render():
    with lock:
        draw_frame()

def draw_points_soln(a, clr, scale):
    
    xoffset = (np.sqrt(x_start**2 + x_end**2)/2)
    if a==0:
        for n in range(len(host_data)):
            point = ((host_data[n] - xoffset) * scale + w/2  - scale/2  , ys[n] *scale  + h/2 - scale/2 )
            pygame.draw.circle(screen, clr, point, 1)
    else:
        for n in range(0,len(host_data), a):
            point = ((host_data[n] - xoffset) * scale + w/2 - scale/2 , ys[n] *scale  + h/2 - scale/2 )
            pygame.draw.circle(screen, clr, point, 1)

def draw_lines_soln(a,clr,scale):
    
    xoffset = (np.sqrt(x_start**2 + x_end**2)/2)
    if a==0:
        for n in range(len(host_data)-1):
            point_a = ((host_data[n] - xoffset) * scale + w/2 - scale/2 , ys[n] *scale  + h/2 - scale/2 )
            point_b = ((host_data[n+a] - xoffset) * scale + w/2 - scale/2 , ys[n+1]*scale  + h/2 - scale/2)
            pygame.draw.line(screen, clr, point_a, point_b,1)
    else:
        for n in range(0,len(host_data)-a, a):
            point_a = ((host_data[n] - xoffset) * scale + w/2 - scale/2 , ys[n] *scale  + h/2 - scale/2 )
            point_b = ((host_data[n+a] - xoffset) * scale + w/2 - scale/2 , ys[n+a] *scale  + h/2 - scale/2 )
            pygame.draw.line(screen, clr, point_a, point_b,2)


        
def draw_frame():
    #pygame objs    
    current_time_sec = np.float32(pygame.time.get_ticks() / 5000.0)
    
    text = font.render(f"Time (s): {current_time_sec}", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    
    # Execute the OpenCL kernel  
    program.sum(queue, host_data.shape, None, x_buffer, y_buffer, current_time_sec)
    #queue.finish()

    #read results from gpu
    cl.enqueue_copy(queue, ys, y_buffer).wait()
    

    # Draw graphics or display computed data here
    screen.fill( (0 , 0, 0) )       # Clear the screen  
    screen.blit(text, text_rect)    #draw current time    
    
    draw_points_soln(0, (255,255,255), 200)
    #draw_lines_soln(50, (255,255,255), 200)

    
    # Update the display
    pygame.display.flip()

    #end_draw_frame




# Main draw loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    compute_and_render()

    
    #clock.tick(60) #framerate target

pygame.quit()
