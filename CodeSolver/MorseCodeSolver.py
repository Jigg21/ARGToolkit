import librosa
morseCodeDict = {".-":"a", "-...":"b", "-.-.":"c", "-..":"d", ".":"e", "..-.":"f", "--.":"g",
                "....":"h", "..":"i", ".---":"j","-.-":"k",".-..":"l", "--":"m", "-.":"n",
                "---": "o", ".--.":"p", "--.-":"q", ".-.":"r", "...":"s", "-":"t", "..-":"u",
                "...-":"v", ".--":"w", "-..-":"x", "-.--":"y", "--..":"z", ".----":"1", 
                "..---":"2", "...--":"3", "....-":"4", ".....":"5", "-....":"6", "--...":"7",
                "---..":"8", "----.":"9", "-----":"0", ".-.-.-":".","-.-.--":"!","..--.":"?",
                "-.--.":"(","-.--.-":")","--..--":",",".-..-.":'"',".----.":"'","-..-.":"/"}

class soundOBJ:
    startSample = 0
    endSample = 0
    silence = False
    def __init__(self,startSample,endSample,silence):
        self.startSample = startSample
        self.endSample = endSample
        self.silence = silence

    def updateEndSample(self,newEnd):
        self.endSample = newEnd

    def __str__(self):
        if (self.silence):
            return "[" + str(self.startSample) + "," + str(self.getDuration) + "] S"
        else:
            return "[" + str(self.startSample) + "," + str(self.getDuration) + "]"
    
    def display(self,threshold):
        if (self.getDuration() <= threshold):
            if (self.silence):
                return ''
            else:
                return '.'
        else:
            if (self.silence):
                if (self.getDuration() >= threshold*3):
                    return ' | '
                else:
                    return " "
            else:
                return '-'
    
    def getDuration(self):
        return self.endSample - self.startSample

def morseDecipher(inputString):
    result = ""
    for letter in inputString.split(" "):
        if (letter == "|"):
            result += " "
        else:
            result += morseCodeDict[letter]
    return result
    
def audioFileExtract(soundFile):
    average = 0
    for sample in soundFile:
        average += abs(sample)
    average /= len(soundFile)

    active = False
    soundList = []
    prevSound = soundOBJ(0,0,True)
    for sample in range(0,len(soundFile),4):
        if abs(soundFile[sample]) > .001:
            if not active:
                active = True
                prevSound.updateEndSample(sample)
                soundList.append(prevSound)
                prevSound = soundOBJ(sample,0,False)
        else:
            if active:
                active = False
                prevSound.updateEndSample(sample)
                soundList.append(prevSound)
                prevSound = soundOBJ(sample,0,True)

    durationList = []
    for sound in soundList:
        if (not sound.silence):
            durationList.append(sound.getDuration())

    unitTime = min(durationList)

    result = ""
    for sound in soundList:
        result += sound.display(unitTime)
    return result

def audioDecrypt():
    soundFile,sr = librosa.load("morse.wav")
    extratedMorse = audioFileExtract(soundFile)
    result = morseDecipher(extratedMorse)
    print(result)

audioDecrypt()