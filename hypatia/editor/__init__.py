import os
import pygame
from pygame.locals import *

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from hypatia.editor.scenes.home import HomeScene
from hypatia.editor.scenes.setpath import SetPathScene
from hypatia.editor.scenes.projscan import ProjectScanScene
from hypatia.editor.scenes.about import AboutScene
from . import assets


class Editor(object):
    def __init__(self, configpath=None):
        pygame.init()

        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size, DOUBLEBUF)
        pygame.display.set_caption("Hypatia")

        self.running = True
        self.assets = assets.Assets()
        self.scenelist = []

        self.delay_load = False
        self.configpath = self.find_config(path=configpath)
        self.config = configparser.ConfigParser()
        self.projects = []

        if not self.configpath:
            self.jump_scene(SetPathScene)
            self.delay_load = True

        if not self.delay_load:
            self.load_config()
            self.jump_scene(ProjectScanScene)

    """ Try to determine config path. If a path is given and it is not None,
        it will be used, otherwise we will look in the "Hypatia Projects"
        directory in the user's home directory.
    """
    def find_config(self, path=None):
        if path and os.path.isfile(path):
            return path

        home = os.path.expanduser("~")
        if os.path.isdir(os.path.join(home, "Hypatia Projects")):
            return os.path.join(home, "Hypatia Projects", "config.ini")

    """ Load the config file from the editor config path.
    """
    def load_config(self):
        if not self.configpath:
            self.configpath = self.find_config()

        self.config.read(self.configpath) 
        if self.config.get("editor", "projectpath") == ".":
            self.config.set("editor", "projectpath",
                            os.path.dirname(self.configpath))

    """ Save the editor config file.
    """
    def save_config(self):
        fh = open(self.config_path, 'w+')
        self.config.write(fh)
        fh.close()

    """ Update screen with contents of current scene.
    """
    def update(self):
        if not self.scenelist[0].started:
            self.scenelist[0].startup()

        self.scenelist[0].update()
        self.screen.blit(self.scenelist[0].surface, (0, 0))
        pygame.display.flip()

    """ Handle pygame events. Passes events through to scene's handle_event()
        function.
    """
    def handle_events(self):
        for event in pygame.event.get():
            if len(self.scenelist) >= 1:
                if self.scenelist[0].handle_event(event):
                    return

            if event.type == QUIT:
                self.running = False

    """ Switch scenes
    """
    def jump_scene(self, scenecls, *args):
        if len(self.scenelist) >= 1:
            self.scenelist[0].shutdown()

        s = scenecls(self, *args)
        self.scenelist = [s]

    def push_scene(self, scenecls, *args):
        if len(self.scenelist) >= 1:
            self.scenelist[0].shutdown()

        self.scenelist.insert(0, scenecls(self, *args))

    def pop_scene(self):
        self.scenelist[0].shutdown()
        del self.scenelist[0]

    """ Editor main loop.
    """
    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update()

        pygame.quit()
