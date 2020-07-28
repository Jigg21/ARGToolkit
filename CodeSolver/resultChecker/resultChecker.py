import json

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#Gets a deciphered string and returns it's probablility of being correct
def checkResult(resultString,langDictionary):
    totalWords = 0
    langWords = 0
    #checks how many words in the string are in the language dictionary
    for word in resultString.split(" "):
        w = word.lower()
        if w in langDictionary:
            langWords+= 1
        totalWords += 1
    return langWords/totalWords

#returns true if a string is above a certain tolerance of "correctness"
def acceptResult(resultString,langDictionary,tolerance):
    result = checkResult(resultString,langDictionary)
    return result >= tolerance