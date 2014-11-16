from __future__ import print_function
import sys, os
import eigenfaceGenerator as eigGen
import projectFaceIntoEigenspace as eigProj

def main():
	# user should pass one file relative to the current directory
	if len(sys.argv) == 2:
		pathname = os.path.abspath(sys.argv[1])
	
		if os.path.isfile(pathname):
			# TODO call our algorithm with path to calculate closest match
			#print("path =", pathname)
		    imgList, flatMean, demeanedImages = eigGen.computeDemeanedImages()
		    eigenValues, eigenVectors = eigGen.computeCovarianceEigens(demeanedImages)

		    print(eigProj.trainingProjections(pathname, imgList, eigenVectors, demeanedImages, flatMean))
		else:
			print("Error: must pass valid file.\n", file=sys.stderr)	
	else:
		print("Error: must pass the path to an image filename.", file=sys.stderr)
		print("Usage: python main.py blah.gif\n")

if __name__ == "__main__":
	main()
