from __future__ import print_function
import sys, os
import eigenfaceGenerator as eigGen
import dataHandler as dh
import projectFaceIntoEigenspace as eigProj

def main():
    # user should pass one file relative to the current directory
    if len(sys.argv) == 2:
        # if the user specifies a generate, it reads through the faces
        # in ./img and and generates mean- and eigen- faces. These are
        # stored via pickle in the file "dataFile.dat"
        if sys.argv[1] == "generate":
            imgList, flatMean, demeanedImages = eigGen.computeDemeanedImages()
            eigenVectors = eigGen.computeCovarianceEigens(demeanedImages)
            writeData = {"imgList":imgList,"flatMean":flatMean,"demeanedImages":demeanedImages,"eigenVectors":eigenVectors}
            dh.writeData(writeData)
        # otherwise, read the generated data from dataFile.dat and
        # determine the best fit of the passed-in image
        else:
            pathname = os.path.abspath(sys.argv[1])
            if os.path.isfile(pathname):                
                readData = dh.readData()
                print(eigProj.trainingProjections(pathname, readData["imgList"], readData["eigenVectors"], readData["demeanedImages"], readData["flatMean"]))
            else:
                print("Error: must pass valid file.\n", file=sys.stderr)	
    else:
        print("Error: must pass the path to an image filename.", file=sys.stderr)
        print("Usage: python main.py blah.gif\n")

if __name__ == "__main__":
    main()
