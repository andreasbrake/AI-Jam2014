from __future__ import print_function
import sys, os, time
import numpy as np
import eigenfaceGenerator as eigGen
import dataHandler as dh
import projectFaceIntoEigenspace as eigProj

def main():
    startTime = time.time()
    # Read the generated data from dataFile.dat and
    # determine the best fit of the passed-in image
    if len(sys.argv) == 2:
        pathname = os.path.abspath(sys.argv[1])
        if os.path.isfile(pathname):                
            readData = dh.readData()
            #print("time to read: " + str(time.time() - startTime))
            print(eigProj.trainingProjections(pathname, readData["imgList"], readData["eigenVectors"], readData["demeanedImages"], readData["flatMean"], readData["trainingDistances"], readData["threshold"])[0])
        else:
            print("Error: must pass valid file.\n", file=sys.stderr)

    else:
        print("Error: must pass the path to an image filename.", file=sys.stderr)
        print("Usage: python main.py blah.gif\n")

    #print("time take: " + str(time.time() - startTime))

# added this method to ease unit testing
def test(imgPath):
    imgList, flatMean, demeanedImages = eigGen.computeDemeanedImages(imgPath)
    pcaEigenVectors, pcaEigenValues, deletedIndices, demeanedImages, trainingDistances, threshold = eigGen.computeCovarianceEigens(demeanedImages)

    imgList = np.delete(imgList, deletedIndices)

    readData = {"imgList":imgList,"flatMean":flatMean,"demeanedImages":demeanedImages,"eigenVectors":pcaEigenVectors, "trainingDistances":trainingDistances, "threshold":threshold}
    #readData = dh.readData()
    print("thresh: " + str(threshold * 0.75))
    return eigProj.trainingProjections(imgPath, readData["imgList"], readData["eigenVectors"], readData["demeanedImages"], readData["flatMean"], readData["trainingDistances"], readData["threshold"])

if __name__ == "__main__":
    main()
