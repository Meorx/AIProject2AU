import numpy as np
import math


class CheckingSystem:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (Red, Green or Blue). The value will be one of the 
        strings "red", "green", or "blue" correspondingly.
        """
        # TODO: Set up state representation.

        opponentColours = ["red", "green", "blue"]
        opponentColours.remove(colour)

        # initialize gamestate
        self.gamestate = {
            "board":{
            (-3, 3, 0): "red",
            (-3, 2, 1): "red",
            (-3, 1, 2): "red",
            (-3, 0, 3): "red",

            (0, 3, -3): "green",
            (1, 2, -3): "green",
            (2, 1, -3): "green",
            (3, 0, -3): "green",

            (0, -3, 3): "blue",
            (1, -3, 2): "blue",
            (2, -3, 1): "blue",
            (3, -3, 0): "blue"
        },
        "score": {
            "red": 0,
            "green": 0,
            "blue": 0
        },
        "pieces": {
            "red": 4,
            "green": 4,
            "blue": 4
        },
        "playerColour": colour,
        "opponentColours": opponentColours,
        "turnCounter": 0
        }

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        """
        # TODO: Decide what action to take + test the depth(s)
        #openingBook = [("MOVE", ((-3,1), (-2,1))), ("MOVE", ((2,-3), (1,-2))), ("MOVE", ((2,1), (1,1)))]

        #if self.gamestate["turnCounter"] < 3:
         #   move = openingBook[self.gamestate["turnCounter"]]
        #else:
           # move = formatCubicMove(bestReplySearch(self.gamestate, 4))
        move = formatCubicMove(bestReplySearch(self.gamestate, 1))
        
        return move


    def update(self, colourAtPlay, action):
        

        doMove(self.gamestate, colourAtPlay, formatAxialMove(action))
        
        #function!!
        

        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red", 
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or 
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action 
        (or pass) for the player colour (your method does not need to validate 
        the action/pass against the game rules).
        """
        # TODO: Update state representation in response to action.

def doMove(gamestate, colourAtPlay, action):
    cubicFromTo = action[1]

    gamestate["turnCounter"]+=1

    if (action[0] == "MOVE"):
        gamestate["board"][cubicFromTo[1]] = colourAtPlay
        del gamestate["board"][cubicFromTo[0]]

    elif (action[0] == "JUMP"):
        gamestate["board"][cubicFromTo[1]] = colourAtPlay
        del gamestate["board"][cubicFromTo[0]]

        #update #pieces
        gamestate["pieces"][colourAtPlay] += 1
        gamestate["pieces"][gamestate["board"][jumpedCoordinates(cubicFromTo)]] -= 1

        gamestate["board"][jumpedCoordinates(cubicFromTo)] = colourAtPlay

    elif (action[0] == "EXIT"):
        
        del gamestate["board"][cubicFromTo]
        gamestate["score"][colourAtPlay] += 1

    elif (action[0] == "PASS"):
        return

def undoMove(gamestate, colourAtPlay, action):
    gamestate["turnCounter"]-=1

    cubicFromTo = action[1]

    if (action[0] == "MOVE"):
        gamestate["board"][cubicFromTo[0]] = colourAtPlay
        del gamestate["board"][cubicFromTo[1]]

    elif (action[0] == "JUMP"):
        gamestate["board"][cubicFromTo[0]] = colourAtPlay
        del gamestate["board"][cubicFromTo[1]]

        #update #pieces
        gamestate["pieces"][colourAtPlay] -= 1
        gamestate["pieces"][action[2]] += 1

        gamestate["board"][jumpedCoordinates(cubicFromTo)] = action[2]

    elif (action[0] == "EXIT"):
        gamestate["board"][cubicFromTo] = colourAtPlay
        gamestate["score"][colourAtPlay] -= 1

    elif (action[0] == "PASS"):
        return

def jumpedCoordinates(fromto):
    delta = np.divide(np.subtract(fromto[1], fromto[0]), 2)
    return tuple(np.add(fromto[0], delta))

def axial_to_cubic(positions):
    # convert axial to cubic coordinates
    cubic = []
    for p in positions:
        cubic.append((p[0], -p[0] - p[1], p[1]))
    return tuple(cubic)

def getMoves(gamestate, colour):
    feasible_moves = []

    #get occupied spaces
    blocked = list(gamestate["board"].keys())

    #get array of the player's pieces
    positions = []
    for key, item in gamestate["board"].items():
        if item == colour:
            positions.append(key)


    for start_pos in positions:

        # all directions a piece can move in
        directions = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]
        moves = [((start_pos[0] + d[0], start_pos[1] + d[1], start_pos[2] + d[2]), "MOVE", start_pos) for d in
                 directions]

        # if space is occupied add jump
        for i, m in enumerate(moves):
            if m[0] in blocked:
                jumppos = (moves[i][0][0] + directions[i][0], moves[i][0][1] + directions[i][1],
                           moves[i][0][2] + directions[i][2])
                #last value is colour jumped over to retain information
                moves[i] = (jumppos, "JUMP", start_pos, gamestate["board"][m[0]])

        # check if all moves still on board and not blocked
        for mv in moves:
            m = mv[0]
            if max((m[0], m[1], m[2])) <= 3 and min((m[0], m[1], m[2])) >= -3:
                if m not in blocked:
                    feasible_moves.append(mv)

        #If in endzone add exit action
        if start_pos[getEndzoneIndex(colour)] == 3:
            feasible_moves.append(((), "EXIT", start_pos))

    #format it to fit the specs
    feasible_actions = []
    for m in feasible_moves:
        if m[1] == "EXIT":
            feasible_actions.append((m[1], m[2]))
        elif m[1] == "JUMP":
            feasible_actions.append((m[1], (m[2], m[0]), m[3]))
        else:
            feasible_actions.append((m[1], (m[2], m[0])))

    #pass if no pieces left
    if not feasible_actions:
        feasible_actions.append(("PASS", None))

    return feasible_actions

def formatCubicMove(cubicMove):
    if cubicMove[0] == "MOVE" or cubicMove[0] == "JUMP":
        return (cubicMove[0], (cubic_to_axial(cubicMove[1])))
    elif cubicMove[0] == "EXIT":
        return (cubicMove[0], cubic_to_axial([cubicMove[1]])[0])
    elif cubicMove[0] == "PASS":
        return cubicMove
    else:
        assert()

def formatAxialMove(axialMove):
    if axialMove[0] == "MOVE" or axialMove[0] == "JUMP":
        return (axialMove[0], axial_to_cubic(axialMove[1]))
    elif axialMove[0] == "EXIT":
        return (axialMove[0], (axialMove[1][0], -axialMove[1][0]-axialMove[1][1], axialMove[1][1]))
    elif axialMove[0] == "PASS":
        return axialMove
    else:
        assert()

def cubic_to_axial(positions):
    axial = []
    for p in positions:
        axial.append((p[0], p[2]))
    return tuple(axial)

#TODO: 
# - make this function return the best move
# - ensure that the best move is updated
def bestReplySearch(gamestate, initDepth):
    #copy gamestate
    gs = dict(gamestate)

    playerColour = gamestate["playerColour"]

    opponentColours = gamestate["opponentColours"]

    

    def BRS(alpha, beta, depth, turn, first):
        # if terminal node or depth is reached return eval value
        if depth <= 0 or max(gs["score"].values()) >= 5:
            # TODO Terminal state
            return evaluate(gs)

        if first: realMoveValues = []
        
        if turn == "MAX":
            #MAX turn
            
            moves = getMoves(gs, playerColour)
            #if first: print(moves)

            value = -math.inf

            for move in moves:
                doMove(gs, gs["playerColour"], move)
                brs = BRS(alpha, beta, depth-1, "MIN", False)

                if first: 
                    realMoveValues.append(brs)
                    
                value = max(value, brs)

                undoMove(gs, gs["playerColour"], move)

                alpha = max(alpha, value)

                if alpha >= beta:
                    #beta cut off
                    break
            
            if first:
                #return move with highest value
                print([(realMoveValues[i], m) for i, m in enumerate(moves)])
                i = realMoveValues.index(value)
                return moves[i]

            return value

        else:
            #MIN turn
            moves = []
            for c in opponentColours:
                moves = [(m, c) for m in getMoves(gs, c)]
            value = math.inf
            for move in moves:
                doMove(gs, move[1], move[0])
                value = min(value, BRS(alpha, beta, depth-1, "MAX", False))
                undoMove(gs, move[1], move[0])

                beta = min(beta, value)
                if alpha >= beta:
                    #alpha cut off
                    break
            return value

    return BRS(-math.inf, math.inf, initDepth, "MAX", True)
    
def getEndzoneIndex(colour):
    if colour == "red":
        return 0
    elif colour == "blue":
        return 1
    elif colour == "green":
        return 2
    else:
        assert()

# TODO: complete the evaluation function
# Checks value at a given node/state
def evaluate(gamestate):

    h = 0
    #TODO 
    variables = {
        "distance": 0,
        "score": 0,
        "pieces_on_board": 0,
        "turn": 0,
        "winning": 0
    }

    weights = {
        "distance": -1,
        "score": 20,
        "pieces_on_board": 80,
        "turn": -0.5,
        "winning": 99999
    }

    variables["turn"] = gamestate["turnCounter"]

    variables["pieces_on_board"] = gamestate["pieces"][gamestate["playerColour"]]

    for pos, pieceColour in gamestate["board"].items():
        if gamestate["playerColour"] == pieceColour:
            variables["distance"] += distancetoGoal(pos, pieceColour)
#        else:
#            variables["distance"]-=distancetoGoal(pos, pieceColour)

    # Average distance of a piece to the exit
    variables["distance"] = variables["distance"]/(variables["pieces_on_board"]+1)

    variables["score"] += gamestate["score"][gamestate["playerColour"]]
    variables["score"] -= max(gamestate["score"][gamestate["opponentColours"][0]], gamestate["score"][gamestate["opponentColours"][1]])

    #if variables["pieces_on_board"] >= 4:


        
    if variables["score"] >= 4:
        variables["winning"] = 20
    elif gamestate["score"][gamestate["opponentColours"][0]] >= 4:
        variables["winning"] = -20
    elif gamestate["score"][gamestate["opponentColours"][1]] >= 4:
        variables["winning"] = -20

    for k in variables:
        h += variables[k] * weights[k]

    #print(gamestate["score"][gamestate["opponentColours"][0]])
    #print(gamestate["score"][gamestate["opponentColours"][1]])


    return h
    
def distancetoGoal(point, colour):
    # if position empty (node exited heuristic =0)
    if not point:
        return 0
    destination = getGoalPosition(colour)
    # moves to end zone + one for exiting

    return abs(point[getEndzoneIndex(colour)] - destination[getEndzoneIndex(colour)]) / 2 + 1

def getGoalPosition(colour):
    # returns position of goal
    if (colour == "red"):
        return (3, 0, 0)
    if (colour == "green"):
        return (0, 0, 3)
    if (colour == "blue"):
        return (0, 3, 0)