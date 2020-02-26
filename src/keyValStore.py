import time

from keyDict import keyDict


# --------------------------------------------------------------------- #
#  Custom value function for returning the time for instrumentation
# --------------------------------------------------------------------- #
def getTimeAsString(start_time, end_time):
    total_time = end_time - start_time;
    suffix = "s"
    if total_time < 1:
        total_time = total_time * 1000
        suffix = "ms"
    timeStr = str(total_time) + suffix
    return timeStr


# --------------------------------------------------------------------- #
#  Top level API for the string key and integer value store
# --------------------------------------------------------------------- #
class keyValueStore:
    def __init__(self):
        self._keyDict = keyDict()
        self._numResults = 25

    def setNumResults(self, numResults):
        self._numResults = numResults

    def insertKey(self, key, value):
        self._keyDict.insertKey(key, value)

    def findKeys(self, key, keyList):
        visitedKeys = {}
        numWords = self._numResults
        # First, find the exact match of the key
        result, val = self._keyDict.searchKey(key)
        if result is True:
            visitedKeys[key] = True
            keyList.append([key, val])
            numWords -= 1

        # If the keyList is empty, query all keys which
        # have the prefix as key
        start_time = time.time()
        self._keyDict.searchAllKeysWithPrefix(key, keyList, numWords, visitedKeys)
        end_time = time.time()
        # print(" Total time for prefix search of \"" + key + "\" is :" + kvUtils.getTimeAsString(start_time, end_time))

        # If the number of keys gathered is less than numWords, perform
        # a fuzzy search
        if len(keyList) < numWords:
            start_time = time.time()
            self._keyDict.searchKeyFuzzy(key, 2, numWords - len(keyList), keyList, visitedKeys)
            end_time = time.time()
            # print(" Total time for fuzzy search of \"" + key + "\" is :" + kvUtils.getTimeAsString(start_time, end_time))

        if len(keyList) < numWords:
            start_time = time.time()
            self._keyDict.searchSubstringKeys(key, keyList, numWords - len(keyList), visitedKeys)
            end_time = time.time()
            # print(" Total time for substring search of \"" + key + "\" is :" + kvUtils.getTimeAsString(start_time, end_time))

    def readTsvFile(self, filename):
        print("Reading: " + filename + " ...")
        f = None
        try:
            f = open(filename, "r")
        except IOError:
            print("Cannot open filename: " + filename)
            return
        for line in f:
            cols = line.split('\t')
            if len(cols) < 2:
                continue
            self._keyDict.insertKey(cols[0], cols[1])
        f.close()

        self._keyDict.sortWordsWithCharsDict()

        return
