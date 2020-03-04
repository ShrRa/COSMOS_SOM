# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:06:18 2020

@author: Alex Razim
"""
import minisom
import pandas as pd
import numpy as np

def addBMUWeights(som,data,magsScaled):
    BMUWeights=som.quantization(np.array(data[magsScaled]))
    BMUWeights=pd.DataFrame(BMUWeights,columns=['w_'+s for s in magsScaled])
    data=pd.concat([data,BMUWeights],axis=1)
    return data

def addQuantErr(data,magsScaled,colWeights=None):
    diff=pd.DataFrame()
    if colWeights is None:
        colWeights=['w_'+s for s in magsScaled]
    for col,w in zip(magsScaled,colWeights):
        diff[col]=data[col]-data[w]
    diff=np.array(diff)
    quantErr=[]
    for row in diff:
        quantErr.append(np.sqrt(np.dot(row, row.T)))
    data['quantErr']=quantErr
    return data

def addCellAddress(som, data, magsScaled, idCol,cellIDPrefix):
    workCols=magsScaled+[idCol]
    d=data[workCols]
    cells=som.cells_map(data=np.array(d),colsToDrop=[d.columns.get_loc(idCol)])
    cells=pd.DataFrame(data=cells,columns=workCols+['cellY','cellX'])
    data['cellID'+cellIDPrefix]=[(int(y),int(x)) for x,y in zip(cells['cellX'],cells['cellY'])]
    return data

def calcOutlCoeff(data,stdMap,meanMap,filterCol,cellID,prefix=''):
    getMean=lambda i: meanMap[i]
    means=list(map(getMean,data[cellID]))
    getStd=lambda i: stdMap[i]
    stds=list(map(getStd,data[cellID]))
    coeffs=(means-data[filterCol])/stds
    data[prefix+filterCol+'_outlCoeff']=coeffs
    return data

def addOccupation(dataset,cellID,activMap):
    getOccupation=lambda i: activMap[i]
    occupations=list(map(getOccupation,dataset[cellID]))
    dataset['trainMapOccupation']=occupations
    return dataset