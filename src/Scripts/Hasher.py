import os
import json
import hashlib
import __main__
from Scripts.BasicLogger import Log
import Scripts.GlobalVariables as GVars

def GetFiles(path):
    fileList = []
    # goes through all the files in the directory and saves their full name in fileList
    for root, files in os.walk(path):
        for file in files:
            fileList.append(os.path.join(root, file))

    return fileList


def GetHash(file):
    hasher = hashlib.md5()

    # opens the file for reading in binary mode
    with open(file, 'rb') as f:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = f.read(1024)
            hasher.update(chunk)

    return hasher.hexdigest()


def SaveFilesData():
    # if the files structure ever changed just change this line
    modFilesPath = "src"+GVars.nf+"ModFiles" + GVars.nf+"Portal 2"+GVars.nf+"install_dlc" # relative mod path
    # and keep the rest as is
    path = os.path.dirname(__main__.__file__) +GVars.nf+ modFilesPath # absolute mod path
    savePath = os.path.dirname(__main__.__file__) + GVars.nf + "modFilesData.json" # where to save the files data
    
    fileList = GetFiles(path)
    Log("got all Files data")
    Log("serializing Data")
    jsn = []
    for i in range(len(fileList)):
        jsn.append({"name": fileList[i].replace(path, "").replace(GVars.nf, "/"), # the second replace is only needed for windows but whatever
                    "hash": GetHash(fileList[i])})

    Log("writing to file")
    jsonStr = json.dumps(jsn)
    open(savePath, "w").write(jsonStr)

    Log("saved Files Data in: " + savePath)
    return savePath
