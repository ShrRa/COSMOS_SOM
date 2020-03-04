# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:06:38 2020

@author: Alex Razim
"""

from numpy import loadtxt,savetxt

def readArray(nameOfFile):
    with open(nameOfFile, 'r') as f:
        # Read header. Any line starting with "#" will be ignored by numpy.loadtxt
        header=f.readline()
        header=header.replace('# Array shape: ','').replace(' ','').replace('\n','')
        shape=tuple(map(int, header[1:-1].split(',')))
    array = loadtxt(nameOfFile)
    array = array.reshape(shape)
    return array


def writeWeights(nDarr,nameOfFile):
    # Thanks to https://stackoverflow.com/a/3685339
    # Write the array to disk
    with open(nameOfFile, 'w') as outfile:
        # Header. Any line starting with "#" will be ignored by numpy.loadtxt
        outfile.write('# Array shape: {0}\n'.format(nDarr.shape))
    
        # Iterating through a ndimensional array produces slices along
        # the last axis. This is equivalent to data[i,:,:] in this case
        for data_slice in nDarr:
            # Writing out a break to indicate different slices...
            outfile.write('# New slice\n')
            # The formatting string indicates that I'm writing out
            # the values in left-justified columns 13 characters in width
            # with 8 decimal places.  
            savetxt(outfile, data_slice, fmt='%-13.8f')
    return
            
def readWeights(nameOfFile):
    weights=readArray(nameOfFile)
    return weights