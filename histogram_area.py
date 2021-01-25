from scipy import integrate
from scipy import interpolate
from scipy import signal
import matplotlib.pyplot as plt
import glob, os, sys, subprocess
import numpy as np
import time

def mainFunction(path_to_file):
## Opens the peak files and plots a histogram
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
                sumAll += float(value_str)

    ## Suggested bin width
    # binwidth=2*0.08
    # numbins0 = np.arange(min(peaks_all),max(peaks_all)+binwidth,binwidth)
    
    ## Otherwise use the automatic binwidth finder
    numbins0 = 'fd'

    # Create figure and axis
    fig, ax0 = plt.subplots(nrows=1, ncols=1, sharey=False, figsize=(5,5)) 
    
    values, bins, patches = ax0.hist(peaks_all,  bins=numbins0, histtype='stepfilled', edgecolor='black',  facecolor='red', label="Pulse area, Run #{0:02d}".format(run_numbers[i]) )
    
    widths = np.diff(bins)

    # widths = np.diff(bins)
    # area_total = sum(widths*values)
    # sumErrorArea = 0.0
    # for i in range(0,len(widths)):
    #     error_height = np.sqrt(values[i])
    #     error_width  = 0.03*np.sqrt(widths[i])
        
    #     area = widths[i]*values[i]
    #     error_area = area*np.sqrt( (error_height/values[i])**2 + (error_width/widths[i])**2 )
        
    #     sumErrorArea += error_area**2
    
    # area_total_error = np.sqrt(sumErrorArea)
    
    # print(area_total, area_total_error)
    # print("Total histogram area. Run #{0:02d}: {1:5.0f} +/- {2:3.0f} mV".format(run_number, area_total, area_total_error))

    ax0.set_ylabel("No. of events/{0:4.1f}".format(widths[0])+" mV"+r"$\cdot$"+"ns")
    ax0.set_xlabel("Pulse area (mV"+r"$\cdot$"+"ns)")
    ax0.legend()

    # Print stats
    print("Run #{0:02d}. Total area: {1:e} mV.s".format(run_numbers[i],sumAll*1.e-9))

    # Change layout
    plt.tight_layout()

    # Show histogram
    plt.show()

    ## You can save it as well
    # name_image = "./areas-histogram.png"
    # plt.savefig(name_image, dpi = 300)
    # plt.close()

### Pre-routine check
if 

else:
    print("Usage: ")