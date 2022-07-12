#!/usr/bin/env python3
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import animation as anim
import numpy as np
import sys
import random
import math

length = int(sys.argv[1])
temp = float(sys.argv[2])

fig = plt.figure()
ax = plt.axes(xlim=(0, length-1), ylim=(0, length-1))
arr = np.zeros((length, length), dtype=int)

cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                                    ['Red', 'Blue', 'Green'])

bounds = [0, 0, 10, 10]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

im = plt.imshow(arr, interpolation='nearest',
                cmap=cmap, vmin=0, vmax=255,
                origin='lower', animated=True)

def hamiltonian(arr, x, y, c):
    return ((1 if (y < length-1 and arr[x][y+1] != c) else 0) 
        + (1 if (y > 0 and arr[x][y-1] != c) else 0)
        + (1 if (x < length-1 and arr[x+1][y] != c) else 0)
        + (1 if (x > 0 and arr[x-1][y] != c) else 0))

def recolour(arr, x, y):
    nRed = hamiltonian(arr, x, y, 0)
    nBlue = hamiltonian(arr, x, y, 150)
    nGreen = hamiltonian(arr, x, y, 300)
    pf = math.exp(-temp*nRed)+math.exp(-temp*nBlue)+math.exp(-temp*nGreen)
    a = math.exp(-temp*nRed)/pf
    b = math.exp(-temp*nBlue)/pf
    rand = np.random.random_sample()
    if rand < a:
        arr[x][y] = 0
    elif rand < a+b:
        arr[x][y] = 150
    else:
        arr[x][y] = 300 
    return arr

def simulate(i):
    arr = im.get_array()
    x0 = int(np.random.random_sample()*length)
    y0 = int(np.random.random_sample()*length)
    arr = recolour(arr, x0, y0)
    im.set_array(arr)
    return [im] 

anim = anim.FuncAnimation(fig, simulate, frames=200, interval=20, blit=True)
plt.show()
