import copy
import random
import sys

class Team2:
    def __init__(self):
        self.bonus = False

    def miniB_pattern_checker(self, board, x, y, ply):
        count = []
        for i in range(8):
            count.append(0)
        tok1 = "x"
        tok2 = "o"
        if ply == "o":
            tok1 = "o"
            tok2 = "x"
        for i in range(3):
            for j in range(3):
                if board[x+i][y+j] == tok2:
                    count[i] = 0
                    break
                if board[x+i][y+j] == tok1:
                    count[i] += 1
        for i in range(3):
            for j in range(3):
                if board[x+j][y+i] == tok2:
                    count[i+3] = 0
                    break
                if board[x+j][y+i] == tok1:
                    count[i+3] += 1
        for i in range(3):
            if board[x+i][y+i] == tok2:
                count[6] = 0
                break
            if board[x+i][y+i] == tok1:
                count[6] += 1
        d1=0
        d2=0
        if board[x+1][y+1] == "-":
            d1 += 1
        if board[x+1][y+1] == tok1 :
            d2 += 1
        if board[x+2][y] == "-":
            d1 += 1
        if board[x+2][y] == tok1:
            d2 += 1
        if board[x][y+2] == "-":
            d1 += 1
        if board[x][y+2] == tok1:
            d2 += 1
        if d1+d2==3:
            count[7]=d2
        weight = 0
        for i in range(8):
            if count[i] == 1:
                weight += 3
            if count[i] == 2:
                weight += 11
        return weight

    def board_pattern_checker(self, board, ply, blocks):
        count = []
        val = []
        for i in range(8):
            count.append(0)
            val.append(0)
        tok1 = "x"
        tok2 = "o"
        if ply == "o":
            tok1 = "o"
            tok2 = "x"
        for i in range(3):
            for j in range(3):
                if board[i][j] == tok2 or board[i][j] == "d":
                    count[i] = 0
                    break
                else:
                    if board[i][j] == tok1:
                        count[i] += 1
                    val[i] += blocks[i][j]
        for i in range(3):
            for j in range(3):
                if board[j][i] == tok2 or board[j][i] == "d":
                    count[i+3] = 0
                    break
                else:
                    if board[j][i] == tok1:
                        count[i+3] += 1
                    val[i+3] += blocks[j][i]
        for i in range(3):
            if board[i][i] == tok2 or board[i][i] == "d":
                count[6] = 0
                break         
            else:
                if board[i][i] == tok1:
                    count[6] += 1
                val[6] += blocks[i][i]
        d1=0
        d2=0
        if board[1][1] == "-":
            d1 += 1
        if board[1][1] == tok1 :
            d2 += 1
        if board[2][0] == "-":
            d1 += 1
        if board[2][0] == tok1:
            d2 += 1
        if board[0][2] == "-":
            d1 += 1
        if board[0][2] == tok1:
            d2 += 1
        if d1+d2==3:
            count[7] = d2
            val[7] = blocks[0][2] + blocks[2][0] + blocks[1][1]
        weight = 0
        for i in range(8):
            if count[i] == 1:
                weight += val[i] * 1.5
            elif count[i] == 2:
                weight += val[i] * 3
            elif count[i] == 3:
                weight += val[i] * 100
            else:
                weight += val[i]
        return weight

    def heuristic(self, board, move, ply):
        k = move[0]

        tok1 = "x"
        tok2 = "o"
        if ply == "o":
            tok1 = "o"
            tok2 = "x"

        blocks = ([[ 0 for i in range(3)] for j in range(3)], [[ 0 for i in range(3)] for j in range(3)])

        temp_small_board = board.small_boards_status
        temp_big_board = board.big_boards_status
        for i in range(3):
            for j in range(3):
                if temp_small_board[k][i][j] == tok1:
                    blocks[k][i][j] = 30
                elif temp_small_board[k][i][j] == tok2 or temp_small_board[k][i][j] == "d":
                    blocks[k][i][j] = -1
                else:
                    blocks[k][i][j] = self.miniB_pattern_checker(temp_big_board[k], 3*i, 3*j, tok1)

        val = self.board_pattern_checker(temp_small_board[k], ply, blocks[k])
        return val

    def revert(self, board, move, fl):
        board.big_boards_status[move[0]][move[1]][move[2]] = "-"
        x = move[1]/3
        y = move[2]/3
        k = move[0]
        if fl or board.small_boards_status[k][x][y] == "d":
            board.small_boards_status[k][x][y] = "-"
        return

    def minimax(self, ply, game_board, currdepth, maxdepth, alpha, beta, old_move):
        status = game_board.find_terminal_state()
        if status[1] == "WON":
            if status[0] == self.ply_token:
                return 10**4, 0
            if status[0] == self.opp_token:
                return -(10**4), 0
        if status[1] == "DRAW":
            return 0, 0
        if currdepth == maxdepth:
            # val = random.randrange(100)
            val = self.heuristic(game_board, old_move, self.ply_token) - self.heuristic(game_board, old_move, self.opp_token)
            return val, 0
        validmoves = game_board.find_valid_move_cells(old_move)
        index = 0
        if ply == self.ply_token:
            imax = float("-inf")
            for i in range(len(validmoves)):
                next_move = validmoves[i]
                ret_update = game_board.update(old_move, next_move, self.ply_token)
                if ret_update[1] == True and self.bonus == False:
                    self.bonus = True
                    v = self.minimax(self.ply_token, game_board,currdepth+1,maxdepth,alpha,beta,next_move)
                else:
                    self.bonus = False                    
                    v = self.minimax(self.opp_token, game_board,currdepth+1,maxdepth,alpha,beta,next_move)
                self.revert(game_board, next_move, ret_update[1])            
                if v[0] > imax:
                    imax = v[0]
                    index = i
                alpha = imax
                if beta < alpha:
                    break
            return imax, index
        if ply == self.opp_token:
            imin = float("inf")
            for i in range(len(validmoves)):
                next_move = validmoves[i]
                ret_update = game_board.update(old_move, next_move, self.opp_token)
                if ret_update[1] == True and self.bonus == False:
                    self.bonus = True
                    v = self.minimax(self.opp_token, game_board,currdepth+1,maxdepth,alpha,beta,next_move)
                else:
                    self.bonus = False                    
                    v = self.minimax(self.ply_token, game_board,currdepth+1,maxdepth,alpha,beta,next_move)
                self.revert(game_board, next_move, ret_update[1])            
                if v[0] < imin:
                    imin = v[0]
                    index = i
                beta = imin
                if beta < alpha:
                    break
            return imin, index

    def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
        if old_move == (-1, -1, -1):
            return (0, 1, 1)
        cells = board.find_valid_move_cells(old_move)
        if flag == "x":
            self.ply_token = "x"
            self.opp_token = "o"
        elif flag == "o":
            self.ply_token = "o"
            self.opp_token = "x"
        if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == flag:
            self.bonus = True
        v = self.minimax(flag, board, 0, 4, float("-inf"), float("inf"), old_move)
        return cells[v[1]]

