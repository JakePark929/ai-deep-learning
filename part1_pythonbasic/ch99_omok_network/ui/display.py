import pygame
from config.constants import *

def draw_board(screen):
    screen.fill(BOARD_COLOR)
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 50))
    pygame.draw.rect(screen, LIGHT_GRAY, (0, HEIGHT - 50, WIDTH, 50))

    for i in range(GRID_SIZE):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE + CELL_SIZE // 2, 50),
                         (i * CELL_SIZE + CELL_SIZE // 2, HEIGHT - 50), 1)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE + CELL_SIZE // 2 + 50),
                         (WIDTH, i * CELL_SIZE + CELL_SIZE // 2 + 50), 1)
    pygame.display.update()

def draw_buttons(screen, running):
    start_color = DARK_GRAY if running else GREEN
    reset_color = LIGHT_RED

    pygame.draw.rect(screen, start_color, (START_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=8)
    pygame.draw.rect(screen, reset_color, (RESET_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=8)

    button_font = pygame.font.Font(None, 30)
    start_text = button_font.render("Start", True, WHITE)
    reset_text = button_font.render("Reset", True, WHITE)

    screen.blit(start_text, start_text.get_rect(center=(START_BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))
    screen.blit(reset_text, reset_text.get_rect(center=(RESET_BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))
    pygame.display.update()

def draw_stones(screen, board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 'B':
                pygame.draw.circle(screen, STONE_BLACK,
                                   (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2 + 50),
                                   CELL_SIZE // 3)
            elif board[row][col] == 'W':
                pygame.draw.circle(screen, STONE_WHITE,
                                   (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2 + 50),
                                   CELL_SIZE // 3)
    pygame.display.update()

def display_turn(screen, message=None, color=BLACK, current_player=None):
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 50))
    font = pygame.font.Font(None, 40)

    if message:
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 25))
        screen.blit(text_surface, text_rect)
    else:
        turn_text = "Now Turn:"
        text_surface = font.render(turn_text, True, BLACK)
        if current_player is None:
            current_player = 'B'
        stone_color = STONE_BLACK if current_player == 'B' else STONE_WHITE
        text_width, _ = text_surface.get_size()
        total_width = text_width + 35
        start_x = (WIDTH - total_width) // 2
        text_rect = text_surface.get_rect(midleft=(start_x, 25))
        stone_x = start_x + text_width + 20
        stone_y = 25
        screen.blit(text_surface, text_rect)
        pygame.draw.circle(screen, stone_color, (stone_x, stone_y), 15)
        pygame.draw.circle(screen, BLACK, (stone_x, stone_y), 15, 2)
    pygame.display.update()