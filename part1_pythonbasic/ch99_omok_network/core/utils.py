from config.constants import CELL_SIZE, BOARD_TOP_OFFSET, CLICK_RADIUS

def is_click_near_cross(x, y, col, row):
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2 + BOARD_TOP_OFFSET
    dx = x - center_x
    dy = y - center_y
    return dx * dx + dy * dy <= CLICK_RADIUS * CLICK_RADIUS