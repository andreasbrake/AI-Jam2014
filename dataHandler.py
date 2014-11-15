import pickle

dataFile = "dataFile.dat"

def writeData(data):
    pickle.dump(data, open(dataFile,"wb"))

def readPersonData(person):
    readback = pickle.load(open(dataFile,"rb"))
    return readback[person]

def readData():
    return pickle.load(open(dataFile,"rb"))
