# --------------------------------------------------------------------- #
#  Implementation of a string key and integer value store for fast
#  lookup, prefix lookup, fuzzy match lookup and substring lookup using
#  ternary search trees (for space efficiency). API overview:
#     - insertKey: Insert a key with an integer value
#     - searchWord: Look for a k
# --------------------------------------------------------------------- #
import time

from BYSubString import BoyerMooreMatch
from DLMatrix import DLMatrix
from tstNode import tstNode


# --------------------------------------------------------------------- #
#  Ternary search tree implementation of the dictionary
# --------------------------------------------------------------------- #
class keyDict:
    # Constructor
    def __init__(self):
        self._root = None
        self._wordsWithChars = {}

    # Utility functions
    # Get the node corresponding to char c from the given node
    def findFirstNodeFromTop(self, node, c):
        rNode = None
        if node is None:
            return rNode
        if node.getChar() == c:
            rNode = node
        elif node.getChar() < c:
            rNode = self.findFirstNodeFromTop(node.getRightNode(), c)
        elif node.getChar() > c:
            rNode = self.findFirstNodeFromTop(node.getLeftNode(), c)
        return rNode

    def addToWordsWithCharsDict(self, substr, key, val):
        if self._wordsWithChars.get(substr) is None:
            tmp = []
            self._wordsWithChars[substr] = tmp
        (self._wordsWithChars[substr]).append([key, val])

    def sortWordsWithCharsDict(self):
        for key in self._wordsWithChars:
            tmp = self._wordsWithChars[key]
            sorted(tmp, key=lambda tmp: tmp[1])

    # Given a leaf node, get the word corresponding to the leaf node
    # by going up the tree
    def getWord(self, node):
        if node is None:
            return
        word = node.getChar()
        prevNode = node
        parentNode = node.getParentNode()
        while parentNode is not None:
            parentChar = parentNode.getChar()
            if parentNode.getDownNode() == prevNode:
                word = parentChar + word
            prevNode = parentNode
            parentNode = parentNode.getParentNode()
        return word

    # Collect all the keys from a TST node's subtree, node inclusive recursively
    def collectAllKeysInSubTree(self, node, numWords, nodeList):
        if node is None:
            return
        if len(nodeList) == numWords:
            return
        if node.getLeftNode() is not None:
            self.collectAllKeysInSubTree(node.getLeftNode(), numWords, nodeList)
        if node.hasWord():
            nodeList.append(node)
        if node.getDownNode() is not None:
            self.collectAllKeysInSubTree(node.getDownNode(), numWords, nodeList)
        if node.getRightNode() is not None:
            self.collectAllKeysInSubTree(node.getRightNode(), numWords, nodeList)

    # Recursively insert a key into the dictionary's TST
    def recursiveInsert(self, node, key, val, keyLen, idx):
        leafNode = None
        if node is None:
            node = tstNode(key[idx])

        w = key[idx];
        if w < node.getChar():
            rNode, leafNode = self.recursiveInsert(node.getLeftNode(), key, val, keyLen, idx)
            node.setLeftNode(rNode)
            rNode.setParentNode(node)
        elif w > node.getChar():
            rNode, leafNode = self.recursiveInsert(node.getRightNode(), key, val, keyLen, idx)
            node.setRightNode(rNode)
            rNode.setParentNode(node)
        elif idx < keyLen - 1:
            if keyLen > 2 and idx > 1:
                prevChar = key[idx - 1]
                substr = prevChar + key[idx]
                self.addToWordsWithCharsDict(substr, key, val)
                if keyLen > 3 and idx > 2:
                    prev2Char = key[idx - 2]
                    substr = prev2Char + prevChar + key[idx]
                    self.addToWordsWithCharsDict(substr, key, val)

            rNode, leafNode = self.recursiveInsert(node.getDownNode(), key, val, keyLen, idx + 1)
            node.setDownNode(rNode)
            rNode.setParentNode(node)
        else:
            node.setValue(val)
            node.markHasWord()
            node.setWordLength(keyLen)

            leafNode = node
        return node, leafNode

    # Recursively search for an exact matching key in the TST
    def recursiveSearch(self, node, key, keyLen, idx):
        if node is None:
            return None

        c = node.getChar()
        if c > key[idx]:
            return self.recursiveSearch(node.getLeftNode(), key, keyLen, idx)
        elif c < key[idx]:
            return self.recursiveSearch(node.getRightNode(), key, keyLen, idx)
        elif idx < keyLen - 1:
            return self.recursiveSearch(node.getDownNode(), key, keyLen, (idx + 1))
        else:
            return node

    # Recursively search all the keys with a prefix and return a list of nodes
    # on the TST which correspond to those keys
    def recursiveSearchAllKeysWithPrefix(self, node, prefix, prefixLen, idx, numWords, nodeList):
        if node is None:
            return
        c = node.getChar()
        if c < prefix[idx]:
            self.recursiveSearchAllKeysWithPrefix(node.getRightNode(), prefix, prefixLen, idx, numWords, nodeList)
        elif c > prefix[idx]:
            self.recursiveSearchAllKeysWithPrefix(node.getLeftNode(), prefix, prefixLen, idx, numWords, nodeList)
        elif idx < prefixLen - 1:
            self.recursiveSearchAllKeysWithPrefix(node.getDownNode(), prefix, prefixLen, idx + 1, numWords, nodeList)
        else:
            if node.hasWord() is True:
                nodeList.append(node)
                if len(nodeList) == numWords:
                    return
            self.collectAllKeysInSubTree(node.getDownNode(), numWords, nodeList)

    # Recursively search all the keys using a fuzzy search by considering True Damerau Levenshtein
    # edit distances on the TST which correspond to those keys
    # Build the edit distances as the TST is traversed
    def recursiveSearchFuzzy(self, node, editDist, thisDLMat, nodeList, strSoFar):
        if node is None:
            return
        # Process stuff for left sub-tree
        leftNode = node.getLeftNode()
        if leftNode is not None:
            self.recursiveSearchFuzzy(leftNode, editDist, thisDLMat, nodeList, strSoFar)

        # Process stuff sub-tree under the current node
        nodeChar = node.getChar()
        strSoFar = strSoFar + nodeChar
        thisDLMat.insertChar(nodeChar)
        if node.hasWord() is True:
            editDistForWord = thisDLMat.getEditDistForWord()
            if editDistForWord > 0 and editDistForWord <= editDist:
                nodeList.append([node, editDistForWord])
        editDistAfterAddingChar = thisDLMat.getEditDistForCharsSoFar()
        downNode = node.getDownNode()
        if editDistAfterAddingChar <= editDist and downNode is not None:
            self.recursiveSearchFuzzy(downNode, editDist, thisDLMat, nodeList, strSoFar)
        thisDLMat.popChar()
        strSoFar = strSoFar[:-1]

        # Process stuff for right sub-tree
        rightNode = node.getRightNode()
        if rightNode is not None:
            self.recursiveSearchFuzzy(rightNode, editDist, thisDLMat, nodeList, strSoFar)

    # Insert a key into the dictionary's TST
    def insertKey(self, key, val):
        # insertion is never unsuccessful as we create nodes
        self._root, leafNode = self.recursiveInsert(self._root, key, int(val), len(key), 0)

    # Search if a key exists in the TST and return the integer value
    # of the key if it exists along with a result which indicates if the
    # key has been found in the TST
    def searchKey(self, key):
        result = False
        val = 0
        if self._root is None:
            return result, val

        node = self.recursiveSearch(self._root, key, len(key), 0)

        if node is not None and node.hasWord() is True:
            val = node.getValue()
            result = True

        return result, val

    # Search for keys with "prefix" in the TST and return them in a list
    def searchAllKeysWithPrefix(self, prefix, keyList, numWords, visitedKeys):
        nodeList = []
        # Pass numWords + 1 in case the prefix has a word already in the TST
        self.recursiveSearchAllKeysWithPrefix(self._root, prefix, len(prefix), 0, (numWords + 1), nodeList)

        numInserted = 0
        for node in nodeList:
            key = self.getWord(node)
            if visitedKeys.get(key) is None:
                val = node.getValue()
                keyList.append([key, val])
                visitedKeys[key] = True
                numInserted += 1
                if numInserted == numWords:
                    break

    # Returns a list of keys whose edit distance according to True Damerau-Levenshtein is within
    # "editDist"; Keep max edit distance as 2
    def searchKeyFuzzy(self, key, maxEditDist, numWords, keyList, visitedKeys):
        if self._root is None:
            return
        if numWords == 0:
            return
        if len(key) < 2:
            return

        thisDLMatrix = DLMatrix(key)
        beginNode = self.findFirstNodeFromTop(self._root, key[0])
        thisDLMatrix.insertChar(beginNode.getChar())
        strSoFar = beginNode.getChar()

        nodeList = []
        start_time = time.time()
        self.recursiveSearchFuzzy(beginNode.getDownNode(), maxEditDist, thisDLMatrix, nodeList, strSoFar)
        end_time = time.time()
        # print("Time taken for recursive fuzzy search only: ", kvUtils.getTimeAsString(start_time, end_time))
        editDist1 = []
        editDist2 = []
        for i in range(len(nodeList)):
            node = nodeList[i][0]
            editDist = nodeList[i][1]
            if editDist == 1:
                editDist1.append([node, node.getValue()])
            elif editDist == 2:
                editDist2.append([node, node.getValue()])
            if len(editDist1) == 25:
                break

        lenEditDist1 = len(editDist1)
        lenEditDist2 = len(editDist2)
        if lenEditDist1 > 0:
            sorted(editDist1, key=lambda editDist1: editDist1[1])
        if lenEditDist1 < numWords and lenEditDist2 > 0:
            sorted(editDist2, key=lambda editDist2: editDist2[1])
            for i in range(min(numWords - lenEditDist1, lenEditDist2)):
                editDist1.append(editDist2[i])
        lenEditDist1 = len(editDist1)
        for i in range(lenEditDist1):
            [node, val] = editDist1[i]
            key = self.getWord(node)
            if visitedKeys.get(key) is None:
                visitedKeys[key] = True
                keyList.append([key, val])
                if i == numWords:
                    break

    def searchSubstringKeys(self, pattern, keyList, numWords, visitedKeys):
        # Pop keys from the priority queue and run the Boyer
        patternLen = len(pattern)
        if patternLen == 1 or patternLen == 0:
            return

        begin2Chars = pattern[0:2]
        keysWithSubstrList = []
        if (patternLen == 2):
            keysWithSubstrList = self._wordsWithChars.get(begin2Chars)
        else:
            begin3Chars = pattern[0:3]
            keysWithSubstrList = self._wordsWithChars.get(begin3Chars)

        if keysWithSubstrList is None:
            return

        byMatch = BoyerMooreMatch(pattern)
        patternLen = len(pattern)
        numAddedWords = 0
        for i in range(len(keysWithSubstrList)):
            keyValPair = keysWithSubstrList[i]
            key = keyValPair[0]
            if len(key) < patternLen:
                continue

            val = keyValPair[1]
            if visitedKeys.get(key) is not None:
                continue
            if byMatch.matches(key):
                keyList.append([key, val])
                visitedKeys[key] = True
                numAddedWords += 1
                if numAddedWords == numWords:
                    break

    # TST display functions
    def visit(self, curNode):
        if curNode is None:
            return
        else:
            print(curNode.getChar() + " " + str(hex(id(curNode))) + " " + str(curNode.hasWord()) + " " + str(
                curNode.getNumWords()))

    def traverseTst(self, node):
        if node is None:
            return
        else:
            self.visit(node)
            self.traverseTst(node.getLeftNode())
            self.traverseTst(node.getDownNode())
            self.traverseTst(node.getRightNode())

    def printTst(self):
        if self._root is None:
            return
        else:
            self.traverseTst(self._root)
