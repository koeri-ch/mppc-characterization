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
    for line in lines:
        split1 = line.split(", ")
        if len(split1) > 1:
            for i in range(1,len(split1)):
                if split1[i]:
                    value_str = split1[i].replace("\n","")
                    if value_str:
                        
                        # All pulses go to a same array and sum.
                        peaks_all.append( float(value_str) )
                        sumAll += float(value_str)
                        
                        # Now we split them by their order on the waveform
                        peaks[i-1].append( float(value_str))
                        sumPeaks[i-1] += float(value_str)

    # The figure and axes
    fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=4, sharey=False, figsize=(15,3)) 
    axes = (ax0, ax1, ax2, ax3)
    
    # Use suggested binwidth
    binwidth  = 2*0.08087327954437595
    numbins_all = np.arange(min(peaks_all),max(peaks_all)+binwidth,binwidth)
    numbins0 = np.arange(min(peaks[0]),max(peaks[0])+binwidth,binwidth)
    numbins1 = np.arange(min(peaks[1]),max(peaks[1])+binwidth,binwidth)
    numbins2 = np.arange(min(peaks[2]),max(peaks[2])+binwidth,binwidth)

    # Colors
    colors2 = ['grey','black','navy']
    
    # Plot the histograms
    bins, pos, _ = ax0.hist(peaks_all, bins=numbins_all, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="All pulses")
    ax1.hist(peaks[0],  bins=numbins0, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="First pulse")
    ax2.hist(peaks[1],  bins=numbins1, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="Second pulse")
    ax3.hist(peaks[2],  bins=numbins2, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="Third pulse")

    # Bin widths
    deltapos = pos[1]-pos[0]
    
    # Set y label
    ax0.set_ylabel("No. of events/{0:4.1f} mV".format(deltapos))

    # Add x label and legend to all plots
    for axi in axes:
        axi.set_xlabel("Amplitude (mV)")
        axi.legend()

    ## Printing some stats:
    print("\nSummed up amplitudes:")
    print("   All pulses (mV)    : {0}".format(sumAll) )
    print("   First pulses (mV)  : {0}".format(sumPeaks[0]) )
    print("   Second pulses (mV) : {0}".format(sumPeaks[1]) )
    print("   Third pulses (mV)  : {0}".format(sumPeaks[2]) )        

    ## Percentages:
    print("\nStats:")
    print("   Pulses found       : {0}".format(len(peaks_all)) )
    print("   First pulses       : {0:.2%}".format(len(peaks[0])/float(len(peaks_all)) ) ) 
    print("   Second pulses      : {0:.2%}".format(len(peaks[1])/float(len(peaks_all)) ) )
    print("   Third pulses       : {0:.2%}".format(len(peaks[2])/float(len(peaks_all)) ) )
    
    # Other pulses
    sumRemainingPeaks = 0
    for i in range(3,100):
        if len(peaks[i]) != 0:
            sumRemainingPeaks += len(peaks[i])
    print("   Other pulses       : {0:.2%}".format(sumRemainingPeaks/float(len(peaks_all)) ) )

    ## Tight layout
    plt.tight_layout()
    
    ## Show only
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