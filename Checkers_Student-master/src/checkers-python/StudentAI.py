from random import randint
from BoardClasses import Move
from BoardClasses import Board
import timeit


# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.


class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        depth = 3
        bestVal = -9999
        moves = self.board.get_all_possible_moves(self.color)

        # choose a random move as first move
        index = randint(0, len(moves) - 1)
        inner_index = randint(0, len(moves[index]) - 1)
        bestMove = moves[index][inner_index]

        for move in moves:
            for m in move:
                self.board.make_move(m, self.color)

                nextTurn = self.opponent[self.color]
                isBlack = self.color == 1
                moveVal = self.minimax(depth, nextTurn, isBlack)
                self.board.undo()

                if moveVal > bestVal:
                    bestMove = m
                    bestVal = moveVal

        self.board.make_move(bestMove, self.color)
        return bestMove

    def minimax(self, depth, turn, isBlack):
        if depth == 0 or \
                self.board.is_win(self.color) or self.board.is_win(self.opponent[self.color]):
            return self.evalBoard(turn)

        moves = self.board.get_all_possible_moves(turn)
        if (isBlack and turn == 1) or (not isBlack and turn == 2):  # if maximizing our ai
            maxVal = -9999

            for move in moves:
                for m in move:
                    self.board.make_move(m, turn)
                    maxVal = max(maxVal, self.minimax(depth - 1, self.opponent[turn], isBlack))
                    self.board.undo()
            return maxVal

        else:
            minVal = 9999

            for move in moves:
                for m in move:
                    self.board.make_move(m, turn)
                    minVal = min(minVal, self.minimax(depth - 1, self.opponent[turn], isBlack))
                    self.board.undo()
            return minVal

    def evalBoard(self, turn):
        score = 0
        for i in range(self.row):
            for j in range(self.col):
                if turn == 1:  # is Black
                    if self.board.board[i][j].color == "B":
                        if self.board.board[i][j].is_king:
                            score += 5 + self.row + 2
                        # if i >= (self.row-1)/2:
                        #     score += 5 + i
                        else:
                            score += 5 + (self.row-1-i)

                    elif self.board.board[i][j].color == "W":
                        if self.board.board[i][j].is_king:
                            score -= 5 + self.row + 2
                        # if i >= (self.row-1)/2:
                        #     score -= 5 + i
                        else:
                            score -= 5 + (self.row-1-i)

                else:  # is While
                    if self.board.board[i][j].color == "W":
                        if self.board.board[i][j].is_king:
                            score += 5 + self.row + 2
                        # if i <= (self.row-1)/2:
                        #     score += 5 + (self.row-1-i)
                        else:
                            score += 5 + i

                    elif self.board.board[i][j].color == "B":
                        if self.board.board[i][j].is_king:
                            score -= 5 + self.row + 2
                        # if i <= (self.row-1)/2:
                        #     score -= 5 + (self.row-1-i)
                        else:
                            score -= 5 + i

        return score
