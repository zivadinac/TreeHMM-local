import pickle as __pickle

def saveTrainedHMM(out_path, hmmTrainResults):
    with open(out_path, "wb") as fitFile:
        __pickle.dump(hmmTrainResults, fitFile, protocol=4)

def loadTrainedHMM(file_path, as_object=True):
    with open(file_path, "rb") as file_file:
        hmm = __pickle.load(file_file)
    return hmm
