import os, pickle

dataFile = "dataFile.dat"

def writeData(data):
    #pickle.dump(data, open(dataFile,"wb"))
    pickleData = pickle.dumps(data)
    print "PICKLED"
    os.environ["GHETTOPICKLE"] = 

def readPersonData(person):
    readback = pickle.load(open(dataFile,"rb"))
    return readback[person]

def readData():
    return pickle.loads(os.environ["GHETTOPICKLE"]) #pickle.load(open(dataFile,"rb"))
