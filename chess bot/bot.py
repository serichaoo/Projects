import chess
import pandas as pd

pieces = ["pawn", "knight", "bishop", "rook", "queen", "king1", "king2"]
table = pd.read_csv("tables/table.csv")
# king1 used for beginning-middlegame
# king2 used for endgame

MAX = int(1e5)

isEndgame = False
# It is the endgame if:
# Both sides have no queens or
# Every side which has a queen has additionally no other pieces or one minorpiece maximum.

board = chess.Board()

def checkEndgame():
    if (((not len(board.pieces(5, 1)))
           or (len(board.pieces(2, 1)) + len(board.pieces(3, 1)) + 2 * len(board.pieces(4, 1)) < 2))
    and ((not len(board.pieces(5, 0)))
           or (len(board.pieces(2, 0)) + len(board.pieces(3, 0)) + 2 * len(board.pieces(4, 0)) < 2))):
        isEndgame = 1

def evaluate():
    material_value = [100, 320, 330, 500, 900, 20000]
    val = 0
    checkEndgame()
    
    # if board.is_checkmate():
    #     if board.turn:
    #         return -MAX
    #     else:
    #         return MAX
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    material = 0
    for i in range(1, 6):
        material += material_value[i-1] * (len(board.pieces(i, 1)) - len(board.pieces(i, 0)))

    val += material

    # add values from piece tables
    for j in range(1, 6):
        val += sum([table[pieces[j-1]].tolist()[i] for i in board.pieces(j, 1)])
        val += sum([-table[pieces[j-1]].tolist()[chess.square_mirror(i)] for i in board.pieces(j, 0)])

    # add value from king table position depending on if it's currently the endgame
    val += sum([table[pieces[6 + isEndgame]].tolist()[i] for i in board.pieces(6, 1)])
    val += sum([-table[pieces[6 + isEndgame]].tolist()[chess.square_mirror(i)] for i in board.pieces(6, 0)])

    if not (board.turn):
        val *= -1
    
    return val

def alphabeta(alpha, beta, depthleft):
    bestscore = -MAX
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        bestscore = max(bestscore, score)
        alpha = max(alpha, score)
    return bestscore

def quiesce(alpha, beta):
    stand_pat = evaluate()
    if (stand_pat >= beta):
        return beta
    alpha = min(alpha, stand_pat)

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()
            if (score >= beta):
                return beta
            alpha = max(alpha, score)
    return alpha

def findMove(depth):
    bestMove = chess.Move.null()
    bestValue = -MAX + 1
    alpha = -MAX
    beta = MAX
    for move in board.legal_moves:
        board.push(move)
        boardValue = -alphabeta(-beta, -alpha, depth-1)
        if (boardValue > bestValue):
            bestMove = move
            bestValue = max(bestValue, boardValue)
        alpha = max(alpha, boardValue)
        board.pop()
    return bestMove

# print(evaluate(board))
# piece = board.piece_at(chess.E2)
# piece_type = piece.piece_type # 1: P, 2: N, 3: B, 4: R, 5: Q, 6: K
# piece_color = piece.color
# piece_symbol = piece.symbol()

# print(piece_type)
# print(piece_symbol)
# print(piece_color)
# print(board.legal_moves)

# Remaining imports
import chess.svg
import chess.pgn
import chess.engine
from IPython.display import SVG

while not board.is_game_over():
    move = findMove(3)
    print(move.uci())
    board.push(move)
    # board.push(chess.Move.from_uci("e2e4"))
    print(board)
    if board.is_game_over():
        break
    playerMove = input("Input your move in algebraic chess notation: ")
    while chess.Move.from_uci(playerMove) not in board.legal_moves:
        playerMove = input("Please enter a legal move: ")
    board.push_san(playerMove)
    # print(board)

print(board.outcome())