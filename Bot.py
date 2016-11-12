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
    2: {(0, 0), (0, 4), (4, 0), (4, 4)},
    3: {(0, 1), (0, 2), (0, 3),
        (1, 0), (1, 4),
        (2, 0), (2, 4),
        (3, 0), (3, 4),
        (4, 1), (4, 2), (4, 3)},
    4: {(1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2), (3, 3)}
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

    zeroBoard = {
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
            else:
                zeroBoard["location"].append((i, j))
                zeroBoard["pieces"].append(0)

    zBoard = dict(zip(zeroBoard["location"], zeroBoard["pieces"]))
    pBoard = dict(zip(playerBoard["location"], playerBoard["pieces"]))
    oBoard = dict(zip(oppBoard["location"], oppBoard["pieces"]))

    board = {
        0: zBoard,
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


def addAdj(board, player, opponent, mainLocation, adjacentLocations):
    primer = 0

    # Loop to find the TRIGGER value 
    for i in TRIGGER:
        if mainLocation in TRIGGER[i]:
            primer = i 
            break

    # Empties the main section or creates a new one and adds it to the board
    if mainLocation in board[player]:
        board[player][mainLocation] -= primer
    else:
        board[player][mainLocation] = 0
    
    # Changes the adjacent locations accordingly and stores them
    for loc in adjacentLocations:
        if loc in board[opponent]:
            del board[opponent][loc]

        if loc in board[player]:
            board[player][loc] += 1
        else:
            board[player][loc] = 1

    return board


def getMoves(board, player):
    possibleMoves = []
    possibleMoves.append(board[ZERO])
    possibleMoves.append(board[player])
    
    return possibleMoves


def checkFinalMove(board, player, opponent):
    if not bool(board[player]) and not bool(board[opponent]):
        return 0
        
    if not board[player]:
        return opponent
    if not board[opponent]:
        return player
    else:
        return 0


def scoreBoard(board, player, opponent):
    playerScore = 0
    multiplier = 1
    oppScore = 0

    for move in board[player]:
        playerScore += board[player][move] 
        
        for i in TRIGGER:
            if move in TRIGGER:
                multiplier = abs(board[player][move] - i)
    
    playerScore += 10/multiplier

    for move in board[opponent]:
        oppScore += board[opponent][move] 

        for i in TRIGGER:
            if move in TRIGGER:
                multiplier = abs(board[player][move] - i) * -1

    oppScore += 10/multiplier

    finalScore = playerScore * len(board[player])  - oppScore * len(board[opponent])

    return finalScore
                

def simulateMove(board, player, opponent, move):
    if checkFinalMove(board, player, opponent) != 0:
        return 100000
    else:
        adj = checkAdjacent(move)
        newBoard = addAdj(board, player, opponent, move, adj)

        tri = checkTrigger(move, newBoard[player][move])
        while tri:
            tri = checkTrigger(move, newBoard[player][move])

        # simulateMove(newBoard, player, opponent, move)

        return scoreBoard(newBoard, player, opponent)


def simulateAllMoves(board, player, opponent):
    results = {
        "initialMove":  [],
        "score": []
    }

    possibleMoves = getMoves(board, player)

    for i in range(2):
        for move in possibleMoves[i]:
            newBoard = copy.deepcopy(board)
            results["initialMove"].append(move)
            score = simulateMove(newBoard, player, opponent, move)
            results["score"].append(score)

    return dict(zip(results["initialMove"], results["score"]))


def bestMove(possibleMoves):
    for move in possibleMoves:
        if possibleMoves[move] == max(list(possibleMoves.values())):
            return move


def displayMove(move):
    print(move[0], move[1])


# This function prints the board in a readable manner
def printBoard(board):
    pprint.pprint(board[1])
    pprint.pprint(board[2])


# Main Function
if __name__ == "__main__":
    board, player, opponent = readBoard()
    results = simulateAllMoves(board, player, opponent)
    move = bestMove(results)
    displayMove(move)