import re
import numpy as np

# calculate the eigenvalues/eigenvectors/Sb/Sw
def lda(X, globalMu):
    projectionLength = X[0][0].shape[1]
    Sb = np.zeros((projectionLength, projectionLength))
    Sw = np.zeros((projectionLength, projectionLength))

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

def generateFisherFaces(pcaEigenvectors, imgList, demeanedImages):
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

    # determine the distances between all training images
    trainingDistances = []
    fisherFacesTranspose = fisherFaces.T
    demeanedImagesTranspose = demeanedImages.T

    for i in range(len(demeanedImagesTranspose)):
        trainingDistances.append(fisherFacesTranspose * demeanedImagesTranspose[i,:].T)

    # Compute the threshold
    threshold = 1
    for i in range(len(trainingDistances)):
        for k in range(i, len(trainingDistances)):
            curDist = np.linalg.norm(trainingDistances[i] - trainingDistances[k])
            if curDist > threshold:
                threshold = curDist

    # Half the max as per powerpoint slideshow from the internet
    threshold /= 2
    
    return fisherFaces, trainingDistances, threshold
if __name__ == "__main__":
    main()
