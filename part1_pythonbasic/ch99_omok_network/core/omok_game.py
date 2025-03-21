import time
import pygame

from config.constants import *
from ui.messages import START_PROMPT
from ui.display import draw_board, draw_buttons, display_turn
from core.handler import handle_click

class OmokGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Omok - Five in a Row")
        self.font = pygame.font.Font(None, 40)
        self.button_font = pygame.font.Font(None, 30)
        self.forbidden_time = None
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'B'
        self.winner = None
        self.running = False  # 게임 비활성화 상태로 초기화
        self.forbidden_time = None

        draw_board(self.screen)
        draw_buttons(self.screen, self.running)
        display_turn(self.screen, START_PROMPT)

        pygame.display.update()  # 화면 갱신 추가

    def start_game(self):
        if self.running:  # 이미 실행 중이면 무시
            return
        self.reset_game()
        self.running = True  # 게임 시작 상태 변경
        display_turn(self.screen, current_player=self.current_player)

        # 버튼 다시 그리기 (Start 버튼을 비활성화된 색상으로)
        draw_buttons(self.screen, self.running)
        pygame.display.update()  # 화면 갱신 추가

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    handle_click(self, *event.pos)

            if self.forbidden_time and time.time() > self.forbidden_time:
                self.forbidden_time = None
                display_turn(self.screen, current_player=self.current_player)