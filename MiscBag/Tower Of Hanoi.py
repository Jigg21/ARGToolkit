VERBOSE = False
RINGS = 3
class Ring(object):

    def __init__(self, position, size):
        self.position = position
        self.size = size
    
    def compare (self, other):
        if (other is None):
            return True
        else:
            return self.size < other.size
    
    def changePosition(self,newPosition):
        self.position = newPosition;

    def __str__(self) -> str:
        return "Position : " + str(self.position) + " Size:" + str(self.size)

class move():
    def __init__(self, fromP, toP):
        self.fromP = fromP
        self.toP = toP

    def perform(self,gameBoard):
        movedRing = gameBoard[self.fromP].pop()
        gameBoard[self.toP].add(movedRing)
        movedRing.changePosition(self.toP)

    def undo(self,gameBoard):
        movedRing = gameBoard[self.toP].pop()
        gameBoard[self.fromP].add(movedRing)
        movedRing.changePosition(self.fromP)
        
    def __str__(self) -> str:
        return "From: " + str(self.fromP) + " To: " + str(self.toP)

class Stack:
    
    def __init__(self):
        self.stack = []

    def add(self, dataval):
# Use list append method to add element
        if dataval not in self.stack:
            self.stack.append(dataval)
            return True
        else:
            return False
        
# Use list pop method to remove element
    def pop(self):
        if len(self.stack) <= 0:
            return None
        else:
            return self.stack.pop()
    
    def peek(self):
        if len(self.stack) <= 0:
            return None
        else:
            return self.stack[len(self.stack) - 1]

    def dump(self):
        result = ""
        for r in self.stack:
            if (r is not None):
                result += str(r.size)
        return result

    def __len__(self):
        return len(self.stack)

    def isEmpty(self):
        return len(self.stack) == 0



    

    
def displayGameBoard(gameboard):
    if (VERBOSE):
        for rung in gameboard:
            
            print("|" + rung.dump())


def getMoves(gameboard):
    moveableRings = []
    for rung in gameboard:
        r = rung.peek()
        if (r is not None):
            moveableRings.append(r)
            if VERBOSE :print (r)
            

    moves = []
    for f in moveableRings:
        for rung in range(len(gameboard)):
            if f.position != rung:
                if f.compare(gameboard[rung].peek()):
                    if VERBOSE : print("Size: " + str(f.size) + " " + str(move(f.position,rung)))
                    moves.append(move(f.position,rung))
    return moves

    
def play(gameBoard):
    if VERBOSE: print("Starting")
    pastGameBoards = []
    for m in getMoves(gameBoard):
        if VERBOSE: print("Running")
        triedMoves = []
        if makeMove(gameBoard.copy(),m,pastGameBoards,triedMoves):
            print("Done! Took",len(triedMoves), "moves")
            
            if (VERBOSE):
                for move in triedMoves:
                    print(move)
            return
    

def makeMove(testGameBoard,move,pastGameBoards,moves):
    #print("Move " + str(moves), move)
    
    move.perform(testGameBoard)
    displayGameBoard(testGameBoard)
    id = getBoardID(testGameBoard)
    if  id in pastGameBoards:
        if VERBOSE: print("Found Redundency")
        return False
    elif stillPlaying(testGameBoard):
        pastGameBoards.append(id)
        for m in getMoves(testGameBoard):
            if VERBOSE: print("Trying Move " + str(len(moves)) + " :" ,m)
            moves.append(m)
            if makeMove(testGameBoard,m,pastGameBoards,moves):
                return True
            m.undo(testGameBoard)
            moves.pop()
    else:
        if VERBOSE: print("WIN")
        displayGameBoard(testGameBoard)
        return True
    
    move.undo(testGameBoard)
    

    



def getBoardID (gameBoard):
    id = gameBoard[0].dump() + "0" + gameBoard[1].dump() + "0" + gameBoard[2].dump()
    return int(id)


    
def stillPlaying(gameBoard):
    return not (gameBoard[0].isEmpty() and gameBoard[1].isEmpty())


    
def main ():
    rings = list()
    gameboard = [Stack(),Stack(),Stack()]
    for i in range(0,RINGS):
        newRing = Ring(0,RINGS-i)
        rings.append(newRing)
        gameboard[0].add(newRing)
    displayGameBoard(gameboard)
    play(gameboard)
    



if __name__ == '__main__':
    main()
    