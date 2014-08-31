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
        return Tetrad((self.position[0] - 1, self.position[1]), self.config, self.rotation)


    def moved_right(self):
        return Tetrad((self.position[0] + 1, self.position[1]), self.config, self.rotation)


    def moved_down(self):
        return Tetrad((self.position[0], self.position[1] + 1), self.config, self.rotation)


    def rotated(self):
        return Tetrad(self.position, self.config, (self.rotation + 1) % self.block_rotations)


    def centered(self, width):
        return Tetrad((width / 2 - 2, 0), self.config, self.rotation)


    @staticmethod
    def random(position=(0, 0)):
        config = random.randrange(len(Tetrad.block_configs))
        rotation = random.randrange(Tetrad.block_rotations)
        return Tetrad(position, config, rotation)


#
# Board
#

class Board:
    border_color = 0xeeeeec
    preview_color = 0xd3d7cf
    block_colors = [
        (0x555753, 0x2e3436), # Aluminium
        (0xedd400, 0xfce94f), # Butter
        (0xf57900, 0xfcaf3e), # Orange
        (0xc17d11, 0xe9b96e), # Chocolate
        (0x73d216, 0x8ae234), # Chameleon
        (0x3465a4, 0x729fcf), # Sky Blue
        (0x75507b, 0xad7fa8), # Plum
        (0xcc0000, 0xef2929)  # Scarlet Red
    ]


    def __init__(self, grid_position, grid_dims, grid_border_width, block_size):
        self.grid_dims = grid_dims
        self.grid_border_width = grid_border_width
        self.block_size = block_size

        grid_screen_dims = (
            grid_border_width * 2 + grid_dims[0] * block_size,
            grid_border_width * 2 + grid_dims[1] * block_size
        )

        self.grid_rect = pygame.Rect(grid_position, grid_screen_dims)
        self.blocks = [[0]*grid_dims[0] for i in range(grid_dims[1])]


    def render(self, surface):
        self.render_frame(surface)
        self.render_blocks(surface)


    def render_frame(self, surface):
        pygame.draw.rect(surface, self.border_color, self.grid_rect, self.grid_border_width)


    def render_blocks(self, surface):
        for y in xrange(self.grid_dims[1]):
            for x in xrange(self.grid_dims[0]):
                self.render_block(surface, self.blocks[y][x], (x, y))


    def render_tetrad(self, surface, tetrad, preview=False):
        color = tetrad.color()
        for point in tetrad.layout():
            self.render_block(surface, color, point, preview)


    def render_block(self, surface, color, position, preview=False):
        block_rect = self.block_screen_rect(position)
        if preview:
            color = 0

        color_outer, color_inner = self.block_colors[color]
        pygame.draw.rect(surface, color_inner, block_rect)
        pygame.draw.rect(surface, color_outer, block_rect, 1)

        if preview:
            position = block_rect.centerx, block_rect.centery
            pygame.draw.circle(surface, self.preview_color, position, 2)


    def block_screen_rect(self, position):
        top_left = (
            self.grid_border_width + self.grid_rect.x + self.block_size * position[0],
            self.grid_border_width + self.grid_rect.y + self.block_size * position[1]
        )
        return pygame.Rect(top_left, (self.block_size, self.block_size))


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
        settled_count = 0

        row_src = row_dst = self.grid_dims[1] - 1
        while row_dst >= 0:
            row_data = self.blocks[row_src] if row_src >= 0 else self.grid_dims[0] * [0]
            self.blocks[row_dst] = row_data
            row_src -= 1
            if 0 in row_data:
                row_dst -= 1
            else:
                settled_count += 1

        return settled_count


#
# Game
#

class Game:
    text_color = 0xeeeeecff
    text_bg_color = 0x000000ff
    line_multipliers = [100, 300, 500, 800]
    lines_per_level = 10
    base_speed = 800
    speed_multiplier = 2
    soft_drop_bonus = 1
    hard_drop_bonus = 2

    def __init__(self):
        font_path = pygame.font.get_default_font()
        self.font = pygame.font.Font(font_path, 16)
        self.reset()


    def new_game(self):
        self.reset()

        self.tetrad = Tetrad.random()
        self.tetrad = self.tetrad.centered(self.board.grid_dims[0])
        self.tetrad_next = Tetrad.random()
        self.tetrad_preview = None

        self.active = True


    def end_game(self):
        self.active = False


    def reset(self):
        border_width = 3
        block_size = 30
        padding = 10

        self.board = Board((padding, padding), (10, 20), border_width, block_size)
        self.board_prev = Board((self.board.grid_rect.right + padding, padding), (4, 4), border_width, block_size)
        self.scoreboard_position = self.board_prev.grid_rect.left, self.board_prev.grid_rect.bottom+padding
        self.scoreboard_dirty = True

        self.tetrad = None
        self.tetrad_next = None
        self.tetrad_preview = None

        self.ticker = 0
        self.score = 0
        self.lines_cleared = 0

        self.active = False


    def render(self, surface):
        self.board.render(surface)
        if self.tetrad_preview is not None:
            self.board.render_tetrad(surface, self.tetrad_preview, True)
        if self.tetrad is not None:
            self.board.render_tetrad(surface, self.tetrad)

        self.board_prev.render(surface)
        if self.tetrad_next is not None:
            self.board_prev.render_tetrad(surface, self.tetrad_next)

        self.render_scoreboard(surface)


    def render_scoreboard(self, surface):
        if not self.scoreboard_dirty:
            return

        text_lines = [
            'Score: {0}'.format(self.score),
            'Lines: {0}'.format(self.lines_cleared),
            'Level: {0}'.format(self.current_level() + 1)
        ]

        for index, text_line in enumerate(text_lines):
            text_surface = self.font.render(
                text_line,
                False,
                pygame.Color(self.text_color),
                pygame.Color(self.text_bg_color)
            )

            text_position = (
                self.scoreboard_position[0],
                self.scoreboard_position[1] + index * self.font.get_height()
            )

            surface.blit(text_surface, text_position)

        self.scoreboard_dirty = False


    def advance(self, elapsed):
        if not self.active:
            return

        self.tetrad_preview = None
        tetrad_preview = self.tetrad.moved_down()
        while self.board.can_place_tetrad(tetrad_preview):
            self.tetrad_preview = tetrad_preview
            tetrad_preview = self.tetrad_preview.moved_down()

        self.ticker += elapsed
        if self.ticker > self.current_speed():
            self.lower_tetrad()


    def try_placement(self, tetrad):
        if self.board.can_place_tetrad(tetrad):
            self.tetrad = tetrad
            return True

        return False


    def lower_tetrad(self):
        self.ticker = 0
        if self.try_placement(self.tetrad.moved_down()):
            return True

        self.board.place_tetrad(self.tetrad)

        lines_cleared = self.board.settle()
        if lines_cleared > 0:
            self.update_score((self.current_level() + 1) * self.line_multipliers[lines_cleared - 1])
            self.lines_cleared += lines_cleared

        self.tetrad = self.tetrad_next.centered(self.board.grid_dims[0])
        self.tetrad_next = Tetrad.random()
        self.tetrad_preview = None

        if not self.try_placement(self.tetrad):
            self.end_game()

        return False


    def move_left(self):
        if self.active:
            self.try_placement(self.tetrad.moved_left())


    def move_right(self):
        if self.active:
            self.try_placement(self.tetrad.moved_right())


    def move_down(self):
        if self.active:
            self.update_score(self.soft_drop_bonus)
            self.lower_tetrad()


    def rotate(self):
        if self.active:
            self.try_placement(self.tetrad.rotated())


    def drop(self):
        if self.active:
            while self.lower_tetrad():
                self.update_score(self.hard_drop_bonus)


    def current_level(self):
        return self.lines_cleared / self.lines_per_level


    def current_speed(self):
        return self.base_speed - self.current_level() * self.speed_multiplier


    def update_score(self, value):
        if value > 0:
            self.score += value
            self.scoreboard_dirty = True


#
# Engine
#

class Engine:
    def create(self, resolution):
        pygame.init()

        self.game = Game()
        self.surface = pygame.display.set_mode(resolution, pygame.DOUBLEBUF)
        pygame.display.set_caption('Tetrys')
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
            elif event.key == pygame.K_SPACE:
                self.game.drop()
            elif event.key == pygame.K_n:
                self.game.new_game()
            elif event.key == pygame.K_ESCAPE:
                return False

        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value > 0: self.game.move_right()
                elif event.value < 0: self.game.move_left()
            elif event.axis == 1:
                if event.value > 0: self.game.move_down()
                elif event.value < 0: self.game.rotate()

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 7:
                self.game.new_game()
            elif event.button == 3:
                self.game.drop()

        return True


#
# Entry
#

def main():
    engine = Engine()
    engine.create((462, 626))
    while engine.update():
        pass
    engine.destroy()

if __name__ == '__main__':
    main()
