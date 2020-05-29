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
    for key in wordDictionary:
        wordsChecked += 1
        print("Words Checked: ", wordsChecked,end="\r")
        answer = vigdecipher(key,cipherText)
        plausibility = checkResult(answer,wordDictionary)
        if (plausibility > .8):
            id = key + ":" + answer
            possibleDict[id] = plausibility
    best = max(possibleDict,key=possibleDict.get)
    print("Most Probable Cipher Key:",best.split(":")[0])
    print("Most Probable Text:",best.split(":")[1])

def vigdecipher(key,cipherText):
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


cipher = "khz scgrzwfvd vvr rlgsjvd jrpv eqiep fza lvamw gf dzgvue rlvth keekixyyrr micieniakaomivs jj gye jtcienwveg xpnjs vvr ko micieniak aih evpmifj tciz"
with open("Dictionary.json") as f:
    words = json.load(f)
    dictionaryBruteForce(words,cipher)