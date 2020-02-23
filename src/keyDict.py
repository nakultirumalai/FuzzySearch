# --------------------------------------------------------------------- #
#  Implementation of a string key and integer value store for fast
#  lookup, prefix lookup, fuzzy match lookup and substring lookup using
#  ternary search trees (for space efficiency). API overview:
#     - insertKey: Insert a key with an integer value
#     - searchWord: Look for a k
# --------------------------------------------------------------------- #
from queue import PriorityQueue

from BYSubString import BoyerMooreMatch
from DLMatrix import DLMatrix


# --------------------------------------------------------------------- #
#  Class for objects on the ternary search tree
# --------------------------------------------------------------------- #
class tstNode:
    _char = 0
    _val = 0
    _linkParent = None
    _linkLeft = None
    _linkRight = None
    _linkDown = None
    _hasWord = False
    _wordLength = 0

    # Constructor
    def __init__(self, nodeChar, numWords=0, maxWordLength=0):
        self._char = nodeChar
        self._numWords = numWords
        self._maxWordLength = maxWordLength

    # Set the value of the word at this node
    def setValue(self, val):
        self._val = val

    def setWordLength(self, wordLength):
        self._wordLength = wordLength

    # Marking that the node has a key word associated
    def markHasWord(self):
        self._hasWord = True

    # Set the down node of the current node
    def setDownNode(self, node):
        self._linkDown = node

    # Set the left node of the current node
    def setLeftNode(self, node):
        self._linkLeft = node

    # Set the right node of the current node
    def setRightNode(self, node):
        self._linkRight = node

    # Set the parent node of the current node
    def setParentNode(self, node):
        self._linkParent = node

    # ------------- Get functions ----------------- #
    def getDownNode(self):
        return self._linkDown

    def getLeftNode(self):
        return self._linkLeft

    def getRightNode(self):
        return self._linkRight

    def getParentNode(self):
        return self._linkParent

    def getValue(self):
        return self._val

    def getWordLength(self):
        return self._wordLength

    def getChar(self):
        return self._char

    def hasWord(self):
        return self._hasWord


# --------------------------------------------------------------------- #
#  Ternary search tree implementation of the dictionary
# --------------------------------------------------------------------- #
class keyDict:
    _root = None

    # Constructor
    def __init__(self):
        _priorityQueue = PriorityQueue()

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
    def collectAllKeysInSubTree(self, node, nodeList):
        if node is None:
            return
        if node.hasWord():
            nodeList.append(node)
        if node.getLeftNode() is not None:
            self.collectAllKeysInSubTree(node.getLeftNode(), nodeList)
        if node.getDownNode() is not None:
            self.collectAllKeysInSubTree(node.getDownNode(), nodeList)
        if node.getRightNode() is not None:
            self.collectAllKeysInSubTree(node.getRightNode(), nodeList)

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
        elif idx < key - 1:
            return self.recursiveSearch(node.getDownNode(), key, keyLen, (idx + 1))
        else:
            return node

    # Recursively search all the keys with a prefix and return a list of nodes
    # on the TST which correspond to those keys
    def recursiveSearchAllKeysWithPrefix(self, node, prefix, prefixLen, idx, nodeList):
        if node is None:
            return
        c = node.getChar()
        if c < prefix[idx]:
            self.recursiveSearchAllKeysWithPrefix(node.getRightNode(), prefix, prefixLen, idx, nodeList)
        elif c > prefix[idx]:
            self.recursiveSearchAllKeysWithPrefix(node.getLeftNode(), prefix, prefixLen, idx, nodeList)
        elif idx < prefixLen - 1:
            self.recursiveSearchAllKeysWithPrefix(node.getDownNode(), prefix, prefixLen, idx + 1, nodeList)
        else:
            self.collectAllWordsInSubTree(node, prefix, prefixLen, idx + 1, nodeList)

    # Recursively search all the keys using a fuzzy search by considering True Damerau Levenshtein
    # edit distances on the TST which correspond to those keys
    # Build the edit distances as the TST is traversed
    def recursiveSearchFuzzy(self, node, editDist, thisDLMat, keyList, strSoFar):
        if node is None:
            return
        # Process stuff for left sub-tree
        leftNode = node.getLeftNode()
        if leftNode is not None:
            self.recursiveSearchFuzzy(node.getLeftNode(), editDist, thisDLMat, keyList, strSoFar)

        # Process stuff sub-tree under the current node
        nodeChar = node.getChar()
        strSoFar = strSoFar + nodeChar
        thisDLMat.insertChar(nodeChar)
        if node.hasWord() is True:
            editDistForWord = thisDLMat.getEditDistForWord()
            if editDistForWord > 0 and editDistForWord < editDist:
                keyList.append([strSoFar, node.getValue()])
        editDistAfterAddingChar = thisDLMat.getEditDistForCharsSoFar()
        downNode = node.getDownNode()
        if editDistAfterAddingChar <= editDist and downNode is not None:
            self.recursiveSearchFuzzy(node.getDownNode(), editDist, thisDLMat, keyList, strSoFar)
        thisDLMat.popChar()
        strSoFar = strSoFar[:-1]

        # Process stuff for right sub-tree
        rightNode = node.getRightNode()
        if rightNode is not None:
            self.recursiveSearchFuzzy(rightNode, editDist, thisDLMat, keyList, strSoFar)

    # Insert a key into the dictionary's TST
    def insertKey(self, key, val):
        # insertion is never unsuccessful as we create nodes
        leafNode = None
        self._root, leafNode = self.recursiveInsert(self._root, key, val, len(key), 0)

        # Store the leaf nodes of the TST on a priority queue
        # for substring search
        self._priorityQueue.put((val, leafNode))

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
    def searchAllKeysWithPrefix(self, prefix, keyList):
        nodeList = []
        self.recursiveSearchAllKeysWithPrefix(self._root, prefix, len(prefix), 0, nodeList)

        for node in nodeList:
            key = self.getWord(node)
            val = node.getValue()
            keyList.append([key, val])

    # Returns a list of keys whose edit distance according to True Damerau-Levenshtein is within
    # "editDist"
    def searchKeyFuzzy(self, key, editDist, keyList):
        if self._root is None:
            return
        if len(key) < 2:
            return

        thisDLMatrix = DLMatrix(key)
        beginNode = self.findFirstNodeFromTop(self._root, key[0])
        thisDLMatrix.insertChar(beginNode.getChar())
        strSoFar = beginNode.getChar()
        self.recursiveSearchFuzzy(beginNode.getDownNode(), editDist, thisDLMatrix, keyList, strSoFar)

    # Return a list of words which have a given string as a substring
    def searchSubstringKeys(self, pattern, keyList, numWords):
        # Pop keys from the priority queue and run the Boyer
        tmpNodeList = []
        i = 0
        byMatch = BoyerMooreMatch(pattern)
        patternLen = len(pattern)
        while i < numWords and not self._priorityQueue.empty():
            data = self._priorityQueue.get()
            node = data[1]
            tmpNodeList.append(node)
            if node.getWordLength() < patternLen:
                continue

            fullWord = self.getWord(node)
            # check if word is contained in full word using Boyer-Moore
            if byMatch.matches(fullWord):
                val = node.getValue()
                keyList.append([fullWord, val])
                i += 1
        for node in tmpNodeList:
            val = node.getValue()
            self._priorityQueue.put((val, node))

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
