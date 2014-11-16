import numpy as np
from PIL import Image
import re

# function to calculate the projections of the training images and and the test image
# in the face space (eigen faces)
# faceSpace and traingingSpace currently passed with vectors as columns
def trainingProjections(testImage, imgList, faceSpace, demeanedImages, flatMean, trainingDistances, threshold):
    # retrieve and flatten test image
    testImage = np.array(Image.open(testImage), dtype = np.float)
    testImage = np.resize(testImage, (1, 77760))

    # projection of testImage onto the faceSpace
    testImageDistance = faceSpace.T * (testImage - flatMean).T

    xf = faceSpace.T * (testImage + flatMean).T
    reconDist = np.linalg.norm(testImage - xf)

    # Compute the min distance from the test image to the face space
    distance = float("inf")
    maxDist = 0
    idx = -1
    
    # TODO not doing anything if image unknown
    unknown = True
    for i in range(len(trainingDistances)):
        curDist = np.linalg.norm(testImageDistance - trainingDistances[i])
        if curDist < distance:
            distance = curDist
            idx = i
        if curDist > maxDist:
            maxDist = curDist
        if curDist < threshold:
            unknown = False

    # debugging
    print distance, threshold, maxDist
    
    # print the id of the subject found
    print imgList[idx]
    return re.search('[^\d]*(\d+)_\d+_.gif', imgList[idx]).group(1)
