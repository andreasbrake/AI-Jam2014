import os, glob
import numpy as np
import dataHandler as db
from PIL import Image
import projectFaceIntoEigenspace as projectTestFace

# helper function to print out a flat image taking its height and
# width as parameters
def printImage(flatImage, height, width):
    # prints mean image to file
    outArray = np.array(flatImage)
    outArray.resize(height, width)
    out = Image.fromarray(outArray)
    out.save("./img/printoutput.gif","GIF")

# compute the demeaned images for one individual's photos
def computeDemeanedImages():
    imgList = [] # the list of image names corresponding to one individual (i.e. 8)

    for imgName in glob.glob("./img/*_*_.gif"):
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
    return flatMean, demeanedImages.T, allImages # array of flattened demeaned images

# returns the covariance eigenvalues and eigenvectors
def computeCovarianceEigens(demeanedImages):
    # numImages x numImages
    pseudoS = demeanedImages.T * demeanedImages

    # gets the covarianceEigenValues (1 x numImages) and eigenVectors (numImages x numImages)
    covarianceEigenValues, eigenVectors = np.linalg.eig(pseudoS)
    covarianceEigenVectors = demeanedImages * eigenVectors

    return covarianceEigenValues, covarianceEigenVectors

def main():
    flatMean, demeanedImages = computeDemeanedImages()
    eigenValues, eigenVectors = computeCovarianceEigens(demeanedImages)

if __name__ == "__main__":
    main()
