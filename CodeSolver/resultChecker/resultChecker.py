import json

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def checkResult(resultString,langDictionary):
    totalWords = 0
    langWords = 0
    for word in resultString.split(" "):
        w = word.lower()
        if w in langDictionary:
            langWords+= 1
        totalWords += 1
    return langWords/totalWords

def acceptResult(resultString,langDictionary,tolerance):
    result = checkResult(resultString,langDictionary)
    return result >= tolerance


def dictionaryBruteForce(wordDictionary,cipherText):
    possibleDict = dict()
    wordsChecked = 0
    total = len(wordDictionary)
    milestone = 1
    print("Starting Dictionary Bruteforce")
    print("Percent Done: 0",end="\r")
    for key in wordDictionary:
        wordsChecked += 1
        if (wordsChecked/total > .05*milestone):
            print("Percent Done:", 5*milestone,end="\r")
            milestone += 1
        answer = vigdecipher(key,cipherText)
        plausibility = checkResult(answer,wordDictionary)
        if (plausibility > .8):
            id = key + ":" + answer
            possibleDict[id] = plausibility
    best = max(possibleDict,key=possibleDict.get)
    print("Most Probable Cipher Key:",best.split(":")[0])
    print("Most Probable Text:",best.split(":")[1])

def absoluteBruteForce(wordDictionary,cipherText,placeMax):
    print("Generating Permutations")
    wordlist = list()
    generateLetterPerms(placeMax,"",wordlist)
    possibleDict = dict()
    wordsChecked = 0
    total = len(wordlist)
    milestone = 1
    print("Complete!")
    print("Starting Simple Bruteforce")
    print("Percent Done: 0",end="\r")
    for item in wordlist:
        wordsChecked += 1
        if (wordsChecked/total > .05*milestone):
            print("Percent Done:",5*milestone,end="\r")
            milestone += 1
        answer = vigdecipher(item,cipherText)
        plausibility = checkResult(answer,wordDictionary)
        if (plausibility > .8):
            id = item + ":" + answer
            possibleDict[id] = plausibility
        if (plausibility == 1):
            print("Found 100% match")
            print("Key:" + item)
            print("Text:" + answer)
            print()
            print("Continue? ")
            userInput = input("(Y/N)")
            if (userInput == "y" or userInput == "Y"):
                pass
            else:
                break
    best = max(possibleDict,key=possibleDict.get)
    print("Most Probable Cipher Key:",best.split(":")[0])
    print("Most Probable Text:",best.split(":")[1])

def generateLetterPerms(depth,currentOutput,finalList):
    if depth == 0:
        finalList.append(currentOutput)
        return
    for letter in letters:
        generateLetterPerms(depth-1,currentOutput+letter,finalList)
    finalList.append(currentOutput)
    return

def vigdecipher(key,cipherText):
    if (len(key) == 0):
        return ""
    keynum = 0
    result= ""
    for letter in cipherText:
        if (letter == " " ):
            result += " "
            continue
        nextLetter = key[keynum]
        if (nextLetter.isalpha()):
            keyVal = letters.index(key[keynum])
            keynum += 1
            keynum %= len(key)
            cipherVal = letters.index(letter)
            result += letters[cipherVal-keyVal]
        else:
            keynum +=1
            keynum %= len(key)
    return result


#cipher = "hes ioph zomwqoiwph ts eoku pvxzi pb hes lbb kec pcir rg qvb fldb"
cipher = "ievwbe hvw ncwvcf vxdwgvd wyg eoo eynatw ve a minjoieoce ased"
with open("Dictionary.json") as f:
    print("Loading Dictionary")
    words = json.load(f)
    print("Loaded!")
    #dictionaryBruteForce(words,cipher)
    absoluteBruteForce(words,cipher,5)