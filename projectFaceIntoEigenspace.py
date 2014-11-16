import os, glob
import numpy as np
import dataHandler as db
from PIL import Image

# function to calculate the projections of the training images and and the test image
# in the face space (eigen faces)
# faceSpace and traingingSpace currently passed with vectors as columns
def trainingProjections(testImage, imgList, faceSpace, demeanedImages, flatMean):

    trainingDistances = []

    faceSpaceTranspose = faceSpace.T
    demeanedImagesTranspose = demeanedImages.T

    for i in range(len(demeanedImagesTranspose)):
        trainingDistances.append(faceSpaceTranspose * demeanedImagesTranspose[i,:].T)

    testImage = np.array(Image.open(testImage), dtype = np.float)

    testImage = np.resize(testImage, (1, 77760))

    testImageMinusMean = testImage - flatMean

    testImageDistance = faceSpaceTranspose * testImageMinusMean.T

    xf = faceSpaceTranspose * (testImage + flatMean).T
    reconDist = np.linalg.norm(testImage - xf)

    # Compute the min distance from the test image to the face space
    distance = float("inf")
    idx = -1
    for i in range(len(trainingDistances)):
        curDist = np.linalg.norm(testImageDistance - trainingDistances[i])
        if curDist < distance:
            distance = curDist
            idx = i

    # print reconDist, distance
    print imgList[idx]

    # Compute the threshold
    threshold = 0
    for i in range(len(trainingDistances)):
        for k in range(i, len(trainingDistances)):
            curDist = np.linalg.norm(trainingDistances[i] - trainingDistances[k])
            if curDist > threshold:
                threshold = curDist

    # Half the max as per powerpoint slideshow from the internet
    threshold /= 2

    # print threshold
