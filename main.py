from __future__ import print_function
import sys, os
import time
import eigenfaceGenerator as eigGen
import dataHandler as dh
import projectFaceIntoEigenspace as eigProj

def main():
    startTime = time.time()
    # if the user specifies a generate, it reads through the faces
    # in ./img and and generates mean- and eigen- faces. These are
    # stored via pickle in the file "dataFile.dat"
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        excludeFile = ""

        if len(sys.argv) == 3:
            pathname = os.path.abspath(sys.argv[2])
            if os.path.isfile(pathname):
                excludeFile = sys.argv[2].replace("\\","/")
            else:
                print("Error: must pass valid file to exclude.\n", file=sys.stderr)
                return
        imgList, flatMean, demeanedImages = eigGen.computeDemeanedImages(excludeFile)
        eigenVectors, eigenValues, trainingDistances, threshold = eigGen.computeCovarianceEigens(demeanedImages)
        writeData = {"imgList":imgList,"flatMean":flatMean,"demeanedImages":demeanedImages,"eigenVectors":eigenVectors, "eigenValues":eigenValues, "trainingDistances":trainingDistances, "threshold":threshold}
        dh.writeData(writeData)

    # otherwise, read the generated data from dataFile.dat and
    # determine the best fit of the passed-in image
    elif len(sys.argv) == 2:
        pathname = os.path.abspath(sys.argv[1])
        if os.path.isfile(pathname):                
            readData = dh.readData()
            print(eigProj.trainingProjections(pathname, readData["imgList"], readData["eigenVectors"], readData["demeanedImages"], readData["flatMean"], readData["trainingDistances"], readData["threshold"]))
        else:
            print("Error: must pass valid file.\n", file=sys.stderr)

    else:
        print("Error: must pass the path to an image filename.", file=sys.stderr)
        print("Usage: python main.py blah.gif\n")

    print("time take: " + str(time.time() - startTime))

# added this method to ease unit testing
def test(imgPath):
	imgList, flatMean, demeanedImages = eigGen.computeDemeanedImages(imgPath)
	eigenVectors = eigGen.computeCovarianceEigens(demeanedImages)
	readData = {"imgList":imgList, "flatMean":flatMean, "demeanedImages":demeanedImages, "eigenVectors":eigenVectors}
	return eigProj.trainingProjections(imgPath, readData["imgList"], readData["eigenVectors"], readData["demeanedImages"], readData["flatMean"])

if __name__ == "__main__":
    main()
