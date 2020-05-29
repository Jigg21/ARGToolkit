import json

def print_word(wordDict,wordCode):
    for letter in wordCode:
        print(wordDict[letter], end='')
    print()
    for letter in wordCode:
        print(' ' + letter, end=' ')

def changeLetter(dictLetter,realLetter,wordDict,used):
    if realLetter in used:
        print(realLetter + " already in use.")
        return
    if wordDict[dictLetter] != ' _ ':
        used.remove(wordDict[dictLetter].strip())
    wordDict[dictLetter] = ' ' + realLetter + ' '

def guessWord (lenWord,requiredLetters,used):
    print(lenWord,requiredLetters)
    paths = ['len1.json','len2.json','len3.json','len4.json','len5.json','len6.json','len7.json','len8.json','len9.json']
    data = dict()
    if lenWord > 8:
        with open(paths[8]) as f:
            data = json.load(f)
    else:
        print("using" + paths[lenWord-1])
        with open(paths[lenWord-1]) as f:
            data = json.load(f)
    possibleWords = []
    for word in data.keys():
        possible = True
        for letter in requiredLetters:
            if word[letter[1]] != letter[0]:
                possible = False
                break
            if letter in used and not letter in requiredLetters:
                possible = False
                break
        if (possible):
            possibleWords.append(word)
    return possibleWords

def main():
    print()
    #print("Input code as representative values separated by commas")
    #print("Example: Hello World = 'A,B,C,C,D, ,E,D,F,C,G'")
    #stringInput = input("Code: ")
    stringInput = "a,b,c,c,d, ,e,c,f, ,d,b,g, ,h,e,d,i"
    wordCode = stringInput.split(',')
    wordDict = {' ': '   '}
    clearDict = {' ': '   '}
    for code in wordCode:
        if (code == ' '):
            wordDict[code] = '   '
        else:
            wordDict[code] = " _ "
            clearDict[code] = " _ "
    print()
    print("To Change a letter type 'Index Letter:Real Letter")
    print("When you are done, type in ':e'")
    print()

    print_word(wordDict,wordCode)
    userInput = input()
    userInput = userInput.strip()
    usedLetters = []
    while (userInput != ':e'):
        if (userInput == ':c'):
            wordDict = clearDict.copy()
            usedLetters = []
            continue
        userInput.strip()
        curInput = userInput.split(':')
        
        if (curInput[0] == "guess"):
            wordString = ''
            for letter in wordCode:
                wordString += letter
            splitString = wordString.split(' ')
            requestedWord = splitString[eval(curInput[1])-1]
            requiredLetters = []
            for count,letter in enumerate(requestedWord):
                if (wordDict[letter] != ' _ '):
                    requiredLetters.append((wordDict[letter].strip(),count))

            possibleWords = guessWord(len(requestedWord),requiredLetters,usedLetters)
            print("Could be:")
            for word in possibleWords:
                print(word)
            continue
        

        changeLetter(curInput[0],curInput[1],wordDict,usedLetters)
        usedLetters.append(curInput[1])
        print_word(wordDict,wordCode)
        print()
        print()
        userInput = input()
        print()

main()