import copy
import pprint
import random


ZERO = 0
SIZE = 5


"""
    0: Left
    1: Right
    2: Up
    3: Down
"""
DIRECTON = {
    0: (0, -1),
    1: (0, 1),
    2: (1, 0),
    3: (-1, 0)
}

TRIGGER = {
    2: [(0, 0), (0, 4), (4, 0), (4, 4)],
    3: [(0, 1), (0, 2), (0, 3),
        (1, 0), (1, 4),
        (2, 0), (2, 4),
        (3, 0), (3, 4),
        (4, 1), (4, 2), (4, 3)],
    4: [(1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2), (3, 3)]
}


# Reads the current board state and returns board, player and opponent
def readBoard():
    playerBoard = {
        "location": [],
        "pieces": []
    }

    oppBoard = {
        "location": [],
        "pieces": []
    }

    for i in range(SIZE):
        row = input().split()

        for j, val in enumerate(row):
            if int(val[0]) == 1:
                playerBoard["location"].append((i, j))
                playerBoard["pieces"].append(int(val[1]))
            elif int(val[0]) == 2:
                oppBoard["location"].append((i, j))
                oppBoard["pieces"].append(int(val[1]))

    pBoard = dict(zip(playerBoard["location"], playerBoard["pieces"]))
    oBoard = dict(zip(oppBoard["location"], oppBoard["pieces"]))

    board = {
        1: pBoard,
        2: oBoard
    }

    opponent = 1
    player = int(input())

    if player == 1:
        opponent = 2

    return board, player, opponent


def addTuple(a, b):
    return ((a[0] + b[0]), (a[1] + b[1]))


def checkBound(pos):
    if (pos[0] > -1 and pos[0] < SIZE) and (pos[1] > -1 and pos[1] < SIZE):
        return True
    else:
        return False


def checkTrigger(move, score):
    for key in TRIGGER:
        if move in TRIGGER[key]:
            if score >= key:
                return True

    return False


def checkAdjacent(move):
    adjacentLocations = []

    for val in DIRECTON:
        temp = addTuple(DIRECTON[val], move)

        if checkBound(temp):
            adjacentLocations.append(temp)

    return adjacentLocations


def getMoves(board, player, opponent):
    possibleMoves = []

    for i in range(SIZE):
        for j in range(SIZE):
            if (i, j) not in board[opponent]:
                possibleMoves.append((i, j))
            elif (i, j) in board[player]:
                possibleMoves.append((i, j))

    return possibleMoves


def checkFinalMove(board, player, opponent):
    sum = 0

    for move in board[player]:
        sum += board[player][move]

    if sum <= 1:
        return 0

    if len(board[player]) == 0 or len(board[opponent]) == 0:
        return 1
    else:
        return 0


def scoreAllBoards(everything, player, opponent):
    results = {
        "initialMove":  [],
        "simulatedMove": [],
        "score": [],
        "simulatedScore": []
    }

    for original in everything:
        counter = 0
        # Original move to a board A
        for dict_moveA in original:
            if counter == 0:
                origKey = list(dict_moveA.keys())

                origKey = (origKey[0])
                board = dict_moveA[origKey]

                results["initialMove"].append(origKey)
                score = scoreBoard(board, player, opponent)
                results["score"].append(score)

            if counter == 1:
                simKey = original[counter][origKey]
                results["simulatedMove"].append(simKey)

            if counter == 2:
                oppScore = 0
                secondCounter = 0

                for singleBoard in original[counter][simKey]:
                    print(oppScore)
                    oppScore += scoreBoard(singleBoard, opponent, player)
                    secondCounter += 1    

                results["simulatedScore"].append(oppScore)

            counter += 1
    
    return results


    

def scoreBoard(board, player, opponent):
    playerScore = 0
    oppScore = 0

    for move in board[player]:
        playerScore += board[player][move]

    playerScore *= len(board[player])

    for i in TRIGGER:
        for move in board[opponent]:
            if move in TRIGGER[i]:
                if board[opponent][move] <= (i - 2):
                    playerScore += 10

    if checkFinalMove(board, player, opponent) != 0:
        playerScore += 9999999

    return playerScore


def simulateMove(board, player, opponent, move):
    newBoard = copy.deepcopy(board)

    if move in newBoard[opponent]:
        newBoard[player][move] += newBoard[opponent][move] + 1
        del newBoard[opponent][move]
    elif move in newBoard[player]:
        newBoard[player][move] += 1
    else:
        newBoard[player][move] = 1

    piecesToExplode = []

    if checkTrigger(move, newBoard[player][move]):
        piecesToExplode.append(move)

    while piecesToExplode != []:
        currentMove = piecesToExplode.pop()
        primer = 0

        # Loop to find the TRIGGER value
        for i in TRIGGER:
            if currentMove in TRIGGER[i]:
                primer = i
                break

        newBoard[player][currentMove] -= primer
        if newBoard[player][currentMove] <= 0:
            del newBoard[player][currentMove]

        adjacentLocations = checkAdjacent(currentMove)
        #Move checkFinal below the for statement
        for loc in adjacentLocations:
            if checkFinalMove(newBoard, player, opponent) != 0:
                return newBoard

            if loc in newBoard[opponent]:
                newBoard[player][loc] = newBoard[opponent][loc] + 1
                del newBoard[opponent][loc]
            elif loc in newBoard[player]:
                newBoard[player][loc] += 1
            else:
                newBoard[player][loc] = 1

            if checkTrigger(loc, newBoard[player][loc]):
                if loc not in piecesToExplode:
                    piecesToExplode.append(loc)

    return newBoard


def getAllBoards(board, player, opponent, allMoves):
    allBoards = []

    for move in allMoves:
        simulatedBoard = simulateMove(board, player, opponent, move)
        allBoards.append(simulatedBoard)
    
    return allBoards


def simulateAllMoves(board, player, opponent, allMoves):
    results = {
        "initialMove":  [],
        "score": []
    }

    for move in allMoves:
        results["initialMove"].append(move)
        simulatedBoard = simulateMove(board, player, opponent, move)
        score = scoreBoard(simulatedBoard, player, opponent)
        results["score"].append(score)
    
    return dict(zip(results["initialMove"], results["score"]))


def searchNextMove(board, player, opponent):
    playerMoves = getMoves(board, player, opponent)
    playerBoards = getAllBoards(board, player, opponent, playerMoves)

    everything = []
    moveAToboardA = {}
    moveAToMoveB = {}
    moveBToBoardB = {}

    for currMove in playerMoves:
        for currBoard in playerBoards:
            oppMoves = getMoves(currBoard, opponent, player)
            oppBoard = getAllBoards(currBoard, opponent, player, oppMoves)

            moveAToboardA[currMove] = currBoard

            for singleMove in oppMoves:
                for singleBoard in oppBoard:
                    try:
                        moveAToMoveB[currMove] = singleMove
                    except:
                        moveAToMoveB[currMove] = (5, 5)
            
                    moveBToBoardB[singleMove] = singleBoard      
    
        everything.append((moveAToboardA, moveAToMoveB, moveBToBoardB))
    
    return everything


def bestMove(possibleMoves):
    for move in possibleMoves:
        if possibleMoves[move] == max(list(possibleMoves.values())):
            return move


def displayMove(move):
    print(move[0], move[1])


# This function prints the board in a readable manner
def printBoard(board):
    dis = [["00" for z in range(SIZE)] for y in range(SIZE)]
    for player in board:
        for position in board[player]:
            dis[position[0]][position[1]] = str(player) + str(board[player][position])

    board_str = "\n".join([" ".join(x) for x in dis])

    print(board_str)


# Main Function
if __name__ == "__main__":
    board, player, opponent = readBoard()
    boardsAndMoves = searchNextMove(board, player, opponent)
    scoreAllBoards(boardsAndMoves, player, opponent)

    #move = bestMove(results)
    #displayMove(move)
    #printBoard(simulateMove(board, player, opponent, move))
