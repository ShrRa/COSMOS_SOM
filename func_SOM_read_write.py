# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:03:48 2020

@author: Alex Razim
"""
import minisom
from ndarr_read_write import writeWeights,readWeights

def createSOM(data, epochs, height, width, num_features, sigma, learning_rate, 
                    neighborhood_function, random_seed=10, saveWeightsName=None):
    som=minisom.MiniSom(height, width, num_features, sigma=sigma, learning_rate=learning_rate, 
                    neighborhood_function=neighborhood_function, random_seed=random_seed)
    som.pca_weights_init(data)
    som.train_random(data, epochs, learn_curve=False)
    if saveWeightsName!=None:
        writeSOM(som,saveWeightsName)
    return som

def writeSOM(som,saveWeightsName):
    somWeigths=som.get_weights()
    writeWeights(somWeigths,saveWeightsName)
    return

def loadSOM(weightsFile,sigma,learning_rate,neighborhood_function='bubble',random_seed=10):
    weights=readWeights(weightsFile)
    height=weights.shape[0]
    width=weights.shape[1]
    num_features=weights.shape[2]
    som=minisom.MiniSom(height, width, num_features, sigma=sigma, learning_rate=learning_rate, 
                    neighborhood_function=neighborhood_function, random_seed=random_seed)
    weights=readWeights(weightsFile)
    som.set_weights(weights)
    return som


