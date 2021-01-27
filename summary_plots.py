from scipy import integrate
from scipy import interpolate
from scipy import signal
import matplotlib.pyplot as plt
import glob, os, sys, subprocess
import numpy as np
import time

def mainFunction(path_to_file):
## Opens the peak files and plots a histogram
## The file with the are is expected to have many columns,
## one with the waveform's name 
## and another the waveform's area

    # Open file with peak information
    file_in = open(path_to_file)
    lines = file_in.readlines()

    # Matrix to store the peaks:
    peaks = [ [] for i in range(0,100) ]
    
    # Array to store all the peaks
    peaks_all = []

    # Sum up of all pulse amplitudes
    sumAll = 0.0
    sumPeaks = [0.0]*100

    # Read through lines 
    # and retrieve peaks
    totalpulses, totalpulses_errors   = np.loadtxt(path_to_file, usecols(0,1), delimiter ", ")
    firstpulses, firstpulses_errors   = np.loadtxt(path_to_file, usecols(2,3), delimiter ", ")
    secondpulses, secondpulses_errors = np.loadtxt(path_to_file, usecols(4,5), delimiter ", ")
    thirdpulses, thirdpulses_errors   = np.loadtxt(path_to_file, usecols(6,7), delimiter ", ")

    

    ## Use original file name to create an image file
    splitname1 = path_to_file.split("/")
    file_name  = splitname1[-1].replace(".dat",".png")
    plt.savefig("./{0}".format(file_name), dpi = 600)

    ## END OF MAIN FUNCTION

### Pre-mainFunction check
if len(sys.argv) == 2:
    # Send file location to main function
    mainFunction(sys.argv[1])
else:
    print("Usage: python path_to_peaks_file")