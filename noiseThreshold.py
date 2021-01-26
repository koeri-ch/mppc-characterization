import os 
import sys
import numpy as np 
import math
import matplotlib.pyplot as plt 
from scipy import signal
from lmfit import Model

# A function to open the files
def openFiles(filename):
    # Open one or two column files.
    with open(filename,'r') as input_file:
        x,y = np.loadtxt(filename,delimiter=' ',usecols=(0,1), unpack=True)
    return x,y

# Function to fit data
def f_gauss(x,Namp,mean,sigma):
    return Namp*np.exp(-0.5/(sigma**2)*(x-mean)**2 )

# Function to show progress
def printProgressAcquisition(i,N):
    sys.stdout.write("Analysing waveform #{0}/{1}. Progress: {2:3.1f}%.\r".format(int(i),int(N),i/float(N)*100 ) )
    sys.stdout.flush()
    if (i == N):
        print()   