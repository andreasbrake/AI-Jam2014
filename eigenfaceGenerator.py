import os, numpy, glob
from PIL import Image

# compute the demeaned images for one individual's photos
def computeDemeanedImages(imgId):
    imgList = [] # the list of image names corresponding to one individual (i.e. 8)

    for imgName in glob.glob("./img/" + imgId + "_*_.gif"):
        imgList.append(imgName)

    # Assuming all images are the same size, get dimensions of first image
    width, height = Image.open(imgList[0]).size
    imgSize = width * height;
    numImages = len(imgList)

    # Create a numpy array of floats to store the average (assume RGB images)
    meanImage = numpy.zeros((height, width), numpy.float)

    allImages = [] # each row is flattened image

    # build the mean image and populates arrays
    for img in imgList:
        currentImage = numpy.array(Image.open(img), dtype = numpy.float)
        meanImage = meanImage + (currentImage / numImages)
        currentImage = numpy.resize(currentImage, (1, imgSize))

        # type hacking
        if len(allImages) == 0:
            allImages = currentImage # initialize allImages with the currentImage
        else:
            allImages = numpy.append(allImages, currentImage, axis=0)

    # rounding everything to integers
    allImages = numpy.array(numpy.round(allImages), dtype = numpy.uint8)
    meanImage = numpy.array(numpy.round(meanImage), dtype = numpy.uint8)

    # mean matrix currently width x height, so we flatten to 1-D array
    flatMean = numpy.resize(meanImage, (1, imgSize))

    # subtract the mean from each image
    demeanedImages = numpy.matrix(allImages) - flatMean

    # Transpose to get images as columns
    return demeanedImages.T # array of flattened demeaned images

# returns the covariance eigenvalues and eigenvectors
def computeCovarianceEigens(demeanedImages):
    # numImages x numImages
    pseudoS = demeanedImages.T * demeanedImages

    # gets the covarianceEigenValues (1 x numImages) and eigenVectors (numImages x numImages)
    covarianceEigenValues, eigenVectors = numpy.linalg.eig(pseudoS)
    covarianceEigenVectors = demeanedImages * eigenVectors

    return covarianceEigenValues, covarianceEigenVectors

def main():
    # range will be from 1 to 16 (15 sets of images)
    for i in range(1,2):
        demeanedImages = computeDemeanedImages(str(i))
        print computeCovarianceEigens(demeanedImages)

if __name__ == "__main__":
    main()
