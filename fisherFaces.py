import glob, re
from PIL import Image
import numpy as np
import eigenfaceGenerator as eigGen

# calculate the eigenvalues/eigenvectors/Sb/Sw
def lda(X, globalMu):
    Sb = np.zeros((114, 114))
    Sw = np.zeros((114, 114))

    for i in range(len(X)):
        Xi = X[i]
        classMu = np.mean(Xi)        
        # The number of samples for this class
        Ni = len(Xi)

        SbDeltaMu = classMu - globalMu
        Sb = Sb + (Ni * np.dot(SbDeltaMu.T, SbDeltaMu))

        for k in range(Ni):
            xk = Xi[k]
            SwDeltaMu = xk - classMu
            Sw = Sw + np.dot(SwDeltaMu.T, SwDeltaMu)

    eigenValues, eigenVectors = np.linalg.eig(np.linalg.inv(Sw) * Sb)

    return eigenValues, eigenVectors

def main():
    # Compute demeanedImages
    imgList, flatMean, demeanedImages = eigGen.computeDemeanedImages()

    # Do PCA first to reduce the space so that computing LDA is tractable
    pcaEigenvectors, pcaEigenvalues, training, threshold, deletedIndices = eigGen.computeCovarianceEigens(demeanedImages)
    imgList = np.delete(imgList, deletedIndices)
    demeanedImages = np.delete(demeanedImages, deletedIndices, axis=1)

    # Project into the PCA space
    projected = np.dot(demeanedImages.T, pcaEigenvectors)

    # Compute new global mean
    projectedGlobalMean = projected.mean(0)

    # Classify eigenfaces according to which person they belong to
    classified = [None] * 15
    for idx in range(len(imgList)):
        # get the id of the person
        personId = int(re.search('[^\d]*(\d+)_\d+_.gif', imgList[idx]).group(1))

        # insert into the classification
        if classified[personId - 1] == None:
            classified[personId - 1] = []
        
        classified[personId - 1].append(projected[idx])

    # Do LDA in the PCA space
    ldaEigenvalues, ldaEigenvectors = lda(classified, projectedGlobalMean)

    fisherFaces = np.dot(pcaEigenvectors, ldaEigenvectors)
    for i in range(len(fisherFaces.T)):
        faceImage = fisherFaces.T[i]
        min = np.amin(faceImage)
        # scale up to 0
        faceImage = faceImage + abs(min)
        # map the max to 1
        max = np.amax(faceImage)
        faceImage = faceImage / max
        # scale all to 255
        faceImage = 255 * faceImage
        eigGen.printImage("ff_" + str(i), faceImage, 243, 320)
if __name__ == "__main__":
    main()
