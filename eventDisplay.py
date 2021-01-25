import scipy 
import numpy as np 
import pyvisa
import sys
import matplotlib.pyplot as plt

def readit(waveform_directory):
## Reads the waveform file
    return np.loadtxt("{0}".format(waveform_directory), usecols=(0,1), delimiter=", ", unpack=True)

def mainFunction(path_to_preamble, path_to_event):
    ## Opens file, corrects units 
    ## and plots the waveform.

    # Open correct units string
    preamble_file = open(path_to_preamble,'r')
    preamble_raw  = preamble_file.readlines()
    details       = preamble_raw[0].split(';')
    preamble_file.close()

    # Open details:
    XINcr  = float(details[8])
    PT_Off = float(details[9])
    XZERo =  float(details[10])
    XUNit =  details[11]
    YMUlt =  float(details[12])
    YZEro =  float(details[13])
    YOFF  =  float(details[14])
    YUNIT =  details[15]
    WFID  =  details[6]
    WFID_details = WFID.split(', ')
    VperDIV = float(WFID_details[2].replace('V/div',''))
    SperDIV = float(WFID_details[3].replace('s/div',''))
    offset_accuracy = 0.002*abs(   YZEro+YMUlt*(YZEro - YOFF -YOFF)    )+1.5/1000.0+0.1*VperDIV
    XOffSet  = 1

    # Read data from file
    x, y = readit(path_to_event)

    # Transform units
    x_s = XZERo+XINcr*(XOffSet+np.asarray(x)-PT_Off)
    y_V = YZEro+YMUlt*(np.asarray(y)-YOFF)
    x_ns = 1.e9*x_s - x_s[0]*1.e9
    y_mV = 1.0*1.e3*y_V

    # Plot
    plt.plot(x_ns,y_mV)
    plt.xlim([x_ns[0], x_ns[-1]])
    plt.xlabel("Time (ns)")
    plt.ylabel("Amplitude (mV)")
    plt.show()

## Initial routine
if len(sys.argv) == 3:
    mainFunction(sys.argv[1], sys.argv[2])
else:
    print("Usage: python eventDisplay.py path_to_preamble path_to_event")

