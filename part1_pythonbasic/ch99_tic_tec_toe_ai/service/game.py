import pygame
from service.ai import TicTacToeAI

# Constants
WIDTH, HEIGHT = 300, 350
BOARD_SIZE = 300
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = BOARD_SIZE // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5
SPACE = 25

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.running = True
        self.current_player = 'O'
        self.ai = TicTacToeAI()

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.font = pygame.font.Font(None, 40)
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_turn_text()

    def draw_grid(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, 50))
        for row in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen, BLACK, (0, row * SQUARE_SIZE + 50), (BOARD_SIZE, row * SQUARE_SIZE + 50), LINE_WIDTH)
            pygame.draw.line(self.screen, BLACK, (row * SQUARE_SIZE, 50), (row * SQUARE_SIZE, BOARD_SIZE + 50), LINE_WIDTH)
        pygame.display.update()

    def draw_turn_text(self):
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, 50))
        turn_text = "Your Turn (O)" if self.current_player == 'O' else "AI's Turn (X)"
        text_surface = self.font.render(turn_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 25))
        self.screen.blit(text_surface, text_rect)
        pygame.display.update()

    def draw_figures(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 'O':
                    pygame.draw.circle(self.screen, BLUE, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2 + 50)), CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[row][col] == 'X':
                    pygame.draw.line(self.screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE + 50), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50), CROSS_WIDTH)
                    pygame.draw.line(self.screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE + 50), (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50), CROSS_WIDTH)
        pygame.display.update()

    def handle_click(self, x, y):
        if y < 50:
            return

        col = x // SQUARE_SIZE
        row = (y - 50) // SQUARE_SIZE
        if self.board[row][col] == ' ':
            self.board[row][col] = 'O'
            self.current_player = 'X'
            self.draw_turn_text()

            if self.ai.check_winner(self.board):
                self.running = False
            if self.running:
                ai_move = self.ai.best_move(self.board)
                if ai_move != (-1, -1):
                    self.board[ai_move[0]][ai_move[1]] = 'X'
                    self.current_player = 'O'
                    self.draw_turn_text()
            self.draw_figures()
            if self.ai.check_winner(self.board):
                self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.handle_click(x, y)
        pygame.quit()