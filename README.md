# mppc-characterization
A few python scripts to help with the MPPC's characterization measurements.

## eventDisplay.py
Loads the waveform information from a file and plots it using matplotlib. Usage:
```bash
python eventDisplay.py <path_to_preamble> <path_to_waveform_file>
```
where ```<path_to_preamble>``` is the location of the waveform preamble file,
used to convert the data in ```<path_to_waveform_file>``` from screen points to mV by ns.

## histogram_area.py
Loads the files with the integrated waveform information.
Such file is required to have two columns: 
one with the waveform name;
another with the respective waveform's area.
Usage:
```bash
python histogram_area.py <path_to_areas_file>
```
where ```<path_to_areas_file>``` is the location of your file, e.g. ```/home/user/data/areas-01.dat```
