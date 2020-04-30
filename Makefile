# from https://jayrambhia.wordpress.com/2012/06/25/configuring-boostpython-and-hello-boost/
# note: IST's boost 1.70.0 has only support for python 2.7,
#  so `module load python/2.7.13-gpu`
# PYTHON_VERSION = 2.7
PYTHON_VERSION = 3.6
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)
PYTHON_LIB_CONFIG = /usr/lib/python$(PYTHON_VERSION)/config-$(PYTHON_VERSION)m-x86_64-linux-gnu/
#PYTHON_LIB_CONFIG = /usr/lib/python$(PYTHON_VERSION)/
#PYTHON_LIB_CONFIG = /usr/lib/python$(PYTHON_VERSION)/config-x86_64-linux-gnu/
#PYTHON_LIB_CONFIG = /mnt/nfs/clustersw/Debian/stretch/python/3.6.9/lib/
 
# location of the Boost Python include files and library
 
# default BOOST on IST cluster in 1.62.0, only >1.63.0 has numpy support
# with `module load boost`, IST provides version 1.70.0
# use `module display boost` to find these include and library paths
#BOOST_INC = /usr/include
BOOST_VERSION = 1.65.1
#BOOST_INC = /mnt/nfs/clustersw/Debian/stretch/boost/$(BOOST_VERSION)/include/
BOOST_INC = /usr/include/boost/
#BOOST_LIB = /usr/lib
#BOOST_LIB = /mnt/nfs/clustersw/Debian/stretch/boost/$(BOOST_VERSION)/lib/
BOOST_LIB = /usr/lib/x86_64-linux-gnu/

# IMP: `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/mnt/nfs/clustersw/Debian/stretch/boost/1.70.0/lib/` in ~/.bashrc
 
# compile mesh classes
TARGET = EMBasins
CC = g++-7 # set g++ to 7 because code doesn't compile on 9.3, TODO fix it
 
$(TARGET).so: $(TARGET).o
	$(CC) -shared -Wl,--export-dynamic $(TARGET).o BasinModel.o TreeBasin.o -L$(BOOST_LIB) -lgsl -lgslcblas -lboost_python3 -lboost_numpy3  -L$(PYTHON_LIB_CONFIG) -lpython$(PYTHON_VERSION) -o $(TARGET).so
 
$(TARGET).o: $(TARGET).cpp
	$(CC) -fPIC -c BasinModel.cpp
	$(CC) -fPIC -c TreeBasin.cpp
	$(CC) -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp

clean:
	rm *.o
	rm *.so
