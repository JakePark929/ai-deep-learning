import math

class TicTacToeAI:
    def check_winner(self, board):
        """ 현재 보드 상태에서 승자를 확인 """
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
        """ Minimax 알고리즘으로 최적의 수 찾기 """
        winner = self.check_winner(board)

        # ✅ 승리 / 패배 / 무승부 점수 설정
        if winner == 'X':  # AI가 이긴 경우
            return 10 - depth
        elif winner == 'O':  # 상대가 이긴 경우
            return -10 + depth
        elif winner == "Draw":
            return 0

        if is_maximizing:
            best_score = -math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = 'X'
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = 'O'
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = ' '
                        best_score = min(score, best_score)
            return best_score

    def best_move(self, board):
        """ AI가 후공(`X`)으로 최적의 수를 찾아서 둠 """
        # ✅ 1. AI(`X`)가 즉시 승리할 수 있는 경우 먼저 선택 (공격 우선)
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    if self.check_winner(board) == 'X':  
                        return (row, col)
                    board[row][col] = ' '  

        # ✅ 2. 상대(`O`)가 즉시 승리할 수 있는 경우 차단 (방어)
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    if self.check_winner(board) == 'O':  
                        board[row][col] = ' '  
                        return (row, col)
                    board[row][col] = ' '  

        # ✅ 3. 상대(`O`)의 첫 번째 수를 분석하여 최적의 위치 선택
        o_positions = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 'O']
        
        if len(o_positions) == 1:  # 첫 번째 수라면
            first_o = o_positions[0]
            if first_o == (1,1):  # 상대가 중앙에 둔 경우
                return (0, 0)  # 코너를 차지
            else:
                return (1, 1)  # 중앙을 차지하여 유리한 플레이 진행

        # ✅ 4. Minimax 실행 (최적의 수 탐색)
        best_score = -math.inf
        best_move = (-1, -1)

        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    score = self.minimax(board, 0, False)
                    board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move