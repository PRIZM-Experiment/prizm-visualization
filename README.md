PRIZM-Visualization
========

**Visualization tools for PRIZM and related low frequency radio experiments**

This repository is under development

Features
--------
* Interactive waterfall plotting tools (under development
* S11 plotting script - Joy Division style (see below for instructions)
* S11 plotting script - overlay


### Temporal Evolution of S11 Measurements
The plot_s11.py script can be run by passing an input and output as follows:

python plot_s11.py -input '/data/measurements/' -output '/plots/stacked.pdf'

note: the in- and output paths needs to be in quotes.

You'll need:
- matplotlib
- seaborn
- pandas
- numpy

The code makes a few assumptions:
- Measurements for different antennas are in seperate folders.
- Files with extension.txt contain the same info as .set (or a least that the .set files are not necessary)
- Every measurement (till the end of time) will have the samen frequency channels
- The end of the metadata is marked by a newline (it can handle varying metadata)
- Each date will have measurement for both polarisations (I assume NS and EW are polarisations) 
- You only care about the 1st Magnitude [dB] column
- The spectra will roughly have the same dynamic range, outliers will mess up the plot.
- You don't want to see the code and just make plots (but you can open the code)
