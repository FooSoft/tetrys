#!/usr/bin/env python

import pygame


#
# Tetrad
#

class Tetrad:
    block_rotations = 4
    block_configs = [
        (1, [[(1, 0), (1, 1), (1, 2), (1, 3)], [(0, 1), (1, 1), (2, 1), (3, 1)], [(1, 0), (1, 1), (1, 2), (1, 3)], [(0, 1), (1, 1), (2, 1), (3, 1)]]), # Shape_I
        (2, [[(0, 1), (1, 1), (2, 1), (1, 2)], [(1, 0), (1, 1), (2, 1), (1, 2)], [(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (0, 1), (1, 1), (1, 2)]]), # Shape T
        (3, [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)]]), # Shape O
        (4, [[(1, 0), (1, 1), (1, 2), (2, 2)], [(2, 0), (2, 1), (1, 1), (0, 1)], [(0, 0), (1, 0), (1, 1), (1, 2)], [(0, 1), (1, 1), (2, 1), (0, 2)]]), # Shape L
        (5, [[(1, 0), (1, 1), (1, 2), (0, 2)], [(2, 1), (2, 2), (1, 1), (0, 1)], [(1, 0), (2, 0), (1, 1), (1, 2)], [(0, 0), (1, 1), (2, 1), (0, 1)]]), # Shape J
        (6, [[(1, 1), (2, 1), (0, 2), (1, 2)], [(1, 0), (1, 1), (2, 1), (2, 2)], [(1, 1), (2, 1), (0, 2), (1, 2)], [(1, 0), (1, 1), (2, 1), (2, 2)]]), # Shape S
        (7, [[(0, 1), (1, 1), (1, 2), (2, 2)], [(1, 1), (1, 2), (2, 0), (2, 1)], [(0, 1), (1, 1), (1, 2), (2, 2)], [(1, 1), (1, 2), (2, 0), (2, 1)]])  # Shape Z
    ]


    def __init__(self, config=0, position=(0, 0), rotation=0):
        self.config = config
        self.position = position
        self.rotation = rotation


    def color(self):
        return self.block_configs[self.config][0]


    def layout(self):
        layout = self.block_configs[self.config][1][self.rotation]
        return map(lambda p: (self.position[0]+p[0], self.position[1]+p[1]), layout)


    def moved_left(self):
        return Tetrad(self.config, (self.position[0]-1, self.position[1]), self.rotation)


    def moved_right(self):
        return Tetrad(self.config, (self.position[0]+1, self.position[1]), self.rotation)


    def moved_down(self):
        return Tetrad(self.config, (self.position[0], self.position[1]+1), self.rotation)


    def rotated(self):
        return Tetrad(self.config, self.position, (self.rotation + 1) % self.block_rotations)


#
# Board
#

class Board:
    grid_color = pygame.Color(0xff, 0xff, 0xff, 0xff)
    block_colors = [
        pygame.Color(0x00, 0x00, 0x00, 0xff), # Black
        pygame.Color(0x00, 0xff, 0xff, 0xff), # Cyan
        pygame.Color(0x00, 0x00, 0xff, 0xff), # Blue
        pygame.Color(0xff, 0x80, 0x00, 0xff), # Orange
        pygame.Color(0xff, 0xff, 0x00, 0xff), # Yellow
        pygame.Color(0x00, 0xff, 0x00, 0xff), # Green
        pygame.Color(0x80, 0x00, 0x80, 0xff), # Purple
        pygame.Color(0xff, 0x00, 0x00, 0xff)  # Red
    ]


    def __init__(self, grid_position, grid_dims, grid_border_width, block_dims):
        self.grid_dims = grid_dims
        self.grid_border_width = grid_border_width
        self.block_dims = block_dims

        grid_screen_dims = grid_border_width*2+grid_dims[0]*block_dims[0], grid_border_width*2+grid_dims[1]*block_dims[1]
        self.grid_rect = pygame.Rect(grid_position, grid_screen_dims)

        self.blocks = [[0]*grid_dims[1] for i in range(grid_dims[0])]


    def render(self, surface, tetrad):
        self.render_frame(surface)
        self.render_blocks(surface)
        self.render_tetrad(surface, tetrad)


    def render_frame(self, surface):
        pygame.draw.rect(surface, self.grid_color, self.grid_rect, 1)


    def render_blocks(self, surface):
        for y in xrange(self.grid_dims[1]):
            for x in xrange(self.grid_dims[0]):
                self.render_block(surface, self.blocks[x][y], (x, y))


    def render_tetrad(self, surface, tetrad):
        for point in tetrad.layout():
            self.render_block(surface, tetrad.color(), point)


    def render_block(self, surface, color, position):
        block_rect = self.block_screen_rect(position)
        pygame.draw.rect(surface, self.block_colors[color], block_rect)


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
            if self.blocks[point[0]][point[1]] != 0:
                return False

        return True


#
# Game
#

class Game:
    def __init__(self):
        self.board = Board((10, 10), (10, 20), 1, (20, 20))
        self.tetrad = Tetrad()


    def render(self, surface):
        self.board.render(surface, self.tetrad)


    def advance(self):
        pass


    def try_tetrad_action(self, tetrad):
        if self.board.can_place_tetrad(tetrad):
            self.tetrad = tetrad


    def move_left(self):
        self.try_tetrad_action(self.tetrad.moved_left())


    def move_right(self):
        self.try_tetrad_action(self.tetrad.moved_right())


    def move_down(self):
        self.try_tetrad_action(self.tetrad.moved_down())


    def rotate(self):
        self.try_tetrad_action(self.tetrad.rotated())


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

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None


    def update(self):
        self.game.advance()
        self.game.render(self.surface)

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
                self.game.move_left()
            elif event.key == pygame.K_RIGHT:
                self.game.move_right()
            elif event.key == pygame.K_DOWN:
                self.game.move_down()
            elif event.key == pygame.K_UP:
                self.game.rotate()
            elif event.key == pygame.K_ESCAPE:
                return False

        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value > 0: self.game.move_right()
                elif event.value < 0: self.game.move_left()
            elif event.axis == 1:
                if event.value > 0: self.game.move_down()
                elif event.value < 0: self.game.rotate()

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
