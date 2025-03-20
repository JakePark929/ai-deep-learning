import pygame
from config.constants import *

class OmokGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Omok - Five in a Row")
        self.font = pygame.font.Font(None, 40)
        self.button_font = pygame.font.Font(None, 30)
        self.reset_game()

    def reset_game(self):
        """ 게임을 초기화하고 Reset 버튼을 누르면 Start가 다시 활성화됨 """
        self.board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'B'
        self.winner = None
        self.running = False  # Start 버튼이 다시 활성화되도록 변경
        self.draw_board()
        self.draw_buttons()
        self.display_turn("Press Start!")

    def start_game(self):
        """ Start 버튼을 눌렀을 때 게임을 시작 (게임 진행 중이면 비활성화) """
        if self.running:
            return  # 🔥 게임이 진행 중이면 Start 버튼 클릭 무시

        self.reset_game()
        self.running = True
        self.display_turn()
        self.draw_buttons()

    def draw_board(self):
        """ 바둑판을 그린다 """
        self.screen.fill(BOARD_COLOR)
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, 50))
        pygame.draw.rect(self.screen, LIGHT_GRAY, (0, HEIGHT - 50, WIDTH, 50))

        for i in range(GRID_SIZE):
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE + CELL_SIZE // 2, 50),
                             (i * CELL_SIZE + CELL_SIZE // 2, HEIGHT - 50), 1)
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE + CELL_SIZE // 2 + 50),
                             (WIDTH, i * CELL_SIZE + CELL_SIZE // 2 + 50), 1)

        self.draw_buttons()
        pygame.display.update()

    def draw_buttons(self):
        """ Start & Reset 버튼을 그린다 (게임 진행 중이면 Start 버튼 비활성화) """
        start_color = DARK_GRAY if self.running else GREEN
        reset_color = LIGHT_RED

        pygame.draw.rect(self.screen, start_color, (START_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=8)
        pygame.draw.rect(self.screen, reset_color, (RESET_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=8)

        start_text = self.button_font.render("Start", True, WHITE)
        reset_text = self.button_font.render("Reset", True, WHITE)

        self.screen.blit(start_text, start_text.get_rect(center=(START_BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))
        self.screen.blit(reset_text, reset_text.get_rect(center=(RESET_BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))

        pygame.display.update()

    def display_turn(self, message=None):
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, 50))  # 상단 바 다시 그리기

        if message:
            # 게임 종료 메시지 표시 (승리/무승부 메시지)
            text_surface = self.font.render(message, True, BLACK)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, 25))
            self.screen.blit(text_surface, text_rect)
        else:
            # "Now Turn:" 텍스트 생성
            turn_text = "Now Turn:"
            text_surface = self.font.render(turn_text, True, BLACK)

            # 바둑돌 색상 선택
            stone_color = STONE_BLACK if self.current_player == 'B' else STONE_WHITE

            # 텍스트 크기 및 위치
            text_width, _ = text_surface.get_size()
            total_width = text_width + 35  # 바둑돌 크기(직경) 포함한 총 너비
            start_x = (WIDTH - total_width) // 2  # 전체 중앙 정렬 기준 위치

            # 텍스트 위치 설정
            text_rect = text_surface.get_rect(midleft=(start_x, 25))

            # 바둑돌 위치 설정 (텍스트 오른쪽)
            stone_x = start_x + text_width + 20  # 텍스트 끝 + 여백
            stone_y = 25

            # 화면에 텍스트와 바둑돌 그리기
            self.screen.blit(text_surface, text_rect)
            pygame.draw.circle(self.screen, stone_color, (stone_x, stone_y), 15)  # 바둑돌
            pygame.draw.circle(self.screen, BLACK, (stone_x, stone_y), 15, 2)  # 테두리 추가

        pygame.display.update()

    def draw_stones(self):
        """ 돌을 화면에 그린다 """
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 'B':
                    pygame.draw.circle(self.screen, STONE_BLACK,
                                       (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2 + 50),
                                       CELL_SIZE // 3)
                elif self.board[row][col] == 'W':
                    pygame.draw.circle(self.screen, STONE_WHITE,
                                       (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2 + 50),
                                       CELL_SIZE // 3)
        pygame.display.update()

    def handle_click(self, x, y):
        """ 마우스 클릭 이벤트 처리 """
        # 🔥 게임 진행 중이면 Start 버튼 클릭 무시
        if START_BUTTON_X <= x <= START_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.start_game()
            return

        # Reset 버튼은 언제든지 동작 가능
        if RESET_BUTTON_X <= x <= RESET_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.reset_game()
            return

        # 게임이 진행 중이 아니면 클릭을 무시
        if y < 50 or not self.running:
            return

        # 돌 두기 처리
        col = x // CELL_SIZE
        row = (y - 50) // CELL_SIZE
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            self.draw_stones()
            self.display_turn()

            winner = self.check_winner()
            if winner:
                self.display_turn(f"{'Black' if winner == 'B' else 'White'} Wins!")
                self.running = False  # 🔥 게임 종료
                self.draw_buttons()  # 버튼 UI 갱신

    def check_winner(self):
        """ 5개 연속된 돌이 있는지 체크 """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == ' ':
                    continue

                player = self.board[row][col]

                for dr, dc in directions:
                    count = 1
                    for step in range(1, 5):
                        r, c = row + dr * step, col + dc * step
                        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] == player:
                            count += 1
                        else:
                            break

                    if count == 5:
                        return player  # 승자 반환

        return None
    
    def run(self):
        """ 게임 실행 루프 """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.handle_click(x, y)