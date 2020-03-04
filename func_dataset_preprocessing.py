# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:16:45 2020

@author: Alex Razim
"""
import pandas as pd
from sklearn import preprocessing
from numpy import array

### Create resid column ###
def residCol(df,colSpectrZ, colPhotoZ,colResid):
    df[colResid]=(df[colSpectrZ]-df[colPhotoZ])/(df[colSpectrZ]+1)
    return df

### Normalizing magnitudes to 0-1 range for SOM training ###
def scaleMags(dataOrig,mags,magsScaled,dataScaleTo=None):
    if set(magsScaled).issubset((dataOrig).columns):
        print('Scaled mags are already present in dataOrig!')
        return
    scaler = preprocessing.MinMaxScaler()
    dataScaled=dataOrig[mags].copy(deep=True)
    dataScaled=array(dataScaled)
    if dataScaleTo is None:
        dataScaled = scaler.fit_transform(dataScaled)
    else:
        magsScaleTo=dataScaleTo[mags].copy(deep=True)
        scaler.fit(magsScaleTo)
        dataScaled=scaler.transform(dataScaled)
    dataOrig=pd.concat([dataOrig,pd.DataFrame(dataScaled,columns=magsScaled)],axis=1)
    return dataOrig

##### Merging photometry and ML photo-z outputs #####
def mergeCatalogs(mergeDf,mergeToDf,colRename,colDelete=None,resids=True,specZ='specZ',photoZ_ML='photoZ_ML',photoZ_SED='photoZ_SED'):
    residML='resid_ML'
    residSED='resid_SED'
    residML_SED='residML_SED'
    outDf=mergeDf.merge(mergeToDf.set_index('Seq'), on='Seq',how='inner')
    outDf=outDf.rename(columns=colRename)
    if colDelete!=None:
        try:
            outDf=outDf.drop(columns=colDelete)
        except:
            print('No column '+ colDelete + ' in merged dataFrame ')
    if resids==True:
        outDf=residCol(outDf,colSpectrZ=specZ,colPhotoZ=photoZ_ML,colResid=residML)
        outDf=residCol(outDf,colSpectrZ=specZ,colPhotoZ=photoZ_SED,colResid=residSED)
        outDf=residCol(outDf,colSpectrZ=photoZ_SED,colPhotoZ=photoZ_ML,colResid=residML_SED)
    return outDf