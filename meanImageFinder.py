import os, numpy, PIL, time
from PIL import Image

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
    origArrays = []
    bigArray = []

    for im in imlist:
        imarr=numpy.array(Image.open(im),dtype=numpy.float)
        arr=arr+imarr/N
        imarr = numpy.resize(imarr, (1, 77760))

        if len(bigArray) == 0:
            bigArray = imarr
        else:
            bigArray = numpy.append(bigArray, imarr, axis=0)

        origArrays.append(imarr)

    bigArray = numpy.array(numpy.round(bigArray),dtype=numpy.uint8)
    arr=numpy.array(numpy.round(arr),dtype=numpy.uint8)
    
    flatMean = numpy.resize(arr, (1, 77760))

    for i in range(0, len(bigArray)):
        bigArray[i] = bigArray[i] - flatMean

    bigArray = bigArray.T

    print numpy.cov(bigArray)

    # Generate, save and preview final image
    out=Image.fromarray(arr)

    #print "creating mean at: " + "./img/" + imgId + "Mean.gif"
    out.save("./img/" + imgId + "Mean.gif","GIF")


for i in range(1,2):
    getMeanOf(str(i) + "_")
