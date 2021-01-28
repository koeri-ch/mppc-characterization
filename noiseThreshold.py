import os, sys
import numpy as np 
import math
import matplotlib.pyplot as plt 
from scipy import signal
from lmfit import Model

def openFiles(filename):
    # Open one or two column files.
    with open(filename,'r') as input_file:
        x,y = np.loadtxt(filename,delimiter=', ',usecols=(0,1), unpack=True)
    return x,y

def f_gauss(x,Namp,mean,sigma):
    # Function to fit data to.
    return Namp*np.exp(-0.5/(sigma**2)*(x-mean)**2 )

def printProgressAcquisition(i,N):
    # Function to show progress
    sys.stdout.write("Analysing waveform #{0}/{1}. Progress: {2:3.1f}%.\r".format(int(i),int(N),i/float(N)*100 ) )
    sys.stdout.flush()
    if (i == N):
        print()   

def mainFunction(path_to_preamble, path_to_waveforms):
    ## Opens file, corrects units 
    ## and finds noise threshold and noise baseline.

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

    # Arrays to store information
    sigmas, means, Ns, wrong_sigma = [],[],[],[]
    sigmaErrors, meansErrors, Nerrors = [], [], []
    j = 0

    # Opening all files in the directory.
    # This will load all pulse information in 
    # matrices x and y. 
    for root, dirs, files in os.walk(path_to_waveforms, topdown=False):
        N = len(files)
        for name in files:
            file_dir  = os.path.join(root,name)
            file_name = file_dir.split('/')[-1]
            
            if ".dat" in file_name:
                if file_name != "waveform-preamble.dat":
                    
                    if j < 10:

                        x, y = openFiles(file_dir)
                        x_s = XZERo+XINcr*(XOffSet+x-PT_Off)
                        y_V = YZEro+YMUlt*(y-YOFF)

                        # Transform units
                        x_ns = x_s*1.0e9
                        y_mV = y_V*1.0e3

                        # Find the peaks
                        x_max, _ = signal.find_peaks(y_mV)
                        x_min, _ = signal.find_peaks(-1.0*y_mV)

                        # Joining the peaks in a single array
                        extrema = []
                        for element in x_max:
                            extrema.append(y_mV[element])
                        for element in x_min:
                            extrema.append(y_mV[element])
                        
                        # Binning data
                        binned_data, bins, _ = plt.hist(extrema)
                        delta_bin = bins[1]-bins[0]

                        # Turning bin positions into something useful to be fitted
                        bin_middle = [0.0]*len(binned_data)
                        for i in range(0,len(bins)-1):
                            bin_middle[i] = bins[0] + delta_bin*(i + 0.5)

                        # ax1.plot(bin_middle, binned_data, 'o', 'orange')

                        # Fitting the data
                        # f_gauss(x,N,mean,sigma):
                        gmodel = Model(f_gauss)
                        result = gmodel.fit(binned_data, x=bin_middle, Namp=5, mean=5, sigma=1)

                        # Extracting the parameters
                        parameters = result.params
                        Namp = parameters['Namp'].value
                        mean = parameters['mean'].value
                        sigma = parameters['sigma'].value

                        if sigma < 10.0:

                            # Values
                            sigmas.append(sigma)
                            means.append(mean)
                            Ns.append(Namp)

                            # Errors
                            sigmaErrors.append(parameters['Namp'].stderr)
                            meansErrors.append(parameters['mean'].stderr)
                            Nerrors.append(parameters['Namp'].stderr)


                        if sigma > 10.0:
                            wrong_sigma.append([sigma, file_name])

                    j += 1
                    # print(j)
                    printProgressAcquisition(j,N)

    print("Measuring the averages and errors...\n")
    sigmaSum = 0.0 
    sigmaErrorSum = 0.0
    NSum = 0.0
    NerrorSum = 0.0
    MeanSum = 0.0
    MeanErrorSum = 0.0
    validCounter = 0

    for i in range(0,len(sigmas)):
        
        if sigmaErrors[i] != None:

            validCounter +=1

            sigmaSum += sigmas[i]
            sigmaErrorSum += sigmaErrors[i]**2

            NSum += Ns[i]
            NerrorSum += Nerrors[i]**2
            
            MeanSum += means[i]
            MeanErrorSum += meansErrors[i]**2

    sigmaAvg = sigmaSum/float(validCounter)
    Navg = NSum/float(validCounter)
    MeanAvg = MeanSum/float(validCounter)

    NampError = np.sqrt(NerrorSum)/validCounter
    meanError = np.sqrt(MeanErrorSum)/validCounter
    sigmaError = np.sqrt(sigmaErrorSum)/validCounter 

    print("here")
    fileAverages = open("./fitting_results.dat", "w")
    fileAverages.write("sigma: {0} ({1}).\n".format(sigmaAvg, sigmaError))
    fileAverages.write("mean:  {0} ({1}).\n".format(MeanAvg, meanError))
    fileAverages.write("amp:   {0} ({1}).\n\n".format(Navg, NampError))
    fileAverages.write("noise threshold: {0}".format(6.*sigmaAvg))

    fileFailed = open("./fitting_fails.dat", "w")
    for element in wrong_sigma:
        fileFailed.write("{0}, {1}".format(element[0], element[1]))


### Pre-mainFunction check
if len(sys.argv) == 3:
    # Send file location to main function
    mainFunction(sys.argv[1], sys.argv[2])
else:
    print("Usage: python path_to_preamble path_to_waveforms")