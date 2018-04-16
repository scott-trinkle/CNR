# CNR

A GUI and series of tools to find the acquisition energy
that optimizes the contrast-to-noise ratio (CNR) in
synchrotron microCT images.

## Installation

Download source files with:

`git clone https://github.com/scott-trinkle/CNR.git`

Install dependencies (numpy, matplotlib and scipy): 

`cd CNR`

`pip install -r requirements.txt`

Then install CNR with 

`pip install .`

## To run

Run with:

`python cnrgui/run_GUI.py` 

This will launch a matplotlib-based GUI displaying CNR as a function of x-ray
energy under adjustable experimental parameters. 

The file contains well documented variables that can be edited to customize the
allowable ranges of values for the sliders in the GUI. There is also a variable
controlling whether the length variables are in units of mm or nm.

## CNR Model

The CNR is calculated with the following model based on [Spanne, 1989](http://iopscience.iop.org/article/10.1088/0031-9155/34/6/004/pdf):

![](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Ctext%7BCNR%7D%28E%29%20%3D%20%5Cfrac%7B%7C%5Cmu_1%28E%29%20-%20%5Cmu_2%28E%29%7C%7D%7B%5Csqrt%7B%5Ctext%7Bvar%7D%5C%7B%5Cmu_1%28E%29%5C%7D%20&plus;%20%5Ctext%7Bvar%7D%5C%7B%5Cmu_2%28E%29%5C%7D%7D%7D)

where 
![](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Cmu_1%28E%29%20%5Cequiv%20%5Cmu_%7Bbg%7D%28E%29)
is the attenuation at the center voxel of a
homogeneous spherical object of background material "bg," and
![](http://latex.codecogs.com/gif.latex?%5Cinline%20%24%5Cmu_2%28E%29%20%5Cequiv%20%5Cmu_%7Bbg%7D%28E%29%20&plus;%20%5Cmu_c%28E%29%24) 
is the attenuation of that same voxel
with the addition of a small amount of contrast material "c.'' 
These two cases are indexed by 
![](http://latex.codecogs.com/gif.latex?%5Cinline%20%24i%20%5Cin%20%5B1%2C2%5D%24).

The variance is defined as

![](http://latex.codecogs.com/gif.latex?%5Ctext%7Bvar%7D%5C%7B%5Cmu_i%28E%29%5C%7D%20%5Cpropto%20%5Cfrac%7B1%7D%7B%5Cbar%7BN%7D_i%28E%29%7D%2C)

where

![](http://latex.codecogs.com/gif.latex?%5Cbar%7BN%7D_i%28E%29%20%3D%20I_0%5Cint_0%5E%7B%5Cinfty%7D%20dE%27N%28E%27%20%7C%20E%2C%20%5Csigma_%7BE%2CBW%7D%29%5Ctext%7B%20exp%7D%5C%7B-A_i%28E%27%29%5C%7D%2C)

Here, ![](http://latex.codecogs.com/gif.latex?%5Cinline%20%24I_0%28E%29%24) 
is the incident intensity given by

![](http://latex.codecogs.com/gif.latex?I_0%28E%29%20%3D%20I_0%20N%28E%20%7C%20E%2C%20%5Csigma_%7BE%2CBW%7D%29%2C)

where ![](http://latex.codecogs.com/gif.latex?%5Cinline%20N%28E%20%7C%20E%2C%20%5Csigma_%7BE%2CBW%7D%29)
is a Gaussian function with mean E and standard deviation ![](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Csigma_%7BE%2CBW%7D)

![](http://latex.codecogs.com/gif.latex?%5Cinline%20A_i%28E%29) is given by

![](http://latex.codecogs.com/gif.latex?A_i%28E%29%20%3D%20%5Csum_%7Bj%7D%5Cmu_j%28E%29%20d_j%2C)

where ![](http://latex.codecogs.com/gif.latex?%5Cinline%20d_j) is the length of each material, j, that is present in case i.
