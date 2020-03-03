# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:08:36 2020

@author: Alex Razim
"""
from func_ndarr_read_write import readArray
from numpy import zeros,mean,std,savetxt
from ast import literal_eval
import os
import glob

def buildMaps(som,data,mapCols,idCol,cellID='cellID'):
    meanMaps=dict(zip(mapCols,
                      [zeros([som._weights.shape[0], som._weights.shape[1]]) for i in range(len(mapCols))]))
    stdMaps=dict(zip(mapCols,
                     [zeros([som._weights.shape[0], som._weights.shape[1]]) for i in range(len(mapCols))]))
    activMap=zeros([som._weights.shape[0], som._weights.shape[1]])
    IDMap={}
    for cell in data[cellID].unique():
        d=data[data[cellID]==cell]
        activMap[cell[0]][cell[1]]=len(d)
        IDMap[cell]=[n for n in d[idCol]]
        for col in mapCols:
            meanMaps[col][cell[0]][cell[1]]=mean(d[col])
            stdMaps[col][cell[0]][cell[1]]=std(d[col])
    maps={'meanMaps':meanMaps,'stdMaps':stdMaps,'activMap':activMap,'IDMap':IDMap}
    return maps

def writeMaps(maps,prefixName):
    for key,val in maps['stdMaps'].items():
        with open(prefixName+'_std_'+key+'.txt', 'w') as outfile:
            outfile.write('# Array shape: {0}\n'.format(val.shape))
            savetxt(outfile, val, fmt='%-13.8f')
                          
    for key,val in maps['meanMaps'].items():
        with open(prefixName+'_mean_'+key+'.txt', 'w') as outfile:
            outfile.write('# Array shape: {0}\n'.format(val.shape))
            savetxt(outfile, val, fmt='%-13.8f')

    with open(prefixName+'_IDMap.txt', 'w') as outfile:
        print(maps['IDMap'], file=outfile)
    
    with open(prefixName+'_activ.txt', 'w') as outfile:
        outfile.write('# Array shape: {0}\n'.format(maps['activMap'].shape))
        savetxt(outfile, maps['activMap'], fmt='%-6.0f')

def readMaps(dirMaps,prefix):
    maps={'stdMaps':{},'meanMaps':{},'IDMap':{},'activMap':[]}
    files=glob.glob(os.path.join(dirMaps,prefix+'_std_*.txt'))
    for nameOfFile in files:
        mapValues=readArray(nameOfFile)
        key=nameOfFile.replace('.txt','').replace(os.path.join(dirMaps,prefix+'_std_'),'')
        maps['stdMaps'][key]=mapValues
    
    files=glob.glob(os.path.join(dirMaps,prefix+'_mean_*.txt'))
    for nameOfFile in files:
        mapValues=readArray(nameOfFile)
        key=nameOfFile.replace('.txt','').replace(os.path.join(dirMaps,prefix+'_mean_'),'')
        maps['meanMaps'][key]=mapValues
        
    nameOfFile=os.path.join(dirMaps,prefix+'_activ.txt')
    mapValues=readArray(nameOfFile)
    maps['activMap']=mapValues
    
    nameOfFile=os.path.join(dirMaps,prefix+'_IDMap.txt')
    with open(nameOfFile, 'r') as f:
        idx=f.readline()
        idx=literal_eval(idx)
    maps['IDMap']=idx
    return maps