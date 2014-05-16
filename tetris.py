#!/usr/bin/env python

import pygame


class Board:
    def __init__(self, grid_position, grid_dims, grid_border_width, block_dims):
        self.grid_dims = grid_dims
        self.grid_border_width = grid_border_width
        self.block_dims = block_dims

        grid_screen_dims = grid_dims[0]*block_dims[0], grid_dims[1]*block_dims[1]
        self.grid_rect = pygame.Rect(grid_position, grid_screen_dims)
        self.grid_color = pygame.Color(0xff, 0xff, 0xff, 0xff)
        self.block_colors = [
            pygame.Color(0xff, 0xff, 0xff, 0xff), # None
            pygame.Color(0x00, 0xff, 0xff, 0xff), # Cyan
            pygame.Color(0x00, 0x00, 0xff, 0xff), # Blue
            pygame.Color(0xff, 0x80, 0x00, 0xff), # Orange
            pygame.Color(0xff, 0xff, 0x00, 0xff), # Yellow
            pygame.Color(0x00, 0xff, 0x00, 0xff), # Green
            pygame.Color(0x80, 0x00, 0x80, 0xff), # Purple
            pygame.Color(0xff, 0x00, 0x00, 0xff)  # Red
        ]

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


    def advance(self):
        pass
    

    def block_screen_rect(self, position):
        top_left = self.grid_rect.x+self.block_dims[0]*position[0], self.grid_rect.y+self.block_dims[1]*position[1]
        return pygame.Rect(top_left, self.block_dims)


class Engine:
    def __init__(self):
        self.board = Board((10, 10), (10, 20), 1, (20, 20))
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
