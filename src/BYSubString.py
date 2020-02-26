class BoyerMooreMatch:
    def preComputeDict(self):
        # Just clearer to have two loops
        # One loop to collect all the characters in
        # the alphabet of the pattern and the second
        # to create columns without much of a run-time impact
        for i in range(self._patternLen):
            c = self._pattern[i]
            if self._rightMostPos.get(c) is None:
                self._rightMostPos[c] = -1

        for i in range(self._patternLen):
            c = self._pattern[i]
            val = self._rightMostPos[c];
            self._rightMostPos[c] = max(val, i)

    def __init__(self, pattern):
        _pattern = ""
        self._pattern = pattern
        self._patternLen = len(pattern)
        self._rightMostPos = {}
        self.preComputeDict()

    def getRightMostPosOfChar(self, char):
        if self._rightMostPos.get(char) is None:
            return -1
        else:
            return self._rightMostPos[char]

    def matches(self, text):
        result = False
        textLen = len(text)
        patternLen = self._patternLen
        i = 0
        while (i <= (textLen - patternLen)):
            mismatchFound = False
            end = i + patternLen - 1
            for j in range(patternLen - 1, 0, -1):
                chari = text[end]
                charj = self._pattern[j]
                if (chari == charj):
                    end -= 1
                else:
                    mismatchFound = True
                    skip = self.getRightMostPosOfChar(chari)
                    if skip == -1:
                        i = i + patternLen
                    else:
                        i = i + max(1, (j - skip))
                    break

            if mismatchFound is False:
                result = True
                break

        return result


def testBoyerMoore():
    pattern = "eryx"
    byMatch = BoyerMooreMatch(pattern)
    text = "archaeopteryx"
    print("Text: " + text + "  pattern: " + pattern + "  result: " + str(byMatch.matches(text)))
    text = "myeryx"
    print("Text: " + text + "  pattern: " + pattern + "  result: " + str(byMatch.matches(text)))

    text = "services"
    print("Text: " + text + "  pattern: " + pattern + "  result: " + str(byMatch.matches(text)))
    text = "servieryxces"
    print("Text: " + text + "  pattern: " + pattern + "  result: " + str(byMatch.matches(text)))

# testBoyerMoore()
