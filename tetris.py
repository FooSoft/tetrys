#!/usr/bin/env python

import pygame


class Board:
    def __init__(self, grid_position, grid_block_dims, block_dims):
        self.block_dims = block_dims
        self.grid_dims = grid_block_dims[0]*block_dims[0], grid_block_dims[1]*grid_block_dims[1]
        self.grid_color = pygame.Color(0xff, 0xff, 0xff, 0xff)
        self.grid_rect = pygame.Rect(grid_position, self.grid_dims)


    def render(self, surface):
        self.render_frame(surface)


    def render_frame(self, surface):
        pygame.draw.rect(surface, self.grid_color, self.grid_rect, 1)


    def advance(self):
        pass


class Engine:
    def __init__(self):
        self.board = Board((10, 10), (10, 20), (20, 20))
        self.surface = None


    def create(self, resolution):
        pygame.init()
        self.surface = pygame.display.set_mode(resolution, pygame.DOUBLEBUF)

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None


    def update(self):
        self.board.advance()
        self.board.render(self.surface)

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
                self.move_left()
            elif event.key == pygame.K_RIGHT:
                self.move_right()
            elif event.key == pygame.K_DOWN:
                self.move_down()
            elif event.key == pygame.K_UP:
                self.flip()
            elif event.key == pygame.K_ESCAPE:
                return False

        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value > 0: self.move_right()
                elif event.value < 0: self.move_left()
            elif event.axis == 1:
                if event.value > 0: self.move_down()
                elif event.value < 0: self.flip()

        return True


    def move_right(self):
        print 'right'


    def move_left(self):
        print 'left'


    def move_down(self):
        print 'down'


    def flip(self):
        print 'flip'


def main():
    engine = Engine()
    engine.create((800, 600))
    while engine.update():
        pass
    engine.destroy()

if __name__ == '__main__':
    main()
