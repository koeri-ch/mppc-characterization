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
    # totalpulses, totalpulses_errors   = np.loadtxt(path_to_file, usecols=(0,1), delimiter=", ", unpack=True)
    # firstpulses, firstpulses_errors   = np.loadtxt(path_to_file, usecols=(2,3), delimiter=", ", unpack=True)
    # secondpulses, secondpulses_errors = np.loadtxt(path_to_file, usecols=(4,5), delimiter=", ", unpack=True)
    # thirdpulses, thirdpulses_errors   = np.loadtxt(path_to_file, usecols=(6,7), delimiter=", ", unpack=True)

    totalpulses  = np.loadtxt(path_to_file, usecols=(0), delimiter=", ", unpack=True)
    firstpulses  = np.loadtxt(path_to_file, usecols=(1), delimiter=", ", unpack=True)
    secondpulses = np.loadtxt(path_to_file, usecols=(2), delimiter=", ", unpack=True)
    thirdpulses  = np.loadtxt(path_to_file, usecols=(3), delimiter=", ", unpack=True)


    ## starting two plots
    fig, (ax0,ax1,ax2,ax3) = plt.subplots(nrows=1, ncols=4, sharey=False, figsize=(20,5)) 
    axes = (ax0,ax1,ax2,ax3)

    x_placeholder = np.arange(1,4,1)
    # ax0.errorbar(x=x_s   fmt='none', ecolor='black', barsabove=True, capsize=2.0)
    ax0.plot(x_placeholder, totalpulses, 'o', color='green', label='Total pulses')


    # ax1.errorbar(x=x_placeholder, y=firstpulses, yerr=firstpulses_errors, 
    #                     fmt='none', ecolor='black', barsabove=True, capsize=2.0)
    ax1.plot(x_placeholder, firstpulses, 'o', color='blue', label='First pulses')

    # ax2.errorbar(x=x_placeholder, y=secondpulses, yerr=secondpulses_errors, 
    #                     fmt='none', ecolor='black', barsabove=True, capsize=2.0)
    ax2.plot(x_placeholder, secondpulses, 'o', color='orange', mec='black', label='Second pulses')

    # ax3.errorbar(x=x_placeholder, y=thirdpulses, yerr=thirdpulses_errors, 
    #                     fmt='none', ecolor='black', barsabove=True, capsize=2.0)
    ax3.plot(x_placeholder, thirdpulses, 'o', color='red', mec='black',  label='Third pulses')


    for axi in axes:
        axi.set_xlim([0.5,3.5])
        axi.set_xticks(x_placeholder)
        axi.set_xticklabels(['Open', 'Reflective', 'Black'])
        axi.set_ylabel("Summed up amplitudes (mV)")
        axi.legend()
    # ax1.set_ylim([93000,107000])

    plt.tight_layout()
    # plt.show()

    

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