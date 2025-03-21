import time

from config.constants import *
from ui.messages import (
    OUT_OF_BOUNDS,
    CELL_OCCUPIED,
    FORBIDDEN_DOUBLE_THREE,
    WINNER_TEXT
)
from service.rule import is_double_three, check_winner
from ui.display import draw_stones, display_turn

def handle_click(game, x, y):
    # Start 버튼 클릭 감지
    if START_BUTTON_X <= x <= START_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
        game.start_game()
        return

    # Reset 버튼 클릭 감지
    if RESET_BUTTON_X <= x <= RESET_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
        game.reset_game()
        return
    
    if not game.running:
        return

    # 보드 좌표 변환
    row = (y - 50) // CELL_SIZE
    col = x // CELL_SIZE

    # 유효 범위 확인
    if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
        game.forbidden_time = time.time() + EVENT_MESSAGE_TIME
        display_turn(game.screen, message=OUT_OF_BOUNDS, color=RED)
        return

    # 셀 점유 확인
    if game.board[row][col] != ' ':
        game.forbidden_time = time.time() + EVENT_MESSAGE_TIME
        display_turn(game.screen, message=CELL_OCCUPIED, color=RED)
        return

    # 쌍삼 금지
    if is_double_three(game.board, row, col, game.current_player):
        game.forbidden_time = time.time() + EVENT_MESSAGE_TIME
        display_turn(game.screen, message=FORBIDDEN_DOUBLE_THREE, color=RED)
        return

    # 정상적인 착수
    game.board[row][col] = game.current_player
    draw_stones(game.screen, game.board)

    # ✅ 승리 여부 체크
    winner = check_winner(game.board)
    if winner:
        game.winner = winner
        game.running = False
        display_turn(
            game.screen,
            message=WINNER_TEXT.format("Black" if winner == 'B' else "White"),
            color=BLUE
        )
        return

    # 다음 플레이어로 턴 넘기기
    game.current_player = 'W' if game.current_player == 'B' else 'B'
    display_turn(game.screen, current_player=game.current_player)