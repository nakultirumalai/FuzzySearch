# --------------------------------------------------------------------- #
#  Class for objects on the ternary search tree
# --------------------------------------------------------------------- #
class tstNode:
    # Constructor
    def __init__(self, nodeChar, numWords=0, maxWordLength=0):
        self._char = nodeChar
        self._numWords = numWords
        self._maxWordLength = maxWordLength
        self._val = 0
        self._linkParent = None
        self._linkLeft = None
        self._linkRight = None
        self._linkDown = None
        self._hasWord = False
        self._wordLength = 0

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

    def __lt__(self, other):
        return self._val > other._val
