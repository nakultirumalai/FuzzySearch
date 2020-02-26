import time

from keyValStore import keyValueStore
from kvUtils import kvUtils


def localTest():
    kvStore = keyValueStore()
    kvStore.setNumResults(25)
    kvStore.insertKey("abc", 1000)
    kvStore.insertKey("bca", 2000)
    kvStore.insertKey("abcd", 201)

    keyList = []
    kvStore.findKeys("a", keyList)
    print("Keys returned for a:")
    print(keyList)
    keyList = []
    kvStore.findKeys("b", keyList)
    print("Keys returned for b:")
    print(keyList)
    keyList = []
    kvStore.findKeys("bc", keyList)
    print("Keys returned for bc:")
    print(keyList)
    keyList = []
    kvStore.findKeys("abc", keyList)
    print("Keys returned for abc:")
    print(keyList)


def queryAndPrintStats(key, kvStore):
    keyList = []
    start_time = time.time()
    kvStore.findKeys(key, keyList)
    end_time = time.time()
    queryTimeStr = kvUtils.getTimeAsString(start_time, end_time)
    allKeys = ", ".join(map(str, keyList))
    if len(keyList) != 0:
        print("QUERY: " + key + "\t" + queryTimeStr + "\t" + str(len(keyList)) + "\t" + allKeys)
    else:
        print("QUERY: " + key + "\t" + queryTimeStr + "\t" + "No keys")


kvStore = keyValueStore()
start_time = time.time()
kvStore.readTsvFile("word_search.tsv")
end_time = time.time()
print("Time taken to read csv file: " + kvUtils.getTimeAsString(start_time, end_time))

queryAndPrintStats("g", kvStore)
queryAndPrintStats("ga", kvStore)
queryAndPrintStats("gar", kvStore)
queryAndPrintStats("gara", kvStore)
queryAndPrintStats("garag", kvStore)
queryAndPrintStats("garage", kvStore)

queryAndPrintStats("i", kvStore)
queryAndPrintStats("id", kvStore)
queryAndPrintStats("idi", kvStore)
queryAndPrintStats("idio", kvStore)

queryAndPrintStats("p", kvStore)
queryAndPrintStats("pa", kvStore)
queryAndPrintStats("par", kvStore)
queryAndPrintStats("para", kvStore)

queryAndPrintStats("e", kvStore)
queryAndPrintStats("er", kvStore)
queryAndPrintStats("ery", kvStore)
queryAndPrintStats("eryx", kvStore)

queryAndPrintStats("p", kvStore)
queryAndPrintStats("pa", kvStore)
queryAndPrintStats("pat", kvStore)
queryAndPrintStats("path", kvStore)
queryAndPrintStats("pathe", kvStore)
queryAndPrintStats("pathet", kvStore)
queryAndPrintStats("pathetc", kvStore)
queryAndPrintStats("pathect", kvStore)
queryAndPrintStats("pathecti", kvStore)
queryAndPrintStats("patheti", kvStore)
queryAndPrintStats("pathetic", kvStore)

queryAndPrintStats("g", kvStore)
queryAndPrintStats("gr", kvStore)
queryAndPrintStats("grt", kvStore)
queryAndPrintStats("grtn", kvStore)
queryAndPrintStats("grtne", kvStore)
queryAndPrintStats("grtnes", kvStore)
queryAndPrintStats("grtness", kvStore)
queryAndPrintStats("graetness", kvStore)

queryAndPrintStats("n", kvStore)
queryAndPrintStats("ne", kvStore)
queryAndPrintStats("nes", kvStore)
queryAndPrintStats("ness", kvStore)
