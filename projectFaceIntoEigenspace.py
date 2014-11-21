import os, glob
import numpy as np
import dataHandler as db
import eigenfaceGenerator as eg
from PIL import Image
import re

# function to calculate the projections of the training images and and the test image
# in the face space (eigen faces)
# faceSpace and traingingSpace currently passed with vectors as columns
def trainingProjections(testImageName, imgList, faceSpace, demeanedImages, flatMean, trainingDistances, threshold):
    threshold *= 0.75

    # retrieve and flatten test image
    testImageName = testImageName.replace("\\", "/")
    width, height = Image.open(testImageName).size
    imgSize = width * height;

    testImage = np.array(Image.open(testImageName).convert("L"), dtype = np.float)
    testImage = np.resize(testImage, (1, imgSize))

    # projection of testImage onto the faceSpace
    testImageDistance = faceSpace.T * (testImage - flatMean).T
    #eg.printImage((testImage - flatMean), 243, 320)


    xf = faceSpace.T * (testImage + flatMean).T
    reconDist = np.linalg.norm(testImage - xf)

    # Build a list of distances associated with each individual
    distances = {}

    for i in range(len(trainingDistances)):
        individual = imgList[i].split("/")[-1].split("_")[0] #re.search('[^\d]*(\d+)_\d+_.gif', imgList[i]).group(1)
        curDist = int(np.linalg.norm(testImageDistance - trainingDistances[i]))
        
        if str(individual) in distances:
            individualDistances = distances[individual][1]
            individualDistances.append(curDist)
            distances[individual] = (distances[individual][0]+1, individualDistances)
        else:
            distances[individual] = (1, [curDist])

    # Compute a weighted mean distance to each individual defined by the
    # mean of all the distances to images of that individual and the
    # negative deviation from the mean.

    imageDistances = [] # top 5 images
    unidentifiable = True
    analDist = []

    for individual in distances:
        meanDistance = 0

        for distance in distances[individual][1]:
            imageDistances.append((individual, distance))
            meanDistance += distance

        meanDistance /= float(distances[individual][0])

        if meanDistance < threshold:
            unidentifiable = False

        analDist.append((individual, meanDistance))

    analDist.sort(key=lambda tup: tup[1])
    newAnal = []

    for i in range(0, len(analDist)):
        if i < 5 and len(analDist) > i:
            if analDist[i][1] < threshold:
                newAnal.append(analDist[i])
        else: 
            break

    if len(newAnal) == 0:
        return ("UNKNOWN",threshold)
    if len(newAnal) > 1:
        if newAnal[1][1] <= (newAnal[0][1] * 1.1):
            return ("UNKNOWN",newAnal[0][1])
    if unidentifiable:
        return ("UNKNOWN",newAnal[0][1])
    return newAnal[0] #imgList[idx].split("/")[-1].split("_")[0]
