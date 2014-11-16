import os, glob
import numpy as np
from PIL import Image

# helper function to print out a flat image taking its height and
# width as parameters
def printImage(name, flatImage, height=243, width=320):
    # prints mean image to file
    outArray = np.array(flatImage)
    outArray.resize(height, width)
    out = Image.fromarray(outArray)
    out.save("./img/" + name + ".gif","GIF")

# compute the demeaned images for one individual's photos
def computeDemeanedImages(excludeFile=""):
    print "excluding: " + excludeFile
    imgList = [] # the list of image names corresponding to one individual (i.e. 8)

    for imgName in glob.glob("./img/*_*_.gif"):
        imgName = imgName.replace("\\","/")
        if imgName != excludeFile:
            imgList.append(imgName)
    
    # Assuming all images are the same size, get dimensions of first image
    width, height = Image.open(imgList[0]).size
    imgSize = width * height;
    numImages = len(imgList)

    # Create a np array of floats to store the average (assume RGB images)
    meanImage = np.zeros((height, width), np.float)

    allImages = [] # each row is flattened image

    # build the mean image and populates arrays
    for img in imgList:
        currentImage = np.array(Image.open(img), dtype = np.float)
        meanImage = meanImage + (currentImage / numImages)
        currentImage = np.resize(currentImage, (1, imgSize))

        # type hacking
        if len(allImages) == 0:
            allImages = currentImage # initialize allImages with the currentImage
        else:
            allImages = np.append(allImages, currentImage, axis=0)

    # mean matrix currently width x height, so we flatten to 1-D array
    flatMean = np.resize(meanImage, (1, imgSize))

    # subtract the mean from each image
    demeanedImages = np.matrix(allImages) - flatMean

    # Transpose to get images as columns
    return imgList, flatMean, demeanedImages.T # array of flattened demeaned images

# returns the covariance eigenvalues and eigenvectors
def computeCovarianceEigens(demeanedImages):
    # numImages x numImages
    pseudoS = demeanedImages.T * demeanedImages

    # gets the covarianceEigenValues (1 x numImages) and eigenVectors (numImages x numImages)
    covarianceEigenValues, eigenVectors = np.linalg.eig(pseudoS)
    covarianceEigenVectors = demeanedImages * eigenVectors

    threshold = 100000000
    eigenVectorsToRemove = []
    temCovar = []
    # remove the inaccurate eigenfaces
    for i in range(len(covarianceEigenValues)):
        temCovar = covarianceEigenVectors.T
        temCovar[i] = (covarianceEigenVectors.T[i] / np.linalg.norm(covarianceEigenVectors.T[i]))

        #min = np.amin(temCovar[i])
        # scale up to 0
        #temCovar[i] = temCovar[i] + abs(min)
        # map the max to 1
        #max = np.amax(temCovar[i])
        #temCovar[i] = temCovar[i] / max
        # scale all to 255
        #temCovar[i] = 255 * temCovar[i]

        covarianceEigenVectors = temCovar.T

        #printImage("eigen_" + str(i), temCovar[i], 243, 320)
        if covarianceEigenValues[i] < threshold:
            eigenVectorsToRemove.append(i)

    #print list(np.array(covarianceEigenVectors.T[0])[0])

    # TODO: try benchmark with top 3 removed as suggested in that one paper
    # ind = np.argpartition(covarianceEigenValues, -3)[-3:]
    # eigenVectorsToRemove = np.append(eigenVectorsToRemove, ind)
    covarianceEigenVectors = np.delete(covarianceEigenVectors.T, eigenVectorsToRemove, 0).T

    # determine the distances between all training images
    trainingDistances = []
    faceSpaceTranspose = covarianceEigenVectors.T
    demeanedImagesTranspose = demeanedImages.T

    for i in range(len(demeanedImagesTranspose)):
        trainingDistances.append(faceSpaceTranspose * demeanedImagesTranspose[i,:].T)

    # Compute the threshold
    threshold = 0
    for i in range(len(trainingDistances)):
        for k in range(i, len(trainingDistances)):
            curDist = np.linalg.norm(trainingDistances[i] - trainingDistances[k])
            if curDist > threshold:
                threshold = curDist

    # Half the max as per powerpoint slideshow from the internet
    threshold /= 2

    #print np.uint8(covarianceEigenValues)

    return covarianceEigenVectors,covarianceEigenValues, trainingDistances, threshold
