import pygame
import tkinter
from tkinter import *
from tkinter import messagebox

import pathfinder as pf
import block_grid as bg

pygame.init()

# size of the window and blocks
WIDTH = 1005
HEIGHT = 795
BLOCK_SIZE = 15

# initialize global variables
board = None
TYPE = None
grid = None
game_started = False

def main():
    global board, TYPE, grid, game_started

    # set block type to start block by default
    TYPE = bg.B_Type.start_block

    board = pygame.display.set_mode((WIDTH, HEIGHT))

    # make board color black
    board.fill((0, 0, 0))
    pygame.display.set_caption("A* Pathfinding: Select Start, End, and Boundaries/Walls")
    pygame.font.init()

    grid_ = bg.Grid(WIDTH, HEIGHT, BLOCK_SIZE)
    grid = grid_.grid

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif game_started == False:
                if pygame.mouse.get_pressed()[0]:
                    for col in grid:
                        for value in col:
                            rect = value.get_rect()
                            if rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                                if TYPE == bg.B_Type.start_block:
                                    found, block = grid_.start_or_end(bg.B_Type.start_block)
                                    if found:
                                        block.set_normal()
                                    value.set_start()
                                elif TYPE == bg.B_Type.end_block:
                                    found, block = grid_.start_or_end(bg.B_Type.end_block)
                                    if found:
                                        block.set_normal()
                                    value.set_end()
                                else:
                                    value.set_wall()

                elif pygame.mouse.get_pressed()[2]:
                    for col in grid:
                        for value in col:
                            rect = value.get_rect()
                            if rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                                value.set_normal()

                # if its a key press, set type to start with a, end with s, wall with d
                # use space to begin visualizer
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        TYPE = bg.B_Type.start_block
                    if event.key == pygame.K_s:
                        TYPE = bg.B_Type.end_block
                    if event.key == pygame.K_d:
                        TYPE = bg.B_Type.wall_block
                    if event.key == pygame.K_SPACE:
                        if grid_.find_start() == None or grid_.find_end() == None:
                            messagebox.showerror('ERROR', 'Start and End not Selected, Please Choose Before Start')
                            main()
                        elif grid_.find_start() != None and grid_.find_end() != None:
                            game_started = True
                            a_star = pf.Pathfinder(grid_)
                            a_star.find_path(lambda: grid_.draw_grid(board, bg.type_color), grid_.find_start(), grid_.find_end())
        board.fill((0, 0, 0))
        grid_.draw_grid(board, bg.type_color)

main()