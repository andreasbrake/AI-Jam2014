import os, pickle

dataFile = "dataFile.dat"

def writeData(data):
    pickle.dump(data, open(dataFile,"wb"))
    #pickleData = pickle.dumps(data)
    #print "PICKLED"
    #strByte = list(bytearray(pickleData))
    #print strByte

    os.environ["GHETTOPICKLE"] = "TEST"

def readPersonData(person):
    readback = pickle.load(open(dataFile,"rb"))
    return readback[person]

def readData():
    return pickle.load(open(dataFile,"rb"))
    #return pickle.loads(os.environ["GHETTOPICKLE"])
