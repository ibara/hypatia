import logging
import pygame
import pygame.locals

from . import scenes
from . import assets

class Editor(object):
    def __init__(self, scene=scenes.HomeScene):
        print("pygame.init()")
        pygame.init()

        print("pygame screen")
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.locals.DOUBLEBUF)
        pygame.display.set_caption("Hypatia")

        print("assets")
        self.assets = assets.Assets()

        print("scene")
        self.scene = None
        self.switch_scene(scene)

    """ Update screen with contents of current scene.
    """
    def update(self):
        print("update")
        if not self.scene.started:
            self.scene.startup()

        self.scene.update()
        self.screen.blit(self.scene.surface, (0, 0))
        pygame.display.flip()

    """ Switch scenes
    """
    def switch_scene(self, scenecls, *args):
        if self.scene:
            self.scene.shutdown()

        s = scenecls(self, *args)
        print(repr(s))
        self.scene = s

    """ Editor main loop.
    """
    def main_loop(self):
        print("main_loop")
        while True:
            self.scene.handle_input()
            self.update()

        pygame.display.quit()


