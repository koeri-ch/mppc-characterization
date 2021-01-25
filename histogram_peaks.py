from scipy import integrate
from scipy import interpolate
from scipy import signal
import matplotlib.pyplot as plt
import glob, os, sys, subprocess
import numpy as np
import time



def main():
## Call all functions
# 
# 
    peHeight=9.8
    voltage=55.73
    run_number=1

    #open data
    file_in = open("/home/koerich/Data/Small_Plate/Run01/peaks-01.dat")
    lines = file_in.readlines()

    # Matrix to store the peaks:
    peaks = [ [] for i in range(0,100) ]
    # print(peaks)
    peaks_all = []
    peaks_pe = []
    lenValues = []
    sumAll = 0.0
    sumPeaks = [0.0]*100

    for line in lines:
        split1 = line.split(", ")
        if len(split1) > 1:
            for i in range(1,len(split1)):
                # print(split1)
                if split1[i]:
                    value_str = split1[i].replace("\n","")
                    if value_str:
                        peaks_all.append( float(value_str)/peHeight/1.0 )
                        sumAll += float(value_str)/peHeight/1.0
                        
                        peaks[i-1].append( float(value_str)/peHeight/1.0 )
                        sumPeaks[i-1] += float(value_str)/peHeight/1.0

    fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=4, sharey=False, figsize=(15,3)) 
    axes = (ax0, ax1, ax2, ax3)
    
    print("Run #{0:2d}. Total sum: {1} p.e.".format(run_number,sumAll))
    print("    First peaks: {0} p.e.".format(sumPeaks[0]))


    # numbins = 'fd'
    # numbins = 150
    binwidth  = 2*0.08087327954437595
    # binwidth2 =  
    numbins_all = np.arange(min(peaks_all),max(peaks_all)+binwidth,binwidth)
    numbins0 = np.arange(min(peaks[0]),max(peaks[0])+binwidth,binwidth)
    numbins1 = np.arange(min(peaks[1]),max(peaks[1])+binwidth,binwidth)
    # numbins1 = 'fd'
    numbins2 = np.arange(min(peaks[2]),max(peaks[2])+binwidth,binwidth)

    colors2 = ['grey','black','navy']
    ax0.hist(peaks_all, bins=numbins_all, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="All peaks")
    ax1.hist(peaks[0],  bins=numbins0, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="First peak in pulse")
    bins, pos, _ = ax2.hist(peaks[1],  bins=numbins1, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="Second peak in pulse")
    ax3.hist(peaks[2],  bins=numbins2, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="Third peak in pulse")

    deltapos = pos[1]-pos[0]
    ax0.set_ylabel("No. of events/{0:4.1f} mV".format(deltapos))

    for axi in axes:
        # axi.set_xlim([0.0,50])
        axi.set_xlabel("Amplitude (p.e.)")
        axi.legend()
    # ax0.set_xlim([0.0,70])

    # print(deltapos)
    # Save plot
    name_image = "./height-several-{0}V-Run{1:02d}.png".format(voltage,run_number)
    plt.tight_layout()
    plt.savefig(name_image, dpi = 600)

    plt.close()

    binwidth=2*0.08087327954437595
    numbins0 = np.arange(min(peaks[0]),max(peaks[0])+binwidth,binwidth)
    fig, ax5 = plt.subplots(nrows=1, ncols=1, sharey=False, figsize=(5,5)) 
    values, bins, patches = ax5.hist(peaks[0],  bins=numbins0, histtype='stepfilled', edgecolor=colors2[1], facecolor=colors2[0], label="First peak in pulse")
    
    widths = np.diff(bins)
    area_total = sum(widths*values)
    sumErrorArea = 0.0
    for i in range(0,len(widths)):
        error_height = np.sqrt(values[i])
        error_width  = 0.03*np.sqrt(widths[i])
        
        area = widths[i]*values[i]
        error_area = area*np.sqrt( (error_height/values[i])**2 + (error_width/widths[i])**2 )
        
        sumErrorArea += error_area**2
    
    area_total_error = np.sqrt(sumErrorArea)
    
    print(area_total, area_total_error)
    print("Total histogram area. Run #{0:02d}: {1:5.0f} +/- {2:3.0f} mV".format(run_number, area_total, area_total_error))
    deltapos = pos[1]-pos[0]
    ax5.set_ylabel("No. of events/{0:4.1f} mV".format(deltapos))
    ax5.set_xlabel("Amplitude (p.e.)")
    plt.tight_layout()
    name_image = "./height-first_peaks-{0}V-Run{1:02d}.png".format(voltage,run_number)
    plt.savefig(name_image, dpi = 300)
    plt.close()



## Run main fuction
if __name__ == "__main__":
    main()
