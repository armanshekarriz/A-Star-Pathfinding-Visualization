import pygame
import enum
from enum import Enum

### block and grid structure for the GUI

# block types and colors for each
class B_Type(Enum):

    # types of blocks --> normal, walls, start selection, end selection, open, closed, final path
    # need to set these out and give each their own color
    normal_block = 1
    wall_block = 2
    start_block = 3
    end_block = 4
    open_block = 5
    closed_block = 6
    path_block = 7

# colors for blocks
type_color = {
    B_Type.normal_block: [0, 0, 0], # black
    B_Type.wall_block: [255, 255, 255], # white
    B_Type.start_block: [20, 100, 20], # darker green
    B_Type.end_block: [180, 45, 45], # darker red
    B_Type.open_block: [0, 0, 255], # blue
    B_Type.closed_block: [255, 0, 0], # red
    B_Type.path_block: [0, 255, 0], # green for final path
}

# block class and functions
class Block:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col

        self.x = row * width
        self.y = col * width
        self.width = width

        self.type = B_Type.normal_block

        self.g = 0
        self.h = 0

        self.parent = None
        self.rect = pygame.Rect(self.x, self.y, width, width)

    def get_rect(self):
        return self.rect

    def set_normal(self):
        self.type = B_Type.normal_block

    def set_wall(self):
        self.type = B_Type.wall_block

    def set_start(self):
        self.type = B_Type.start_block

    def set_end(self):
        self.type = B_Type.end_block

    def set_open(self):
        self.type = B_Type.open_block

    def set_closed(self):
        self.type = B_Type.closed_block

    def set_path(self):
        self.type = B_Type.path_block

    def draw(self, board, color):
        pygame.draw.rect(board, color, self.rect)

    def f(self):
        return self.g + self.h

# grid structure
class Grid:
    def __init__(self, width, height, size):
        self.block_size = size

        self.width = width
        self.height = height

        self.rows = width // size
        self.cols = height // size
        
        self.grid = self.make_grid()
        self.currentBlock = self.grid[0][0]

    # make the grid
    def make_grid(self):
        grid = []
        for y in range(self.cols):
            row = []
            for x in range(self.rows):
                item = Block(x, y, self.block_size)
                row.append(item)

            grid.append(row)
        return grid

    def draw_grid(self, board, switch):
        for col in range(len(self.grid)):
            for row in range(len(self.grid[0])):
                self.grid[col][row].draw(board, switch.get(self.grid[col][row].type))

        for x in range(0, self.width, self.block_size):
            pygame.draw.line(board, [212, 212, 212], (x, 0), (x, self.height))
            for y in range(0, self.height, self.block_size):
                pygame.draw.line(board, [212, 212, 212], (0, y), (self.width, y))

        pygame.draw.line(board, [212, 212, 212], (self.width, 0), (self.width, self.height))

        pygame.display.update()

    def find_adjacent(self, block):
        neighbors = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                else:
                    check_x = block.row + x
                    check_y = block.col + y

                    if check_x >= 0 and check_x < self.rows and check_y >= 0 and check_y < self.cols:
                        neighbors.append(self.grid[check_y][check_x])
        return neighbors

    def start_or_end(self, block_type):
        for col in self.grid:
            for value in col:
                if value.type == block_type:
                    return True, value

        return False, None

    def find_start(self):
        for col in self.grid:
            for value in col:
                if value.type == B_Type.start_block:
                    return value.row, value.col

        return None

    def find_end(self):
        for col in self.grid:
            for value in col:
                if value.type == B_Type.end_block:
                    return value.row, value.col

        return None