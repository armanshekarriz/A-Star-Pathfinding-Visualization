import block_grid as bg 
import time

class Pathfinder:
    def __init__(self, grid):
        self.grid_object = grid
        self.grid = grid.grid

    @staticmethod
    def get_distance(block_a, block_b):

        # distances between points in x and y direction
        x_dist = abs(block_a.x - block_b.x)
        y_dist = abs(block_a.y - block_b.y)

        if x_dist > y_dist:
            return 14 * y_dist + 10 * (x_dist - y_dist)
        else:
            return 14 * x_dist + 10 * (y_dist - x_dist)

    def retrace(self, start, end):
        path = []
        current_block = end

        while current_block != start:
            path.append(current_block)
            current_block = current_block.parent

        path.append(start)

        path.reverse()

        for block in path:
            block.set_path()

        # only show the path once found, no longer show open blocks and closed blocks searched
        self.show_path()

    def show_path(self):
        for row in self.grid:
            for block in row:
                if block.type == bg.B_Type.open_block:
                    block.set_normal()
                elif block.type == bg.B_Type.closed_block:
                    block.set_normal()

    def find_path(self, draw, start, end):
        start_block = self.grid[start[1]][start[0]]
        end_block = self.grid[end[1]][end[0]]

        open_list = []
        open_list.append(start_block)
        closed_list = []

        while len(open_list) > 0:
            current_block = open_list[0]

            for i in range(1, len(open_list)):
                if open_list[i].f() < current_block.f() or open_list[i].f() == current_block.f() and open_list[i].h < current_block.h:
                    current_block = open_list[i]

            open_list.remove(current_block)
            closed_list.append(current_block)
            current_block.set_closed()

            draw()

            if current_block == end_block:
                self.retrace(start_block, end_block)
                return

            for neighbour in self.grid_object.find_adjacent(current_block):
                if neighbour.type == bg.B_Type.wall_block or neighbour in closed_list:
                    continue

                new_cost = current_block.g + self.get_distance(current_block, neighbour)

                if new_cost < neighbour.g or neighbour not in open_list:
                    neighbour.g = new_cost
                    neighbour.h = self.get_distance(neighbour, end_block)
                    neighbour.parent = current_block

                    if neighbour not in open_list:
                        open_list.append(neighbour)
                        neighbour.set_open()