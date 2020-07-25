import json
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

class letter():
    capturedLetter = ''
    frequencyDict = dict()
    occurences = 0
    eowOccurences = 0
    def __init__(self,mainLetter):
        for l in letters:
            self.frequencyDict[l] = 0
        self.capturedLetter = mainLetter

    def addOccurence(self,nextLetter):
        self.occurences += 1
        if (nextLetter == "eow"):
            self.eowOccurences += 1
        else:
            self.frequencyDict[nextLetter] += 1
    def getFrequency(self):
        result = dict()
        for l in self.frequencyDict:
            result[l] = self.frequencyDict[l]/self.occurences
        result['eow'] = self.eowOccurences/self.occurences
        return result
    




with open("words_dictionary.json") as f:
    print("Loading Dictionary")
    words = json.load(f)
    print("Loaded!")

letterList = dict()
for l in letters:
    letterList[l] = letter(l)

for word in words:
    print(word)
    for index in range(len(word)-1):
        if (str.isalpha(word[index+1]) and str.isalpha(word[index])):
            letterList[word[index]].addOccurence(word[index+1])
    letterList[word[-1]].addOccurence('eow')

for l in letterList:
    with open(l + '.json', 'w') as f:
        json.dump(letterList[l].getFrequency(), f)


