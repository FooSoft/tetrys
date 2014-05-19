#!/usr/bin/env python

import pygame
import random


#
# Tetrad
#

class Tetrad:
    block_rotations = 4
    block_configs = [
        (1, 0x00f0222200f02222), # Shape I
        (2, 0x0232007202620270), # Shape T
        (3, 0x0033003300330033), # Shape O
        (4, 0x0170022300740622), # Shape L
        (5, 0x0071022604700322), # Shape J
        (6, 0x0462036004620360), # Shape S
        (7, 0x0264063002640630)  # Shape Z
    ]


    def __init__(self, position, config, rotation):
        self.position = position
        self.config = config
        self.rotation = rotation


    def color(self):
        return self.block_configs[self.config][0]


    def layout(self):
        layout = list()
        mask = self.block_configs[self.config][1] >> (16 * self.rotation)
        for bit in xrange(16):
            position = bit % 4, bit / 4
            if mask & (1 << bit):
                layout.append((self.position[0] + position[0], self.position[1] + position[1]))
        return layout


    def moved_left(self):
        return Tetrad((self.position[0]-1, self.position[1]), self.config, self.rotation)


    def moved_right(self):
        return Tetrad((self.position[0]+1, self.position[1]), self.config, self.rotation)


    def moved_down(self):
        return Tetrad((self.position[0], self.position[1]+1), self.config, self.rotation)


    def rotated(self):
        return Tetrad(self.position, self.config, (self.rotation + 1) % self.block_rotations)


    @staticmethod
    def random(position=(0, 0)):
        config = random.randrange(len(Tetrad.block_configs))
        rotation = random.randrange(Tetrad.block_rotations)
        return Tetrad(position, config, rotation)


#
# Board
#

class Board:
    border_color = 0xffffff
    grid_color = 0x808080
    block_colors = [
        0x000000, # Black
        0x00ffff, # Cyan
        0x0000ff, # Blue
        0xff8000, # Orange
        0xffff00, # Yellow
        0x00ff00, # Green
        0x800080, # Purple
        0xff0000, # Red
    ]


    def __init__(self, grid_position, grid_dims, grid_border_width, block_dims):
        self.grid_dims = grid_dims
        self.grid_border_width = grid_border_width
        self.block_dims = block_dims

        grid_screen_dims = grid_border_width*2 + grid_dims[0]*block_dims[0], grid_border_width*2 + grid_dims[1]*block_dims[1]
        self.grid_rect = pygame.Rect(grid_position, grid_screen_dims)

        self.blocks = [[0]*grid_dims[0] for i in range(grid_dims[1])]


    def render(self, surface, tetrad):
        self.render_frame(surface)
        self.render_blocks(surface)
        self.render_tetrad(surface, tetrad)


    def render_frame(self, surface):
        pygame.draw.rect(surface, self.border_color, self.grid_rect, self.grid_border_width)


    def render_blocks(self, surface):
        for y in xrange(self.grid_dims[1]):
            for x in xrange(self.grid_dims[0]):
                self.render_block(surface, self.blocks[y][x], (x, y))


    def render_tetrad(self, surface, tetrad):
        color = tetrad.color()
        for point in tetrad.layout():
            self.render_block(surface, color, point)


    def render_block(self, surface, color, position):
        block_rect = self.block_screen_rect(position)
        pygame.draw.rect(surface, self.block_colors[color], block_rect)
        if color != 0:
            pygame.draw.rect(surface, self.grid_color, block_rect, 1)


    def block_screen_rect(self, position):
        top_left = (
            self.grid_border_width+self.grid_rect.x+self.block_dims[0]*position[0],
            self.grid_border_width+self.grid_rect.y+self.block_dims[1]*position[1]
        )
        return pygame.Rect(top_left, self.block_dims)


    def can_place_tetrad(self, tetrad):
        for point in tetrad.layout():
            if point[0] < 0 or point[1] < 0:
                return False
            if point[0] >= self.grid_dims[0] or point[1] >= self.grid_dims[1]:
                return False
            if self.blocks[point[1]][point[0]] != 0:
                return False

        return True


    def place_tetrad(self, tetrad):
        color = tetrad.color()
        for point in tetrad.layout():
            self.blocks[point[1]][point[0]] = color


    def settle(self):
        row_src = row_dst = self.grid_dims[1] - 1
        while row_dst >= 0:
            row_data = self.blocks[row_src] if row_src >= 0 else self.grid_dims[0] * [0]
            self.blocks[row_dst] = row_data
            row_src -= 1
            if 0 in row_data:
                row_dst -= 1


#
# Game
#

class Game:
    interval = 500

    def __init__(self):
        self.new_game()


    def new_game(self):
        self.reset_board()
        self.tetrad = Tetrad.random()
        self.tetrad_next = Tetrad.random()
        self.counter = 0
        self.active = True


    def end_game(self):
        self.reset_board()
        self.active = False


    def reset_board(self):
        border_width = 3
        block_dims = 20, 20
        padding = 10
        self.board = Board((padding, padding), (10, 20), border_width, block_dims)
        self.board_prev = Board((self.board.grid_rect.right+padding, padding), (4, 4), border_width, block_dims)


    def render(self, surface):
        self.board.render(surface, self.tetrad)
        self.board_prev.render(surface, self.tetrad_next)


    def advance(self, elapsed):
        if not self.active:
            return

        self.counter += elapsed
        if self.counter > self.interval:
            self.lower_tetrad()


    def try_placement(self, tetrad):
        if self.board.can_place_tetrad(tetrad):
            self.tetrad = tetrad
            return True

        return False


    def lower_tetrad(self):
        self.counter = 0
        if self.try_placement(self.tetrad.moved_down()):
            return

        self.board.place_tetrad(self.tetrad)
        self.board.settle()

        self.tetrad = self.tetrad_next
        self.tetrad_next = Tetrad.random()

        if not self.try_placement(self.tetrad):
            self.end_game()


    def input_left(self):
        self.try_placement(self.tetrad.moved_left())


    def input_right(self):
        self.try_placement(self.tetrad.moved_right())


    def input_down(self):
        self.lower_tetrad()


    def input_up(self):
        self.try_placement(self.tetrad.rotated())


#
# Engine
#

class Engine:
    def __init__(self):
        self.surface = None
        self.game = Game()


    def create(self, resolution):
        pygame.init()

        self.surface = pygame.display.set_mode(resolution, pygame.DOUBLEBUF)
        self.ticks = pygame.time.get_ticks()

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None


    def update(self):
        ticks = pygame.time.get_ticks()
        self.game.advance(ticks - self.ticks)
        self.game.render(self.surface)
        self.ticks = ticks

        pygame.display.flip()
        pygame.time.delay(1)

        event = pygame.event.poll()
        return self.handle_event(event)


    def destroy(self):
        self.surface = None

        if self.joystick is not None:
            self.joystick.quit()

        pygame.quit()


    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.game.input_left()
            elif event.key == pygame.K_RIGHT:
                self.game.input_right()
            elif event.key == pygame.K_DOWN:
                self.game.input_down()
            elif event.key == pygame.K_UP:
                self.game.input_up()
            elif event.key == pygame.K_ESCAPE:
                return False

        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value > 0: self.game.input_right()
                elif event.value < 0: self.game.input_left()
            elif event.axis == 1:
                if event.value > 0: self.game.input_down()
                elif event.value < 0: self.game.input_up()

        return True


#
# Entry
#

def main():
    engine = Engine()
    engine.create((800, 600))
    while engine.update():
        pass
    engine.destroy()

if __name__ == '__main__':
    main()
