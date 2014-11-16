import sys, os, time
import dataHandler as dh
import eigenfaceGenerator as eigGen

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
    eigenVectors, eigenValues, trainingDistances, threshold = eigGen.computeCovarianceEigens(demeanedImages)
    writeData = {"imgList":imgList,"flatMean":flatMean,"demeanedImages":demeanedImages,"eigenVectors":eigenVectors, "eigenValues":eigenValues, "trainingDistances":trainingDistances, "threshold":threshold}
    print "time to generate: " + str(time.time() - startTime)
    dh.writeData(writeData)
    print "time taken: " + str(time.time() - startTime)

if __name__ == "__main__":
    main()
