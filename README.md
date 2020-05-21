# TreeHMM
This is a fork of [TreeHMM](https://github.com/adityagilra/TreeHMM-local) with few changes:
  * TreeHMM can now be installed as global python package
  * Added new higher level and easier to use API
  * Regularization parameter eta is exposed in API
  
  
The C++ code and Matlab mex bindings are from Adrianna Loback's repo [https://github.com/adriannaloback/TreeHMM-local](https://github.com/adriannaloback/TreeHMM-local), which is the code for the paper:  
Prentice, Jason S., Olivier Marre, Mark L. Ioffe, Adrianna R. Loback, Gašper Tkačik, and Michael J. Berry II. 2016. “Error-Robust Modes of the Retinal Population Code.” PLOS Computational Biology 12 (11): e1005148. [https://doi.org/10.1371/journal.pcbi.1005148](https://doi.org/10.1371/journal.pcbi.1005148).  
  
Compared to the original bindings, I've made some changes:
1. Wrote python bindings to both HMM and EMBasins i.e. with and without temporal correlations (no re-compiling C++ code).  
  Note also the typedef `<TreeBasin/IndependentBasin> BasinType` directive in `EMBasins.cpp` for turning spatial correlations on and off (need to recompile C++ code).  
  See below.  
2. Modfied Matlab bindings to call HMM or TreeBasins by switching the `#define matlabHMM` directive in `EMBasins.cpp` (need to recompile C++ code).  
  See below.  
3. Return a few more outputs like test-log-likelihood etc. via the bindings.
4. Avoid nan / inf -s in computing log likelihood, by checking for small numbers and replacing them by `double min = std::numeric_limits<double>::min();`
5. Added comments to clarify the code / issues

-------------  
  
# Python bindings added  
Author: Aditya Gilra, 2019
The python bindings require boostpython and boost installed. Set version numbers and paths in Makefile and run `make` on the commandline. A .so file will be generated if all files compile successfully (2-3 warning appear). Set the LD_LIBRARY_PATH to include libboost_python (see Makefile). Test in python by `import EMBasins`. You can also import this module from outside this directory, as long as its parent directory is in the PYTHONPATH (due to `__init__.py` file). It's been tested on Debian 9.11 with Python 2.7.  
For Mac systems, use Homebrew (`brew`) from the terminal to install boost and boost-python, then rename Makefile.mac to Makefile and run `make` on the terminal. Test in `python2.7` by `import EMBasins`. However, if you have library loading issues during import, add the path to libboost_python into the environment variable DYLD_LIBRARY_PATH or LD_LIBRARY_PATH on the terminal as specified in `Makefile.mac`. You may need to [disable SIP](http://osxdaily.com/2015/10/05/disable-rootless-system-integrity-protection-mac-os-x/) for these environment variables to take effect.    
Spatial correlations / tree term can be removed for both of the two models above by modifying this statement at the top of EMBasins.cpp (need to recompile after this)  
 // Selects which basin model to use  
 typedef TreeBasin BasinType;  
 to  
 typedef IndependentBasin BasinType;  
Thus you can switch from pyHMM to pyEMBasins, without recompiling, to remove time-domain correlations,  
 and TreeBasin to IndependentBasin, with recompiling, to remove space-domain correlations.
 
 After building, install pip package `pip install -e .`. Now use it in usualy way with `import TreeHMM`. Available functions are: [`TreeHMM.trainHMM`](https://github.com/zivadinac/TreeHMM-local/blob/master/TreeHMM/__train__.py#L31) (including regularization parameter eta), [`TreeHMM.io.saveTrainedHMM`](https://github.com/zivadinac/TreeHMM-local/blob/master/TreeHMM/__io__.py#L3) and [`TreeHMM.io.loadTrainedHMM`](https://github.com/zivadinac/TreeHMM-local/blob/master/TreeHMM/__io__.py#L7). Original functions (`pyInit`, `pyHMM`, `pyEMBasins`) can be accessed through `TreeHMM.orig`.
  
-------------  
  
# Matlab bindings  
The Matlab bindings should work as well. If not, then use the code from the [original repo](https://github.com/adriannaloback/TreeHMM-local).   
Just comment `#define PYTHON` in `EMBasins.cpp`, and uncomment `#define MATLAB`.  
First you need to compile BasinModel.cpp, etc.

On linux:  
Just compile, don't link, hence -c:  
EMBasins.cpp uses Matlab's matrix.h and mex.h, hence the -I, see:  
 [https://www.mathworks.com/help/matlab/matlab_external/mat-file-library-and-include-files.html](https://www.mathworks.com/help/matlab/matlab_external/mat-file-library-and-include-files.html)  
Also matlab complained when mex-ing, and suggested -fPIC  
`g++ -I/usr/local/MATLAB/R2019a/extern/include/  -fPIC -c EMBasins.cpp`  
`g++  -fPIC -c BasinModel.cpp`  
`g++  -fPIC -c TreeBasin.cpp`  
.o files are created and we don't need to link them, as we will mex them for Matlab.  
    
On Mac:  
You first need to install boost
`brew install boost --with-python`  
Then compile the C++ files as below, be sure to add the '-std=c++0x' directive, else you'll get some errors (thanks to Gasper for this tip!).  
`g++ -std=c++0x -fPIC -c EMBasins.cpp`  
`g++ -std=c++0x -fPIC -c BasinModel.cpp`  
`g++ -std=c++0x -fPIC -c TreeBasin.cpp`  
    
Now in matlab, as per Adrianna's Documentation_TreeHMMcode.pdf:  
`mex -largeArrayDims -I/usr/local/include -I/usr/local/Cellar/boost/1.68.0 -lgsl -lgslcblas EMBasins.cpp BasinModel.o TreeBasin.o`  
You will need Boost libraries (can install as above with brew) to compile (set available version in mex-ing command above).  
  
Now copy EMBasins.mexa64 on linux (.mexmaci instead of .mexa on mac) to the working directory, and run Matlab from there.  
In matlab on the CLI, you can run: ... = EMBasins(...).  
See fit_prentice.m (thanks to Gasper for a bugfix!)  
 for examples of how to use with HMM or EMBasins (with or without temporal correlations).  
  
From matlab when EMBasins() is called, actually the mexFunction() inside EMBasins.cpp gets called. See:  
https://www.mathworks.com/help/matlab/apiref/mexfunction.html  
The mexFunction called is always EMBasins() as per the EMBasins.cpp filename,  
 but internally in EMBasins.cpp, you should #define matlabHMM or not.    
  
Currently mexFunction() creates an HMM model.  
Comment the `#define matlabHMM` line in EMBasins.cpp to turn off temporal correlations.  
Comment / uncomment `typedef <...> BasinType` lines to flip spatial correlations.  

##### Note: Regularization parameter eta has also been exposed in Matlab interface, but was not tested since focus of this fork is on python.
  
------------
