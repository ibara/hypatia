import pygame
from pygame.locals import *

from . import scenes
from . import assets


class Editor(object):
    def __init__(self, scene=scenes.HomeScene):
        pygame.init()

        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size, DOUBLEBUF)
        pygame.display.set_caption("Hypatia")

        self.running = True
        self.assets = assets.Assets()
        self.scene = None
        self.switch_scene(scene)

        # TODO: create a scene that actually scans projects, instead of this
        # debugging measure

        self.projects = [
            {
                'name': 'debug',
                'path': '/home/hypatia-develop/demo'
            }
        ]

    """ Update screen with contents of current scene.
    """
    def update(self):
        if not self.scene.started:
            self.scene.startup()

        self.scene.update()
        self.screen.blit(self.scene.surface, (0, 0))
        pygame.display.flip()

    """ Handle pygame events. Passes events through to scene's handle_event()
        function.
    """
    def handle_events(self):
        for event in pygame.event.get():
            if self.scene:
                if self.scene.handle_event(event):
                    return

            if event.type == QUIT:
                self.running = False

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
        while self.running:
            self.handle_events()
            self.update()

        pygame.quit()
