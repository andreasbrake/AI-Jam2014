#im = Image.open("./img/1_2_.gif")

#im.save("./img/testOut.gif", "GIF")

import os, numpy, PIL
from PIL import Image

# Access all PNG files in directory

def getMeanOf(imgId):
    allfiles=os.listdir(os.getcwd() + "\\img\\")
    imlist=[]
    for filename in allfiles:
        if filename[-4:] in [".gif",".GIF"] and filename[:len(imgId)] == imgId:
            imlist.append("./img/" + filename)

    # Assuming all images are the same size, get dimensions of first image
    w,h=Image.open(imlist[0]).size
    N=len(imlist)

    # Create a numpy array of floats to store the average (assume RGB images)
    arr=numpy.zeros((h,w),numpy.float)

    # Build up average pixel intensities, casting each image as an array of floats
    for im in imlist:
        imarr=numpy.array(Image.open(im),dtype=numpy.float)
        arr=arr+imarr/N

    # Round values in array and cast as 8-bit integer
    arr=numpy.array(numpy.round(arr),dtype=numpy.uint8)

    # Generate, save and preview final image
    out=Image.fromarray(arr)
    print "creating mean at: " + "./img/" + imgId + "Mean.gif"
    out.save("./img/" + imgId + "Mean.gif","GIF")


for i in range(1,16):
    getMeanOf(str(i) + "_")
