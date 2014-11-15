import os, glob
import numpy as np
import dataHandler as db
from PIL import Image

# function to calculate the projections of the training images and and the test image
# in the face space (eigen faces)
# faceSpace and traingingSpace currently passed with vectors as columns
def trainingProjections(testImage, faceSpace, demeanedImages, flatMean):

    trainingDistances = []

    faceSpaceTranspose = faceSpace.T
    demeanedImagesTranspose = demeanedImages.T

    print faceSpaceTranspose.shape
    print demeanedImagesTranspose[0,:].T.shape

    for i in range(len(demeanedImagesTranspose)):
        trainingDistances.append(faceSpaceTranspose * demeanedImagesTranspose[i,:].T)

    testImage = np.array(Image.open(testImage), dtype = np.float)

    testImage = np.resize(testImage, (1, 77760))

    testImageMinusMean = testImage - flatMean

    testImageDistance = faceSpaceTranspose * testImageMinusMean.T

    print testImageDistance