import main # code under test
import glob
import dataHandler as dh
import pprint

# testing output from our algorithm to determine improvements or regressions
class TestRecognition():

	# go through the images and find expected output
	def testFaces(self):

		numCorrect = 0 
		total = 0 # should be 120
		incorrect = {}
		for imgName in glob.glob("./img/*_*_.gif"):
			
			# determine the slicing based on file name
			end = 8 if self.isNumber(imgName[6:8]) else 7

			expected = imgName[6:end]
			actual = main.test(imgName) # test each face from the data set

			if (expected == actual):
				print "PASS\n"
				numCorrect += 1
			else:
				print "FAIL\n"
				incorrect[imgName] = actual

			total += 1

		print "Number correct out of " + total + " = " numCorrect + "\n"
		print "Incorrect images and their matches:"
		pprint(incorrect) 

	# helper to check for the number portion of filename
	def isNumber(self, s):
		try:
			float(s)
			return True
		except ValueError:
			return False

if __name__ == "__main__":
	TestRecognition().testFaces()
