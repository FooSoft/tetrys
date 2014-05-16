#!/usr/bin/env python

import pygame


class Engine:
    def create(self, resolution):
        pygame.init()
        pygame.display.set_mode(resolution, pygame.DOUBLEBUF)

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None


    def update(self):
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
            print 'keydown'
        elif event.type == pygame.JOYAXISMOTION:
            print event.axis, event.value
            if event.axis == 0:
                if event.value > 0: self.move_right()
                else: self.move_left()
            elif event.axis == 1:
                if event.value > 0: self.move_down()
                else: self.flip()

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
