def count_consecutive_stones(board, row, col, dr, dc, player):
    """ 특정 방향(dr, dc)으로 연속된 돌 개수 계산 """
    count = 0
    for step in range(1, 5):  # 최대 4개까지 체크
        r, c = row + dr * step, col + dc * step
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
            count += 1
        else:
            break
    return count

def is_three(board, row, col, player):
    """ 특정 위치에서 3개의 연속된 돌이 있는지 체크 """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 가로, 세로, 대각선 방향

    three_count = 0  # 삼의 개수 카운트
    for dr, dc in directions:
        count1 = count_consecutive_stones(board, row, col, dr, dc, player)
        count2 = count_consecutive_stones(board, row, col, -dr, -dc, player)
        if count1 + count2 == 2:  # 3개 연속된 경우 (자신 포함 3개)
            three_count += 1

    return three_count >= 2  # 쌍삼 여부 확인

def is_double_three(board, row, col, player):
    """ 쌍삼(삼삼) 체크: 현재 위치에 돌을 두었을 때 3이 두 개 이상인지 확인 """
    board[row][col] = player  # 돌을 둔 상태로 가정
    result = is_three(board, row, col, player)  # 삼삼 체크
    board[row][col] = ' '  # 돌을 다시 제거 (가상의 시뮬레이션이므로 원상복구)
    return result