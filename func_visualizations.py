# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:09:03 2020

@author: Alex Razim
"""
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from numpy import nan,nanmin,nanmax,max,min,ones_like,array,linspace

def plotSOM(mapToPlot,height,width,title,saveFlag=False,saveName='',axs=None,cmap='plasma',
            vmin=None,vmax=None,badVal=None,under=False,cb=True):
    mapToPlot2=mapToPlot
    if axs is None:
        axs = plt.gca()
    cmap=cm.get_cmap(cmap)
    cmap.set_bad(color='black',alpha=1)
    if under==True:
        cmap.set_under('gray')
    else:
        cmap.set_under(cmap(0))
    mapToPlot2[mapToPlot2==badVal]=nan
    im1=axs.pcolormesh(mapToPlot2, cmap=cmap,vmin=vmin,vmax=vmax)
    if cb==True:
        cb=plt.colorbar(im1,ax=axs)
        cb.ax.tick_params(labelsize=15)
    else:
        cb=im1
    axs.set_title(title,fontsize=14)
    axs.tick_params(labelsize=15)
    if saveFlag==True:
        if saveName=="":
            plt.savefig(title.replace(' ','_')+'.png')
        else:
            plt.savefig(saveName)
    return axs,cb

def plotSOMRow(mapsDict,cases,estimator,axes, row,height, width,cmap='plasma',vmin=None, vmax=None,badVal=None,cbFlag=False,fig=None,axisToPlot=None):
    if axisToPlot==None:
        if vmin==None:
            vmin=min([nanmin(mapsDict[estimator][c]) for c in cases])
        if vmax==None:
            vmax=max([nanmax(mapsDict[estimator][c]) for c in cases])
        for i,c in enumerate(cases):
            t,im=plotSOM(mapsDict[estimator][c],height,width,estimator+' ('+c+') map',axs=axes[row][i],cmap=cmap,
                badVal=badVal,vmin=vmin,vmax=vmax,cb=cbFlag)
    else:
        [axes[row][i].axis('off') for i,ax in enumerate(axes[row]) if i!=axisToPlot]
        t,im=plotSOM(mapsDict[estimator],height,width,estimator+" map",axs=axes[row][axisToPlot],cmap=cmap,
                     vmin=vmin,vmax=vmax,badVal=badVal,under=False,cb=cbFlag)
    if cbFlag==False:
        cb=fig.colorbar(im, ax=axes[row].ravel().tolist(),pad=0.02)
        cb.ax.tick_params(labelsize=15)
        
### Multiple histograms on one plot ###
def plotMultiBar(datasets,numBins,labels,alpha,logScale=False,normCounts=False,saveFlag=False,
                  range=None, saveName='',xlabel='',ylabel='',axs=None,grayscale=False,edgecolor='black'):
    if axs is None:
        axs = plt.gca()
        
    colorBlindPalette=['#000000','#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7']
    grayScalePalette=['#4c4c4c','#cccccc','#999999','#101010','#dedede']
    if grayscale==True:
        palette=grayScalePalette
    else:
        palette=colorBlindPalette 
    textSize=14
    if logScale==True:
        axs.set_yscale('log')
    if normCounts==True:
        weights=[]
        for data in datasets:
            weight = ones_like(data)/float(len(data))
            weights.append(weight)
        n, bins, patches = axs.hist(datasets, bins=numBins,weights=weights,color=palette[:len(datasets)],
                 alpha=alpha, label=labels,edgecolor=edgecolor, linewidth=1.2, range=range)
    else:
        n, bins, patches = axs.hist(datasets,bins=numBins,color=palette[:len(datasets)],
                 alpha=alpha,label=labels,edgecolor=edgecolor, linewidth=1.2, range=range)  
    if grayscale==True:
        hatches = ['..', 'xx', '**','','|||']
        for patch_set, hatch in zip(patches, hatches):
            plt.setp(patch_set, hatch=hatch)
    axs.set_xlabel(xlabel,size=textSize)
    axs.set_ylabel(ylabel,size=textSize)
    axs.legend(prop={'size': 10})

    if saveFlag==True:
        if saveName=="":
            print("Cannot save catalog: saveName is empty string")
        else:
            plt.savefig(saveName)
    return

### Multiple histograms on one plot ###
def plotMultiBar2(datasets,bins,labels,alpha,logScale=False,normCounts=False,saveFlag=False,
                  range=None, saveName='',xlabel='',ylabel='',axs=None,grayscale=False,edgecolor='black',medianLine=True):
    if axs is None:
        axs = plt.gca()
        
    colorBlindPalette=['#000000','#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7']
    grayScalePalette=['#4c4c4c','#cccccc','#999999','#101010','#dedede']
    if grayscale==True:
        palette=grayScalePalette
    else:
        palette=colorBlindPalette 
    textSize=14
    if logScale==True:
        axs.set_yscale('log')
        
    if normCounts==True:
        weights=[]
        for i,data in enumerate(datasets):
            weight = ones_like(data)/float(len(data))
            weights.append(weight)
            n, bins, patches = axs.hist(array(data), bins=bins,weights=weight,histtype='stepfilled',color=palette[i],
                 alpha=alpha, label=labels[i],edgecolor=edgecolor, linewidth=1.2, range=range)
    else:
        for i,data in enumerate(datasets):
            n, bins, patches = axs.hist(array(data),bins=bins,histtype='stepfilled',color=palette[i],
                 alpha=alpha,label=labels[i],edgecolor=edgecolor, linewidth=1.2, range=range)  
    if medianLine==True:
        for i,data in enumerate(datasets):
            axs.axvline(float(data.median()),color=palette[i],linewidth=2,linestyle='dashed')
    
    if grayscale==True:
        hatches = ['..', 'xx', '**','','|||']
        for patch_set, hatch in zip(patches, hatches):
            plt.setp(patch_set, hatch=hatch)
    axs.set_xlabel(xlabel,size=textSize)
    axs.set_ylabel(ylabel,size=textSize)
    axs.legend(prop={'size': 10})

    if saveFlag==True:
        if saveName=="":
            print("Cannot save catalog: saveName is empty string")
        else:
            plt.savefig(saveName)
    return

def drawMagDistribs(datasets,mags,labels,numBins,xlim,ylim,normCounts=True,logScale=False,h=5,w=2):
    fig, axs = plt.subplots(h,w,figsize=(15,h*5),sharey=True)
    for i in range(h):
        for j in range(w):
            data=[d[[mags[i*w+j]]] for d in datasets]
            axs[i][j].grid(axis='y',linestyle ='--')
            if normCounts==True:
                ylabel='Normalized number of objects'
            else:
                ylabel='Number of objects'
            plotMultiBar2(data,linspace(xlim[0], xlim[1], numBins),labels,logScale=logScale,
                          alpha=0.8,normCounts=normCounts,xlabel=mags[i*w+j],
                          ylabel=ylabel,axs=axs[i][j],edgecolor='black')
            axs[i][j].set_xlim(xlim[0],xlim[1])
            axs[i][j].set_ylim(ylim[0],ylim[1])
            if j>0:
                axs[i][j].set_ylabel(None)
    plt.tight_layout()
    return fig

def plotBinnedStats(stats,estimators,residCols,binCol):
    colorBlindPalette=['#000000','#E69F00','#009E73','#0072B2','#D55E00','#56B4E9','#F0E442','#CC79A7']
    fig, axs = plt.subplots(len(estimators), 2,figsize=(15,4*len(estimators)),sharey='row',sharex='col')
    if len(estimators)==1:
        axs=[axs]
    for i,est in enumerate(estimators):
        for j, c in enumerate(residCols):
            axs[i][j].grid(axis='y',linestyle ='--')
            axs[i][j].grid(axis='x',linestyle ='--')
            axs[i][j].set_ylabel(est+' resid_'+c,size=12)
            for k,(key,val) in enumerate(stats.items()):
                axs[i][j].plot(val['General']['binEdge'],val[c][est],
                               label=key+' filter',marker='o',markersize=10-2*k,c=colorBlindPalette[k])
            axs[i][j].legend()
    axs[i][0].set_xlabel(binCol,size=12)
    axs[i][1].set_xlabel(binCol,size=12)
    plt.tight_layout()
    return fig
