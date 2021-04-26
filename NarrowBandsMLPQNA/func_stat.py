# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:10:29 2020

@author: Alex Razim
"""

from numpy import nan,around,std,mean,abs,histogram
from scipy.stats import median_absolute_deviation as MAD
import pandas as pd

def createStatTab(cases,estimators=['Std','NMAD','Mean','% outl_15'],indexName=None,addCols=None):
    colNames=pd.MultiIndex.from_product([cases,estimators])
    statTab=pd.DataFrame(columns=colNames)
    statTab[('General','Num objects')]=nan
    if addCols!=None:
        for name in addCols:
            statTab[('General',name)]=nan
    if indexName!=None:
        statTab.index.name=indexName
    return statTab

### Dictionary with statistics for resid ###
def statResid(df,colResid):
    if colResid==None:
        statDict={'Num objects':nan,
                  'Std':nan,
                  'NMAD':nan,
                  'Mean':nan}
    else:
        statDict={'Num objects':int(len(df)),
                  'Std':around(std(df[colResid]),3),
                  'NMAD':around(MAD(df[colResid]),3),
                  'Mean':around(mean(df[colResid]),4)}
        if len(df)>0:
            statDict['% outl_15']=around(len(df[abs(df[colResid])>0.15])/len(df)*100,2)
        else:
            statDict['% outl_15']=0
    return statDict

def allStatsAddRec(allStats,case,data,residCols,addCols={}):
    for col in residCols:
        stat=statResid(data,col)
        allStats.loc[case,(col,'Std')]=stat['Std']
        allStats.loc[case,(col,'NMAD')]=stat['NMAD']
        allStats.loc[case,(col,'Mean')]=stat['Mean']
        allStats.loc[case,(col,'% outl_15')]=stat['% outl_15']

    allStats.loc[case,('General','Num objects')]=stat['Num objects']
    for key,val in addCols.items():
        allStats.loc[case,('General',key)]=val
    return allStats

def statByBins(df,binCol,residCols,bins=12):
    counts, bin_edges=histogram(df[binCol],bins)    
    binning={}
    for i in range(len(bin_edges)-1):
        binning[bin_edges[i+1]]=df[(df[binCol]>bin_edges[i]) & (df[binCol]<=bin_edges[i+1])]
        
    statTab=createStatTab(residCols,addCols=['binEdge'])

    for key,binned in binning.items():
        if len(binned)>0:
            statTab=allStatsAddRec(statTab,case=key,data=binned,residCols=residCols,addCols={'binEdge':key})
    return statTab

def printStat(stat,fprecision=3,colsAsInt=[('General','Num objects')],hideIndex=False):
    formatter={k: '{:.'+str(fprecision)+'f}' for k in stat.columns}
    for k in colsAsInt:
        formatter[k]='{:.0f}' 
    if hideIndex==True:
        stat=stat.style.format(formatter).hide_index()
    else:
        stat=stat.style.format(formatter).set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
    return stat

