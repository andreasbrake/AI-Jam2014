import os, glob
import numpy as np
import dataHandler as db
from PIL import Image

# function to calculate the projections of the training images and and the test image
# in the face space (eigen faces)
def trainingProjections(testImage, faceSpace, trainingSpace):
    print trainingSpace