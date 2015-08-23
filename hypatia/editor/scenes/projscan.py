import os
import zipfile
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
                tilesheets = []
                scenes = []
                walkabouts = []

                tilesheet_dir = os.path.join(root, "resources", "tilesheets")
                scene_dir = os.path.join(root, "resources", "scenes")
                walkabout_dir = os.path.join(root, "resources", "walkabouts")

                for f in os.listdir(tilesheet_dir):
                    if os.path.splitext(f)[1] == '.zip':
                        fn = os.path.join(tilesheet_dir, f)
                        with zipfile.ZipFile(fn) as zip:
                            if 'tilesheet.png' in zip.namelist():
                                tilesheets.append(os.path.splitext(f)[0])
                                continue

                    if os.path.isdir(os.path.join(tilesheet_dir, f)):
                        if os.path.isfile(os.path.join(tilesheet_dir, f,
                                                       "tilesheet.png")):
                            tilesheets.append(f)

                for f in os.listdir(scene_dir):
                    if os.path.splitext(f)[1] == '.zip':
                        fn = os.path.join(scene_dir, f)
                        with zipfile.ZipFile(fn) as zip:
                            if 'tilemap.txt' in zip.namelist():
                                scenes.append(os.path.splitext(f)[0])
                                continue

                    if os.path.isdir(os.path.join(scene_dir, f)):
                        fn = os.path.join(scene_dir, f, "tilemap.txt")
                        if os.path.isfile(fn):
                            scenes.append(f)

                for f in os.listdir(walkabout_dir):
                    searches = ['only.gif', 'walk_north.gif', 'walk_south.gif']
                    if os.path.splitext(f)[1] == '.zip':
                        fn = os.path.join(walkabout_dir, f)
                        with zipfile.ZipFile(fn) as zip:
                            for i in searches:
                                if i in zip.namelist():
                                    walkabouts.append(os.path.splitext(f)[0])
                                    continue

                    if os.path.isdir(os.path.join(walkabout_dir, f)):
                        found = False
                        for i in searches:
                            if not found:
                                if os.path.join(walkabout_dir, f, i):
                                    walkabouts.append(f)

                self.editor.projects.append({
                    "name": os.path.split(root)[-1],
                    "path": root,
                    "tilesheets": set(tilesheets),
                    "scenes": set(scenes),
                    "walkabouts": set(walkabouts),
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
