The C++ code and Matlab mex bindings are from Adrianna Loback's repo [https://github.com/adriannaloback/TreeHMM-local](https://github.com/adriannaloback/TreeHMM-local), which is the code for the paper:  
Prentice, Jason S., Olivier Marre, Mark L. Ioffe, Adrianna R. Loback, Gašper Tkačik, and Michael J. Berry Ii. 2016. “Error-Robust Modes of the Retinal Population Code.” PLOS Computational Biology 12 (11): e1005148. [https://doi.org/10.1371/journal.pcbi.1005148](https://doi.org/10.1371/journal.pcbi.1005148).  
  
-------------  
  
## Python bindings added (only tested on Debian 9.11 with Python 2.7)  
Author: Aditya Gilra, 2019    
The python bindings require boostpython and boost installed. Set version numbers and paths in Makefile and run `make` on the commandline. A .so file will be generated if all files compile successfully (2-3 warning appear). You can import this module from outside this directory as long as its parent directory is in the PYTHONPATH (due to `__init__.py` file).  
  
Train on nrnspiketimes, test on nrnspiketimes_test:  
`params,w,samples,state_list,state_hist,state_list_test,state_hist_test,P,P_test,prob,prob_test,train_logli,test_logli = \
        EMBasins.pyEMBasins(nrnspiketimes, nrnspiketimes_test, float(binsize), nModes, niter)`
For details see: [https://github.com/adityagilra/UnsupervisedLearningNeuralData/blob/master/EMBasins_sbatch.py](https://github.com/adityagilra/UnsupervisedLearningNeuralData/blob/master/EMBasins_sbatch.py) in the repo: [https://github.com/adityagilra/UnsupervisedLearningNeuralData](https://github.com/adityagilra/UnsupervisedLearningNeuralData).  

You can download retinal spiking data for the above Prentice et al 2016 paper from:  
[https://datadryad.org/stash/dataset/doi:10.5061/dryad.1f1rc](https://datadryad.org/stash/dataset/doi:10.5061/dryad.1f1rc).
  
You can choose between Hidden Markov Model vs time-independent model by calling pyHMM() or pyEMBasins() respectively (no need to recompile). See details in the separate repo above.  
  
Spatial correlations / tree term can be removed by modifying this statement at the top of EMBasins.cpp (need to recompile after this)  
 // Selects which basin model to use  
 typedef TreeBasin BasinType;  
 to  
 typedef IndependentBasin BasinType;  
Thus you can switch from HMM to EMBasins to remove time-domain correlations,  
 and TreeBasin to IndependentBasin to remove space-domain correlations.  

-------------  
  
# Matlab bindings  
The Matlab bindings should work as well (last tested by AG a while ago, hopefully no changes in C++ function signatures since then!). Just comment #define PYTHON in EMBasins.cpp, and uncomment #define Matlab.  
First compile BasinModel.cpp, etc. for linux. Just compile, don't link, hence -c:  
EMBasins.cpp uses Matlab's matrix.h and mex.h, hence the -I, see:  
 [https://www.mathworks.com/help/matlab/matlab_external/mat-file-library-and-include-files.html](https://www.mathworks.com/help/matlab/matlab_external/mat-file-library-and-include-files.html)  
Also matlab complained when mex-ing, and suggested -fPIC  
`g++ -I/usr/local/MATLAB/R2019a/extern/include/  -fPIC -c EMBasins.cpp`  
`g++  -fPIC -c BasinModel.cpp`  
`g++  -fPIC -c TreeBasin.cpp`  
.o files are created and I don't need to link them, as I will mex them for Matlab.  
    
Now in matlab, as per Adrianna's Documentation_TreeHMMcode.pdf:  
`mex -largeArrayDims -I/usr/local/include -I/usr/local/Cellar/boost/1.68.0 -lgsl -lgslcblas EMBasins.cpp BasinModel.o TreeBasin.o`  
You will need Boost libraries to compile (set available version above).  
  
Now copy EMBasins.mexa64 (note Adrianna's one had mexmaci, not mexa -- it was for mac) to the working directory, and run Matlab from there.  
In matlab on the CLI, I tried: params = EMBasins(), now it crashed with an internal error,  
 but I think that's because I didn't pass any params!  
 At least, it doesn't say EMBasins not found.  

From matlab when EMBasins() is called, actually the mexFunction() inside EMBasins.cpp gets called. See:  
https://www.mathworks.com/help/matlab/apiref/mexfunction.html  
Currently mexFunction() creates an HMM model.  
  
