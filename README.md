# CNR

Developing a series of tools and GUIs to optimize contrast-to-noise ratio (CNR) in synchrotron microCT images.

## To launch the GUI

Run the python script 'code/run_GUI.py' to launch a matplotlib-based GUI displaying CNR as a function of x-ray energy under adjustable experimental parameters. The file contains well documented variables that can be edited to customize the allowable ranges of values for the sliders in the GUI. There is also a variable controlling whether the length variables are in units of mm or nm. 

## To compare the current and previous implementations

The folder 'replicating_alexandras_plots/' contains work related to reproducing plots made by former student Alexandra Rojek. Most importantly, the file 'replicating_alexandras_plots.pdf' contains side-by-side comparisons between CNR plots made by Alexandra and those made by myself.

Note that similar trends are seen for the plots varying total thickness (Figures 5A and 5B), but the CNR trend is reversed for plots varying contrast density (Figures 4A and 4B). The same parameters are represented in the default slider ranges set by the 'run_GUI.py' interface - you can see that increasing the contrast density reduces the CNR for very small values (up to about 0.02 g/cc). After this point, increasing the contrast density increases the CNR, as expected. 

The folders 'alexandras_plots/' and 'my_plots/' contain the .pngs used to create the .pdf. Alexandra's figures were taken from 'Alexandra Rojec ACS Paper.pdf', my figures were generated with 'replicate_plots.py'

## Data/

The folder 'atten_data/' contains attenuation data for all relevant materials, taken from [NIST](https://physics.nist.gov/PhysRefData/FFast/html/form.html). The raw data was saved into individual .txt files in the folder 'raw_data/'. The script 'convert_to_numpy.py' reads in the .txt files and saves them to the .npy format, where they are read into the GUI scripts. 
