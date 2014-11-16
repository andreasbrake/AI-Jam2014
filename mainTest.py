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
			end = 9 if self.isNumber(imgName[7:9]) else 8

			expected = imgName[7:end]
			actual = main.test(imgName) # test each face from the data set

			if (expected == actual):
				print "PASS\n"
				numCorrect += 1
			else:
				print "FAIL\n"
				incorrect[imgName] = actual

			total += 1

		print "Incorrect images and their matches:"
		pprint.pprint(incorrect) 
		print "\nNumber correct: " + str(numCorrect) + " out of " + str(total)
		print "Percentage correct: " + str ((numCorrect/total) * 100) + "%\n"

	# helper to check for the number portion of filename
	def isNumber(self, s):
		try:
			float(s)
			return True
		except ValueError:
			return False

if __name__ == "__main__":
	TestRecognition().testFaces()
