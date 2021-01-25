# mppc-characterization
A few python scripts to help with the MPPC's characterization measurements.

## eventDisplay.py
Loads the waveform information from a file and plots it using matplotlib. Usage:
```bash
python eventDisplay <path_to_preamble> <path_to_waveform_file>
```
where ```<path_to_preamble>``` is the location of the waveform preamble file,
used to conver the data in ```<path_to_waveform_file>``` from screen points to mV by ns.
