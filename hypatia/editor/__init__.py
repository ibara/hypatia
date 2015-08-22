import logging
import pygame
import pygame.locals

class Editor(object):
    def __init__(self, scene=None):
        pygame.init()

        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.locals.DOUBLEBUF)
        pygame.display.set_caption("Hypatia")

        from . import scenes
        if scene == None:
            scene = scenes.HomeScene

        self.scene = None
        self.switch_scene(scene)

    """ Update screen with contents of current scene.
    """
    def update(self):
        self.scene.update()
        self.screen.blit(self.scene.surface, (0, 0))
        pygame.display.flip()

    """ Switch scenes
    """
    def switch_scene(self, scenecls, *args):
        if self.scene:
            self.scene.shutdown()

        s = scenecls(self, *args)
        self.scene = s

    """ Editor main loop.
    """
    def main_loop(self):
        while True:
            self.scene.handle_input()
            self.update()

        pygame.quit()

