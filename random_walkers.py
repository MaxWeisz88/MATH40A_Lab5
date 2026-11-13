#!/usr/bin/python
from random import random
import numpy as np
import matplotlib.pyplot as plt

# Time steps
tmax = 200

# Max spatial steps
nmax = 2*tmax

# Number of walkers and initial positions
nwalkers = 2
x = [0]*nwalkers

# Bin random walk positions into an empty 2D array (time, bin)
bins = np.zeros((tmax,nmax+1)) # tmax rows x nmax+1 columns
bins[0,int(nmax/2)] = nwalkers  # all walkers initially at x=0

# Intialize statistics
meanx = [0.0]*tmax
widthx = [0.0]*tmax

# Time iteration
for i in range(1,tmax):
    
    # Walker iteration
    for j in range(nwalkers):
        
        if random()>0.5:
            x[j] += 1
        else:
            x[j] -= 1
        
        # Increment count for location of x[j]
        bins[i,x[j]+int(nmax/2)] += 1 # recenter bins around x=0
            
    # Statistics
    meanx[i] = sum(x)/float(len(x))
    widthx[i] = np.std(x)


def get_diffusion_constant(tmax):
    t = np.arange(1, tmax)
    D = np.array(widthx[1:])**2 / (2*t)
    return np.mean(D)

print(get_diffusion_constant(tmax=tmax))

# Sample plots
# Added lim parameter to specify the limits of plot in the function call
def walker_hist(i, lim=10):
    plt.figure(i)
    bw = float(np.shape(bins)[1]-1)/float(np.shape(bins)[1])
    binx = -0.5*(np.shape(bins)[1]-1)+bw*(0.5+np.arange(np.shape(bins)[1]))
    biny = bins[i,:]
    plt.bar(binx,biny,width=bw) #width here is just a plot style option
    plt.xlim((-lim, lim)) 
    
walker_hist(0, 5),walker_hist(1, 5),walker_hist(10,30),walker_hist(100, 40)#,walker_hist(200,80),walker_hist(500, 100)
plt.show()

plt.figure()
plt.loglog(widthx)
plt.xlabel("Time step (t)")
plt.ylabel("Width sigma(t) (std of walker positions)")
plt.title("Width of the walker distribution over time")
plt.show()

t = np.arange(tmax)
plt.figure()
plt.plot(t, widthx, label='simulation')
plt.plot(t, np.sqrt(t), '--', label='sqrt(t)')
plt.xlabel('time step t')
plt.ylabel('width σ(t)')
plt.legend()
plt.show()

def plot_walker_avg(meanx):
    plt.figure()
    plt.plot(meanx)
    plt.xlabel("Time step (t)")
    plt.ylabel("Mean position of the walkers")
    plt.title(f"Average position of {nwalkers} random walkers over time")
    plt.show()

plot_walker_avg(meanx)
