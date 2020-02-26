# Implementation of the construction of a Damerau-Levenshtein Edit Distance Matrix
class DLMatrix:
    def addFirstRow(self):
        firstRow = []
        firstRow.append(0)
        for i in range(len(self._refWord)):
            firstRow.append(i + 1)
        self._DLArray.append(firstRow)

    def __init__(self, refWord):
        self._refWord = refWord
        self._DLArray = []
        self._charStack = []
        # Initialize DLArray's first row
        self.addFirstRow()

    def show(self):
        print(" \t", end=" ")
        for w in self._refWord:
            print(w, end=" ")
        print("")
        i = 0
        j = 0
        for i in range(len(self._charStack)):
            print(self._charStack[i] + " " + str(self._DLArray[i + 1][0]), end="  ")
            for j in range(len(self._refWord)):
                print(str(self._DLArray[i + 1][j + 1]), end=" ")
            print("")

    def insertChar(self, c):
        row = []

        if len(self._charStack) > 0:
            prevc = self._charStack[-1:]
        else:
            prevc = -1
        self._charStack.append(c)

        arrSize = len(self._DLArray)
        row.append(arrSize)
        i = arrSize
        j = 0
        for w in self._refWord:
            j += 1
            cost = 0
            if w != c:
                cost = 1

            diminus1j = self._DLArray[i - 1][j]
            dijminus1 = row[j - 1]
            diminus1jminus1 = self._DLArray[i - 1][j - 1]

            dij = min(diminus1j + 1,
                      dijminus1 + 1,
                      diminus1jminus1 + cost)

            if prevc != -1:
                idxj = j - 1
                if i > 1 and idxj > 1 and c == self._refWord[idxj - 1] and prevc == self._refWord[idxj]:
                    diminus2jminus2 = self._DLArray[i - 2][j - 2]
                    dij = min(dij, diminus2jminus2 + 1)
            row.append(dij)
        self._DLArray.append(row)

    def getEditDistForCharsSoFar(self):
        arrSize = len(self._DLArray)
        if arrSize > 0:
            cols = len(self._DLArray[0])
            if cols > 0:
                numCharsOnStack = len(self._charStack)
                idxi = numCharsOnStack
                idxj = min(numCharsOnStack, cols - 1)
                return self._DLArray[idxi][idxj]
        return 0

    def getEditDistForWord(self):
        arrSize = len(self._DLArray)
        if arrSize > 1:
            cols = len(self._DLArray[arrSize - 1])
            if cols >= 1:
                return self._DLArray[arrSize - 1][cols - 1]
        return 0

    def popChar(self):
        self._DLArray.pop()
        self._charStack.pop()

    def test(self, word1, word2):
        tmpArray = []
        tmpRefWord = self._refWord
        tmpCharStack = self._charStack.copy()

        for i in range(len(self._DLArray)):
            tmpArray.append((self._DLArray[i]).copy())

        self._DLArray.clear()
        self._refWord = word1
        self.addFirstRow()

        for s in word2:
            self.insertChar(s)

        self.show()
        print("Edit distance: " + str(self.getEditDist()))
