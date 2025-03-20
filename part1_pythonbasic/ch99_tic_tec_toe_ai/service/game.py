import pygame
from service.ai import TicTacToeAI

WIDTH, HEIGHT = 300, 400
BOARD_SIZE = 300
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = BOARD_SIZE // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5
SPACE = 25

BUTTON_Y = 357
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 35

START_BUTTON_X = 40
RESET_BUTTON_X = 160

WHITE = (255, 255, 255)
LIGHT_GRAY = (230, 230, 230)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
LIGHT_RED = (255, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

class TicTacToe:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.font = pygame.font.Font(None, 40)
        self.button_font = pygame.font.Font(None, 30)
        self.ai = TicTacToeAI()
        self.running = False
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.running = False
        self.current_player = 'O'
        self.winner = None
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, 50))
        self.draw_grid()
        self.draw_turn_text("Press Start")
        self.draw_buttons()
        pygame.display.update()

    def start_game(self):
        self.board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.running = True
        self.current_player = 'O'
        self.winner = None
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, 50))
        self.draw_grid()
        self.draw_turn_text()
        self.draw_buttons()
        pygame.display.update()

    def draw_grid(self):
        for row in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen, BLACK, (0, row * SQUARE_SIZE + 50), (BOARD_SIZE, row * SQUARE_SIZE + 50), LINE_WIDTH)
            pygame.draw.line(self.screen, BLACK, (row * SQUARE_SIZE, 50), (row * SQUARE_SIZE, BOARD_SIZE + 50), LINE_WIDTH)
        pygame.display.update()

    def draw_turn_text(self, message=None):
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, 50))
        text = message if message else ("Your Turn (O)" if self.current_player == 'O' else "AI's Turn (X)")
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 25))
        self.screen.blit(text_surface, text_rect)
        pygame.display.update()

    def draw_figures(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 'O':
                    pygame.draw.circle(self.screen, BLUE, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2 + 50)), CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[row][col] == 'X':
                    pygame.draw.line(self.screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE + 50),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50), CROSS_WIDTH)
                    pygame.draw.line(self.screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE + 50),
                                     (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50), CROSS_WIDTH)
        pygame.display.update()

    def draw_buttons(self):
        pygame.draw.rect(self.screen, LIGHT_GRAY, (0, 350, WIDTH, 50))

        start_color = DARK_GRAY if self.running else GREEN
        reset_color = LIGHT_RED  

        pygame.draw.rect(self.screen, start_color, (START_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=8)
        pygame.draw.rect(self.screen, reset_color, (RESET_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=8)

        start_text = self.button_font.render("Start", True, WHITE)
        reset_text = self.button_font.render("Reset", True, WHITE)

        self.screen.blit(start_text, start_text.get_rect(center=(START_BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))
        self.screen.blit(reset_text, reset_text.get_rect(center=(RESET_BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))

        pygame.display.update()

    def handle_click(self, x, y):
        if START_BUTTON_X <= x <= START_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            if not self.running:
                self.start_game()
            return

        if RESET_BUTTON_X <= x <= RESET_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.reset_game()
            return

        if y < 50 or not self.running:
            return

        col = x // SQUARE_SIZE
        row = (y - 50) // SQUARE_SIZE
        if self.board[row][col] == ' ':
            self.board[row][col] = 'O'
            self.current_player = 'X'
            self.draw_figures()
            self.draw_turn_text()

            winner = self.check_winner()
            if winner:
                self.draw_figures()
                self.end_game(winner)
                return

            ai_move = self.ai.best_move(self.board)
            if ai_move != (-1, -1):
                self.board[ai_move[0]][ai_move[1]] = 'X'
                self.current_player = 'O'
                self.draw_figures()
                self.draw_turn_text()

            winner = self.check_winner()
            if winner:
                self.draw_figures()
                self.end_game(winner)

    def check_winner(self):
        winner = self.ai.check_winner(self.board)
        if winner == 'O':
            return "You Win!"
        elif winner == 'X':
            return "AI Wins!"
        elif winner == "Draw":
            return "Draw!"
        return None

    def end_game(self, message):
        self.running = False
        self.draw_turn_text(message)
        self.draw_buttons()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.handle_click(x, y)