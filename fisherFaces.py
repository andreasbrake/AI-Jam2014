import glob
from PIL import Image
import numpy as np
import eigenfaceGenerator as eigGen

def lda(X):
    print "Mozzletoff"

# calculate the eigenvalues/eigenvectors/Sb/Sw
def createClass(i):
    images = []

    # Open images and return them
    for image in glob.glob("./img/" + str(i) + "_*_.gif"):
        currentImage = np.array(Image.open(image), dtype=np.float)
        currentImage = np.resize(currentImage, (1, 77760))
        images.append(currentImage)
    # return

    return images

def main():
    # Compute demeanedImages
    imgList, flatMean, demeanedImages = eigGen.computeDemeanedImages()

    # Do PCA first to reduce the space so that computing LDA is tractable
    pcaEigenvectors, pcaEigenvalues = eigGen.computeCovarianceEigens(demeanedImages)

    # Project into the PCA space
    projected = np.dot(pcaEigenvectors, demeanedImages)

    print projected.shape

    # Compute new global mean
    globalMean = projected.mean(0)

    # Classify eigenfaces according to which person they belong to
    classified = [None] * 15
    for i in imgList:
        # get the id of the person
        personId = re.search('[^\d]*(\d+)_\d+_.gif', imgList[idx]).group(1)

        # insert into the classification
        if classified[personId] == None:
            classified[personId] = []
        
        classified[personId].append(projected[i])

    # Do LDA in the PCA space
    ldaEigenvalues, ldaEigenvectors = lda(classified)

if __name__ == "__main__":
    main()
