import math

class TicTacToeAI:
    def check_winner(self, board):
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] and board[row][0] != ' ':
                return board[row][0]
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
                return board[0][col]
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
            return board[0][2]
        if all(board[row][col] != ' ' for row in range(3) for col in range(3)):
            return 'Draw'
        return None

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner(board)
        if winner == 'X':
            return -10 + depth
        elif winner == 'O':
            return 10 - depth
        elif winner == 'Draw':
            return 0
        if is_maximizing:
            best_score = -math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = ' '
                        best_score = min(score, best_score)
            return best_score

    def best_move(self, board):
        best_score = -math.inf
        move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    score = self.minimax(board, 0, False)
                    board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        return move