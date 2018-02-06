# CNR

Developing a series of tools and GUIs to optimize contrast-to-noise ratio (CNR) in synchrotron microCT images.

## code

Run '1D_gui.py' to launch a Python GUI displaying CNR as a function of x-ray energy, with options to adjust contrast and background material parameters. 

## replicating_alexandras_plots

'replicating_alexandras_plots.pdf' contains side-by-side comparisons between CNR plots made by former student Alexandra Rojek and those made by myself. Note that similar trends are seen for the plots varying total thickness (Figures 5A and 5B), but the CNR trend is reversed for plots varying contrast density (Figures 4A and 4B). The same parameters are within the current ranges set by the '1D_gui.py' interface - you can see that increasing the contrast density reduces the CNR for very small values (up to about 0.02 g/cc). After this point, increasing the contrast density increases the CNR, as expected. 

The folders 'alexandras_plots/' and 'my_plots' contain the .pngs in the .pdf. Alexandra's figures were taken from 'Alexandra Rojec ACS Paper.pdf', my figures were generated with 'replicate_plots.py'
