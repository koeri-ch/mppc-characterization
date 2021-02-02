from scipy import integrate
from scipy import interpolate
from scipy import signal
import matplotlib.pyplot as plt
import glob, os, sys, subprocess
import numpy as np
import time

def histogramError(values,widths):
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

    return np.sqrt(sumErrorArea)

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
    eventCounter = 0
    for line in lines:
        if eventCounter < 400000:
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

            eventCounter += 1

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
    bins1, pos1, _ = ax1.hist(peaks[0],  bins=numbins0, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="First pulse")
    bins2, pos2, _ = ax2.hist(peaks[1],  bins=numbins1, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="Second pulse")
    bins3, pos3, _ = ax3.hist(peaks[2],  bins=numbins2, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="Third pulse")

    # Bin widths
    deltapos = pos[1]-pos[0]
    
    # Set y label
    ax0.set_ylabel("No. of events/{0:4.1f} mV".format(deltapos))

    # Add x label and legend to all plots
    for axi in axes:
        axi.set_xlabel("Amplitude (mV)")
        axi.legend()

    ## Printing some stats:
    deltay = 0.32 # mV
    totalpulses=len(peaks_all)
    firstpulses=len(peaks[0])
    secondpulses=len(peaks[1])
    thirdpulses=len(peaks[2])
    
    ## Summed-up amplitudes
    print("\nSummed up amplitudes:")
    print("   All pulses (mV)    : {0} +/- {1}".format(sumAll,      np.sqrt(totalpulses)*deltay ) )
    print("   First pulses (mV)  : {0} +/- {1}".format(sumPeaks[0], np.sqrt(firstpulses)*deltay ) )
    print("   Second pulses (mV) : {0} +/- {1}".format(sumPeaks[1], np.sqrt(secondpulses)*deltay ) )
    print("   Third pulses (mV)  : {0} +/- {1}".format(sumPeaks[2], np.sqrt(thirdpulses)*deltay ) )

    ## Averaged amplitudes:
    print("\nAveraged amplitudes:")
    print("   All pulses        : {0} +/- {1}".format(sumAll/float(totalpulses),       deltay/np.sqrt(totalpulses) ) )
    print("   First pulses      : {0} +/- {1}".format(sumPeaks[0]/float(firstpulses),  deltay/np.sqrt(firstpulses) ) )
    print("   Second pulses     : {0} +/- {1}".format(sumPeaks[1]/float(secondpulses), deltay/np.sqrt(secondpulses) ) )
    print("   Third pulses      : {0} +/- {1}".format(sumPeaks[2]/float(thirdpulses),  deltay/np.sqrt(thirdpulses) ) )

    ## Number of pulses
    print("\nNumber of pulses:")
    print("   Pulses found      : {0} +/- {1}".format(totalpulses,int(np.sqrt(totalpulses))) )
    print("   First found       : {0} +/- {1}".format(firstpulses,int(np.sqrt(firstpulses))) )
    print("   Second found      : {0} +/- {1}".format(secondpulses,int(np.sqrt(secondpulses))) )
    print("   Third found       : {0} +/- {1}".format(thirdpulses,int(np.sqrt(thirdpulses))) )

    ## Histogram area
    print("\nHistogram area:")
    area_all          = sum(bins*np.diff(pos))
    area_all_error    = histogramError(bins,np.diff(pos))
    area_first        = sum(bins1*np.diff(pos1))
    area_first_error  = histogramError(bins1,np.diff(pos1))
    area_second       = sum(bins2*np.diff(pos2))
    area_second_error = histogramError(bins2,np.diff(pos2))
    area_third        = sum(bins3*np.diff(pos3))
    area_third_error  = histogramError(bins3,np.diff(pos3))
    print("   Total pulses      : {0} +/- {1}".format(area_all,    area_all_error) )
    print("   First pulses      : {0} +/- {1}".format(area_first,  area_first_error ) )
    print("   Second pulses     : {0} +/- {1}".format(area_second, area_second_error ) )
    print("   Third pulses      : {0} +/- {1}".format(area_third,  area_third_error ) )

    ## Percentages:
    print("\nPercentage:")
    firstpercentage = firstpulses/totalpulses
    secondpercentage = secondpulses/totalpulses
    thirdpercentage = thirdpulses/totalpulses
    firstpercentage_error = firstpercentage*np.sqrt( (np.sqrt(firstpulses)/firstpulses)**2 + (np.sqrt(totalpulses)/np.sqrt(totalpulses)**2 ))
    secondpercentage_error = secondpercentage*np.sqrt( (np.sqrt(secondpulses)/secondpulses)**2 + (np.sqrt(totalpulses)/np.sqrt(totalpulses)**2 ))
    thirdpercentage_error = thirdpercentage*np.sqrt( (np.sqrt(thirdpulses)/thirdpulses)**2 + (np.sqrt(totalpulses)/np.sqrt(totalpulses)**2 ))
    
    print("   First pulses      : {0:.2%} +/- {1:.0%}".format(firstpercentage, firstpercentage_error))  
    print("   Second pulses     : {0:.2%} +/- {1:.0%}".format(secondpercentage, secondpercentage_error))
    print("   Third pulses      : {0:.2%} +/- {1:.0%}".format(thirdpercentage, thirdpercentage_error))
    
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