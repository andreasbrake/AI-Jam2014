import sys, os, time
import numpy as np
import dataHandler as dh
import eigenfaceGenerator as eigGen
import fisherFaces as ff

def main():
    startTime = time.time()
    # if the user specifies a generate, it reads through the faces
    # in ./img and and generates mean- and eigen- faces. These are
    # stored via pickle in the file "dataFile.dat"

    excludeFile = ""
    if len(sys.argv) == 2:
        pathname = os.path.abspath(sys.argv[1])
        if os.path.isfile(pathname):
            excludeFile = sys.argv[1].replace("\\","/")
        else:
            print("Error: must pass valid file to exclude")
            return
    imgList, flatMean, demeanedImages = eigGen.computeDemeanedImages(excludeFile)
    pcaEigenvectors, pcaEigenvalues, deletedIndices = eigGen.computeCovarianceEigens(demeanedImages)

    imgList = np.delete(imgList, deletedIndices)
    demeanedImages = np.delete(demeanedImages, deletedIndices, axis=1)

    fisherFaces, trainingDistances, threshold = ff.generateFisherFaces(pcaEigenvectors, imgList, demeanedImages)
    writeData = {"imgList":imgList,"flatMean":flatMean,"demeanedImages":demeanedImages,"fisherFaces":fisherFaces, "trainingDistances":trainingDistances, "threshold":threshold}
    
    print "time to generate: " + str(time.time() - startTime)
    dh.writeData(writeData)
    print "time taken: " + str(time.time() - startTime)

if __name__ == "__main__":
    main()
