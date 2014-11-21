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

    minDistance = float("inf")
    imageDistances = [] # top 5 images
    maxDistance = 0
    minDistanceIndividual = "unknown"
    unidentifiable = True
    analDist = []

    for individual in distances:
        weightedMean = 0
        meanDistance = 0
        negDeviation = 0

        for distance in distances[individual][1]:
            imageDistances.append((individual, distance))
            meanDistance += distance

        meanDistance /= float(distances[individual][0])
        weightedMean = meanDistance

        negDevCount = 0
        for distance in distances[individual][1]:
            if distance < meanDistance:
                negDeviation += pow(abs(distance - meanDistance), 1)
                negDevCount += 1

        if negDevCount != 0:
            negDeviation /= negDevCount
        if negDeviation != 0:
            weightedMean /= negDeviation

        if meanDistance < threshold:
            unidentifiable = False

        analDist.append((individual, meanDistance, negDeviation, weightedMean))

    analDist.sort(key=lambda tup: tup[1])
    newAnal = []
    minMean = 0
    for i in range(0, len(analDist)):
        if i < 5:
            if analDist[i][1] < threshold:
                print analDist[i], threshold
                newAnal.append(analDist[i])
        else: 
            break

    if analDist[1][1] < (analDist[0][1] * 1.1):
        unidentifiable = True

    newAnal.sort(key=lambda tup: tup[3])

    print analDist[0][1], newAnal[0][1]
    if newAnal[0][0] != analDist[0][0] and newAnal[0][1] > (analDist[0][1] * 1.2):
        unidentifiable = True

    """
    # Compute the min distance from the test image to the face space
    distance = float("inf")
    maxDist = 0
    idx = -1

    for i in range(len(trainingDistances)):
        curDist = np.linalg.norm(testImageDistance - trainingDistances[i])
        if curDist < distance:
            distance = curDist
            idx = i
        if curDist > maxDist:
            maxDist = curDist
        # if curDist < threshold:
        #     unknown = False

    print distance, threshold, maxDistance
    
    # print the id of the subject found
    print imgList[idx]
    """
    print unidentifiable
    if unidentifiable:
        return ("UNKNOWN",newAnal[0][1])
    return newAnal[0] #imgList[idx].split("/")[-1].split("_")[0]
    

    """
    # Compute a weighted mean distance to each individual defined by the
    # mean of all the distances to images of that individual and the
    # negative deviation from the mean.

    minDistance = float("inf")
    imageDistances = [] # top 5 images
    maxDistance = 0
    minDistanceIndividual = "unknown"
    unidentifiable = True
    analDist = []

    for individual in distances:
        meanDistance = 0
        for distance in distances[individual][1]:
            imageDistances.append((individual, distance))
            meanDistance += distance

        meanDistance /= float(distances[individual][0])
                     
        negDeviation = 0
        negDevCount = 0
        for distance in distances[individual][1]:
            if distance < meanDistance:
                negDeviation += pow(abs(distance - meanDistance), 0.5)
                negDevCount += 1

        negDeviation /= negDevCount
        weightedMean = meanDistance #100 * (meanDistance / negDeviation)
           
        analDist.append((individual, meanDistance, negDeviation, weightedMean))

        if weightedMean < minDistance:
            minDistance = weightedMean
            minDistanceIndividual = (individual, meanDistance, negDeviation, weightedMean)#individual
        if weightedMean > maxDistance:
            maxDistance = weightedMean
        if weightedMean < threshold:
            unidentifiable = False

    #newAnal = []
    #for individual in analDist:
    #    if individual[1] < minMean * 1.25:
    #        newAnal.append(individual)
    #analDist = newAnal

    #for individual in analDist:
    #    weightedMean = individual[3]
        
    imageDistances.sort(key=lambda tup: tup[1])
    topImages = []
    for i in range(0, len(imageDistances)):
        if i < 5:
            topImages.append(imageDistances[i][0])

    print topImages

    newAnal = []
    for individual in analDist:
        if individual[0] in topImages:
            newAnal.append(individual)
    analDist = newAnal
"""