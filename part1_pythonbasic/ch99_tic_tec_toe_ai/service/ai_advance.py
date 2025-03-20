import math

class TicTacToeAI:
    # Check if there is a winner
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
    
    # Minimax algorithm
    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner(board)

        # ✅ 즉시 승리하는 경우 높은 점수 부여 (방어보다 공격을 우선하도록 강제)
        if winner == 'O':
            return 1000 - depth  # ✅ AI가 이기면 높은 점수
        elif winner == 'X':
            return -1000 + depth  # ✅ 상대가 이기면 큰 패널티
        elif winner == "Draw":
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

    # Find the best move
    def best_move(self, board):
        # ✅ 1. AI가 즉시 승리할 수 있는 경우 먼저 선택
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    if self.check_winner(board) == 'O':  # ✅ 즉시 승리 가능하면 선택
                        return (row, col)
                    board[row][col] = ' '  # 원상복구

        # ✅ 2. 상대가 즉시 승리할 수 있는 경우 차단 (방어)
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    if self.check_winner(board) == 'X':  # ✅ 상대가 이길 가능성이 있으면 차단
                        board[row][col] = ' '  # 원상복구 후 방어 위치 반환
                        return (row, col)
                    board[row][col] = ' '  # 원상복구

        # ✅ 3. 첫 번째 수는 중앙을 선점 (중앙이 비어있다면 바로 둠)
        if board[1][1] == ' ':
            return (1, 1)

        # ✅ 4. 중앙이 차지되었으면, 코너를 선점
        corners = [(0,0), (0,2), (2,0), (2,2)]
        for row, col in corners:
            if board[row][col] == ' ':
                return (row, col)

        # ✅ 5. 중앙과 코너가 차지되었다면, 사이드를 선택
        sides = [(0,1), (1,0), (1,2), (2,1)]
        for row, col in sides:
            if board[row][col] == ' ':
                return (row, col)

        # ✅ 6. 위의 조건을 만족하지 않으면, 기존 Minimax 알고리즘 적용
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