from scipy import integrate
from scipy import interpolate
from scipy import signal
import matplotlib.pyplot as plt
import glob, os, sys, subprocess
import numpy as np
import time

def mainFunction(path_to_file):
## Opens the areas files and plots a histogram
## The file with the are is expected to have two columns,
## one with the waveform's name 
## and another the waveform's area

    # Open file with area information
    file_in = open(path_to_file, "r")
    lines = file_in.readlines()

    # array to store the areas
    areas = []

    # Absolute area
    areaAll = 0.0
    
    # Run through lines in the file
    for line in lines:
        split1 = line.split(", ")
        if len(split1) > 1:
            value_str = split1[1].replace("\n","")
            if value_str:

                # Append the area value to the array
                areas.append( float(value_str) )

                # Sums the waveform's area to all others
                areaAll += float(value_str)

    ## Suggested bin width
    # binwidth=2*0.08
    # numbins0 = np.arange(min(peaks_all),max(peaks_all)+binwidth,binwidth)
    
    ## Or use the automatic binwidth finder
    numbins0 = 'fd'

    # Create figure and axis
    fig, ax0 = plt.subplots(nrows=1, ncols=1, sharey=False, figsize=(5,5)) 
    
    # Plot the histogram
    values, bins, patches = ax0.hist(areas,  bins=numbins0, histtype='stepfilled', edgecolor='black',  facecolor='white', label="Pulse area" )
    
    # Find bin widths (should be equal)
    widths = np.diff(bins)

    # Find area of histogram
    areaHisto = sum(widths*values)
    sumErrorArea = 0.0
    for i in range(0,len(widths)):

        if ((widths[i] != 0.0) and (values[i] != 0)) :
            
            # Bin error as squareroot of counts
            error_height = np.sqrt(values[i])

            # Width error as 3% of width
            error_width  = 0.03*np.sqrt(widths[i])
            
            # Area of bin
            area = widths[i]*values[i]
            
            # Error in bin
            error_area = area*np.sqrt( (error_height/values[i])**2 + (error_width/widths[i])**2 )
            
            # Error in quadrature
            sumErrorArea += error_area**2
    
    # Total error is square-root of total squared errors
    areaHisto_error = np.sqrt(sumErrorArea)
    
    # Adding labels to histogram
    ax0.set_ylabel("No. of events/{0:4.1f}".format(widths[0])+" mV"+r"$\cdot$"+"ns")
    ax0.set_xlabel("Pulse area (mV"+r"$\cdot$"+"ns)")
    ax0.set_xlim([0.0,12000.])
    ax0.legend()

    # Print stats
    print(len(areas))
    print("All units in mV.ns")
    print("Summed waveform areas     : {0:e}".format(areaAll))
    print("Average area per waveform : {0:e}".format(areaAll/len(areas)))
    print("Histogram area            : {0:e}".format(areaHisto))
    print("Histogram area error      : {0:e}".format(areaHisto_error))

    # Change layout
    plt.tight_layout()

    # Show histogram
    # plt.show()

    ## You can save it as well
    splitname1 = path_to_file.split("/")
    file_name  = splitname1[-1].replace(".dat",".png")
    plt.savefig(file_name, dpi = 300)
    plt.close()

### Pre-routine check
if len(sys.argv) == 2:
    # Send file location to main function
    mainFunction(sys.argv[1])
else:
    print("Usage: python path_to_area_file")