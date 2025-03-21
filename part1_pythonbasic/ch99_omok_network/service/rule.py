def count_consecutive_stones(board, row, col, dr, dc, player):
    count = 0
    for step in range(1, 6):  # 최대 5칸까지 검사
        r, c = row + dr * step, col + dc * step
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
            count += 1
        else:
            break
    return count

def is_three(board, row, col, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 가로, 세로, 대각선 검사
    three_count = 0  # 삼 개수 카운트

    for dr, dc in directions:
        count1 = count_consecutive_stones(board, row, col, dr, dc, player)
        count2 = count_consecutive_stones(board, row, col, -dr, -dc, player)

        r1, c1 = row + (count1 + 1) * dr, col + (count1 + 1) * dc
        r2, c2 = row - (count2 + 1) * dr, col - (count2 + 1) * dc

        # 열린 형태인지 확인 (양쪽이 비어 있어야 함)
        is_open = (
            (0 <= r1 < len(board) and 0 <= c1 < len(board[0]) and board[r1][c1] == ' ') and
            (0 <= r2 < len(board) and 0 <= c2 < len(board[0]) and board[r2][c2] == ' ')
        )

        # 연속된 돌이 정확히 2개이면 삼(three)으로 간주
        if count1 + count2 == 2 and is_open:
            three_count += 1  # 삼 카운트 증가

    return three_count  # 몇 개의 삼이 존재하는지 반환

def is_double_three(board, row, col, player):
    return is_three(board, row, col, player) >= 2  # 삼이 2개 이상이면 쌍삼

def check_winner(board):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == ' ':
                continue
            player = board[row][col]
            for dr, dc in directions:
                count1 = count_consecutive_stones(board, row, col, dr, dc, player)
                count2 = count_consecutive_stones(board, row, col, -dr, -dc, player)
                if count1 + count2 == 4:  # 정확히 5개
                    return player
    return None