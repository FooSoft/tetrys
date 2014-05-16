#!/usr/bin/env python

import pygame


#
# Tetrad
#

class Tetrad:
    block_rotations = 4
    block_configs = [
        [[[1, 0], [1, 1], [1, 2], [1, 3]], [[0, 1], [1, 1], [2, 1], [3, 1]], [[1, 0], [1, 1], [1, 2], [1, 3]], [[0, 1], [1, 1], [2, 1], [3, 1]]], # Shape_I
        [[[0, 1], [1, 1], [2, 1], [1, 2]], [[1, 0], [1, 1], [2, 1], [1, 2]], [[1, 0], [0, 1], [1, 1], [2, 1]], [[1, 0], [0, 1], [1, 1], [1, 2]]], # Shape T
        [[[0, 0], [0, 1], [1, 0], [1, 1]], [[0, 0], [0, 1], [1, 0], [1, 1]], [[0, 0], [0, 1], [1, 0], [1, 1]], [[0, 0], [0, 1], [1, 0], [1, 1]]], # Shape O
        [[[1, 0], [1, 1], [1, 2], [2, 2]], [[2, 0], [2, 1], [1, 1], [0, 1]], [[0, 0], [1, 0], [1, 1], [1, 2]], [[0, 1], [1, 1], [2, 1], [0, 2]]], # Shape L
        [[[1, 0], [1, 1], [1, 2], [0, 2]], [[2, 1], [2, 2], [1, 1], [0, 1]], [[1, 0], [2, 0], [1, 1], [1, 2]], [[0, 0], [1, 1], [2, 1], [0, 1]]], # Shape J
        [[[1, 1], [2, 1], [0, 2], [1, 2]], [[1, 0], [1, 1], [2, 1], [2, 2]], [[1, 1], [2, 1], [0, 2], [1, 2]], [[1, 0], [1, 1], [2, 1], [2, 2]]], # Shape S
        [[[0, 1], [1, 1], [1, 2], [2, 2]], [[1, 1], [1, 2], [2, 0], [2, 1]], [[0, 1], [1, 1], [1, 2], [2, 2]], [[1, 1], [1, 2], [2, 0], [2, 1]]]  # Shape Z
    ]


    def __init__(self, config=0, position=(0, 0), rotation=0):
        self.config = config
        self.position = position
        self.rotation = rotation

    
    def layout(self):
        return self.block_configs[self.config][self.rotations]



#
# Board
#

class Board:
    grid_color = pygame.Color(0xff, 0xff, 0xff, 0xff)
    block_colors = [
        pygame.Color(0xff, 0xff, 0xff, 0xff), # White
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

        grid_screen_dims = grid_dims[0]*block_dims[0], grid_dims[1]*block_dims[1]
        self.grid_rect = pygame.Rect(grid_position, grid_screen_dims)

        self.blocks = [[0]*grid_dims[1] for i in range(grid_dims[0])]


    def render(self, surface):
        self.render_frame(surface)
        self.render_blocks(surface)


    def render_frame(self, surface):
        pygame.draw.rect(surface, self.grid_color, self.grid_rect, 1)


    def render_blocks(self, surface):
        for y in xrange(self.grid_dims[1]):
            for x in xrange(self.grid_dims[0]):
                self.render_block(surface, self.blocks[x][y], (x, y))


    def render_block(self, surface, color, position):
        block_rect = self.block_screen_rect(position)
        pygame.draw.rect(surface, self.grid_color, block_rect, 1 if color == 0 else 0)


    def block_screen_rect(self, position):
        top_left = self.grid_rect.x+self.block_dims[0]*position[0], self.grid_rect.y+self.block_dims[1]*position[1]
        return pygame.Rect(top_left, self.block_dims)


#
# Game
#

class Game:
    def __init__(self):
        self.board = Board((10, 10), (10, 20), 1, (20, 20))


    def render(self, surface):
        self.board.render(surface)


    def advance(self):
        pass


    def move_left(self):
        pass


    def move_right(self):
        pass


    def move_down(self):
        pass


    def rotate(self):
        pass


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


    def move_right(self):
        print 'right'


    def move_left(self):
        print 'left'


    def move_down(self):
        print 'down'


    def rotate(self):
        print 'rotate'


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
