import random
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

#Creates a list of all possible codes
def permuteCodes(codeList,current,length,possibleColors,duplicates):
    if len(current) == length:
        codeList.append(current)
        return
    for color in possibleColors:
        if (canPlace(color,current,duplicates)):
            permuteCodes(codeList,current + color,length,possibleColors,duplicates)

#determines if a color can be added to a code
def canPlace(color,currentCode,duplicates):
    count = 0
    for c in currentCode:
        if (color == c):
            if (duplicates):
                count += 1
            else:
                return False
    return count <2

#gives the hits and blows count of a code vs the secret code
def evalCode(secretCode,testCode):
    hit = 0
    blow = 0
    testSecret = secretCode
    for color in testCode:
        if color in testSecret:
            blow += 1
            testSecret = testSecret.replace(color,'',1)

    for i in range(len(secretCode)):
        if (secretCode[i] == testCode[i]):
            blow -= 1
            hit += 1
    return hit,blow

#prunes possible codes after the previous results
def evalGuesses(codeList,prevGuess,results):
    removedItems = 0
    codeRemoval = []
    for PossibleCode in codeList:
        possibleResults = evalCode(PossibleCode,prevGuess)
        #would PossibleCode return the same result as the one we just got
        if possibleResults[0] == results[0] and possibleResults[1] == results[1]:
            codeRemoval.append(PossibleCode)
        else:
            removedItems += 1

    print("Excluded " + str(removedItems) + " Codes")
    return codeRemoval

#turns the internal code into readable colors
def showColors (code,colorDict):
    resultString = ""
    for color in code:
        resultString += colorDict[color] + " "
    return resultString

#runs iterations number of tests and returns the average turn count, used for trying new selection algorithms
def runTests(iterations):
    turnCountDict = dict()
    for i in range(iterations):
        turns = test()
        if turns in turnCountDict:
            turnCountDict[turns] += 1
        else:
            turnCountDict[turns]=1
    totalTurnCount = 0
    for turns in turnCountDict:
        totalTurnCount += turnCountDict[turns]*turns
        print(str(turns) + " Turns: " + str(turnCountDict[turns]))
    print("Average Turn Count: " + str(totalTurnCount/iterations))

#runs a game of Mastermind with a random code and returns how many turns the AI needed to guess it
def test():
    codeLength = 4
    colorDict = {"a":"a","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","h":"h"}
    codes = []
    permuteCodes(codes,"",codeLength,colorDict,False)
    secretCode = codes[random.randrange(len(codes))]
    #testCode = codes[random.randrange(len(codes))]
    #testCode = codes[0]
    testCode = SelectNextTest(codes)
    print(testCode)
    turns = 0
    while (turns < 100):
        turns += 1
        results = evalCode(secretCode,testCode)
        if (results[0]==codeLength):
            return turns
        codes = evalGuesses(codes,testCode,results)
        #testCode = codes[0]
        #testCode = codes[random.randrange(len(codes))]
        testCode = SelectNextTest(codes)
        print(testCode)
    return 100

#chooses the next test code, currently too expensive to run
def SelectNextTest(codes):
    bestCode = ""
    bestPrune = 0
    originalLength = len(codes)
    possibleResults = []
    permuteResponses(0,0,0,possibleResults)
    print(originalLength,len(possibleResults))
    for code in codes:
        pruneLength = 0
        for result in possibleResults:
            pruneLength += originalLength - len(evalGuesses(codes,code,result))
        if pruneLength > bestPrune:
            bestPrune = pruneLength
            bestCode = code
    return bestCode

#creates a list of all possible hit/blow responses
def permuteResponses(hits,blows,depth,responseList):
    if (depth == 4):
        if [hits,blows] not in responseList:
            responseList.append([hits,blows])
        return
    permuteResponses(hits+1,blows,depth+1,responseList)
    permuteResponses(hits,blows+1,depth+1,responseList)
    permuteResponses(hits,blows,depth+1,responseList)

#Runs a game of Mastermind with the user giving result feedback
def main():
    #setup
    duplicates = True
    pInput = input("Code Length: ")
    codeLength = int(pInput)
    print("Input Possible Colors separated by ,")
    pInput = input()
    colorList = pInput.split(",")
    colorDict = dict()
    for index in range(len(colorList)):
        colorDict[letters[index]] = colorList[index]
    pInput = input("Duplicates? (Y/N) ")
    pInput = pInput.lower()
    if (pInput == "n"):
        duplicates = False

    #permutes all possible codes
    codes = []
    print("Permuting codes, this may take a while")
    permuteCodes(codes,"",codeLength,colorDict,duplicates)
    totalLength = len(codes)

    #gets the first code to try
    testCode = codes[random.randrange(len(codes))]
    print("Done")
    print()
    print("Starting input is: " + showColors(testCode,colorDict))
    print("Format results as 'hits,blows'. Type 'exit' to quit")
    Pinput = ''

    #loop until the player ends the game
    while (Pinput != "exit"):
        Pinput = input()
        if (Pinput == "exit"):
            break
        results = Pinput.split(",")
        hits = int(results[0])
        blows = int(results[1])
        results = [hits,blows]
        codes = evalGuesses(codes,testCode,results)
        print(len(codes))
        testCode = codes[0]
        currentLength = len(codes)
        print("Next Code to try is:" + showColors(testCode,colorDict))
        print(str(100 *currentLength//totalLength) + "% remaining")



main()




