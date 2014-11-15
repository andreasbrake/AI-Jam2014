from __future__ import print_function
import sys, os

def main():
	# user should pass one file relative to the current directory
	if len(sys.argv) == 2:
		pathname = os.path.abspath(sys.argv[1])
	
		if os.path.isfile(pathname):
			# TODO call our algorithm with path to calculate closest match
			print("path =", pathname)
		else:
			print("Error: must pass valid file.\n", file=sys.stderr)	
	else:
		print("Error: must pass the path to an image filename.", file=sys.stderr)
		print("Usage: python main.py blah.gif\n")

if __name__ == "__main__":
	main()

