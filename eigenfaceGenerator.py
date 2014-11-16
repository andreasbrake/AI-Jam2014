import os, glob
import numpy as np
from PIL import Image

# helper function to print out a flat image taking its height and
# width as parameters
def printImage(name, flatImage, height, width):
    # prints mean image to file
    outArray = np.array(flatImage)
    outArray.resize(height, width)
    out = Image.fromarray(outArray)
    out.save("./img/" + name + ".gif","GIF")

# compute the demeaned images for one individual's photos
def computeDemeanedImages():
    imgList = [] # the list of image names corresponding to one individual (i.e. 8)

    for imgName in glob.glob("./img/*_*_.gif"):
        imgList.append(imgName)
    #imgList.remove("./img/8_1_.gif")
    
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

    #printImage(demeanedImages[9], height, width)

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
    # remove the inaccurate eigenfaces
    for i in range(len(covarianceEigenValues)):
        temCovar = covarianceEigenVectors.T
        temCovar[i] = 255 * (covarianceEigenVectors.T[i] / np.linalg.norm(covarianceEigenVectors.T[i]))
        covarianceEigenVectors = temCovar.T

        #printImage("eigen_" + str(i), covarianceEigenVectors.T[i], 243, 320)
        if covarianceEigenValues[i] < threshold:
            eigenVectorsToRemove.append(i)

    #print list(np.array(covarianceEigenVectors.T[0])[0])
    covarianceEigenVectors = np.delete(covarianceEigenVectors.T, eigenVectorsToRemove, 0).T

    #print np.uint8(covarianceEigenValues)

    return covarianceEigenVectors
