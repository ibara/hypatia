import os
import threading
import pygame
import pygame.locals

from hypatia.editor.scenes.home import HomeScene
from hypatia.editor import constants
from . import Scene


class ProjectScanScene(Scene):
    def __init__(self, editor):
        super(ProjectScanScene, self).__init__(editor)

    def startup(self):
        super(ProjectScanScene, self).startup()
        self.thread = threading.Thread(target=self.threadtarget)
        self.thread.start()

    def threadtarget(self):
        path = self.editor.config.get("editor", "projectpath")
        for root, __, files in os.walk(path, followlinks=True):
            if 'game.py' in files:
                self.editor.projects.append({
                    "name": os.path.split(root)[-1],
                    "path": root,
                })

    def update(self):
        super(ProjectScanScene, self).update()

        if not self.thread.is_alive():
            self.editor.jump_scene(HomeScene)

        self.surface.fill((255, 255, 255))

        # draw the box
        boxsize = (self.editor.screen_size[0], 150)
        box = pygame.Surface(boxsize)
        box.fill(constants.COLOR_DEFAULT)

        t = self.editor.assets.font_render('title', "Scanning for projects...",
                                           constants.COLOR_INVERTED)
        tpos = ((boxsize[0] / 2) - (t.get_rect().width / 2),
                (boxsize[1] / 2) - (t.get_rect().height / 2))
        box.blit(t, tpos)

        boxpos = (0, (self.editor.screen_size[1] / 2) - (boxsize[1] / 2))
        self.surface.blit(box, boxpos)
