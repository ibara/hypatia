import pygame
import pygame.locals

from hypatia.editor.scenes.about import AboutScene
from hypatia.editor.scenes.project import ProjectScene
from hypatia.editor import constants
from . import Scene


class HomeScene(Scene):
    def __init__(self, editor):
        super(HomeScene, self).__init__(editor)
        self.click_targets = []
        self.projects = {}

    def handle_event(self, event):
        super(HomeScene, self).handle_event(event)

        if event.type == pygame.locals.MOUSEMOTION:
            self.mousepos = event.pos
            return True

        if event.type == pygame.locals.MOUSEBUTTONUP:
            for i, data in enumerate(self.click_targets):
                if data["rect"].collidepoint(event.pos):
                    data["callback"](event)
                    return True

        return False

    def startup(self):
        super(HomeScene, self).startup()

        self.click_targets = []
        self.projects = []

        about = self.editor.assets.font_render('fa', b'\xf0\x59',
                                               constants.COLOR_DEFAULT)
        aboutpos = (self.editor.screen_size[0] - about.get_rect().width - 8, 8)
        self.about = about
        self.aboutpos = aboutpos

        self.click_targets.append({
            "rect": self.about.get_rect().move(*self.aboutpos),
            "callback": lambda e: self.editor.push_scene(AboutScene),
        })

        for i, v in enumerate(self.editor.projects):
            pos = (32, 75 + ((self.editor.assets.font_size + 5) * i))
            t = self.editor.assets.font_render(None, v["name"], (0, 0, 0))
            rect = t.get_rect().move(*pos)
            cb = lambda e: self.editor.push_scene(ProjectScene, v["name"])

            self.click_targets.append({
                "rect": rect,
                "callback": cb,
            })

            self.projects.append({
                "name": v["name"],
                "rect": rect,
                "pos": pos,
            })

    def update(self):
        super(HomeScene, self).update()

        self.surface.fill((255, 255, 255))
        self.surface.blit(self.editor.assets.logotype_small, (8, 8))

        self.surface.blit(self.about, self.aboutpos)

        t = self.editor.assets.font_render('title', "Projects",
                                           constants.COLOR_DEFAULT)
        self.surface.blit(t, (16, 48))

        for i, v in enumerate(self.projects):
            color = constants.COLOR_DEFAULT
            if v["rect"].collidepoint(self.mousepos):
                color = constants.COLOR_HOVERED

            t = self.editor.assets.font_render(None, v["name"], color)
            self.surface.blit(t, v["pos"])

        if len(self.projects) >= 1:
            last_pos = self.projects[-1]["rect"]
            np_pos = last_pos.move(0, self.editor.assets.font_size + 5)
        else:
            np_pos = pygame.Rect(32, 75, 1, 1)

        # Render the new projects text once, get it's rect so we can determine
        # hover state, and then re-render it with appropriate color
        t = self.editor.assets.font_render(None, "+ New project", (0, 0, 0))
        rect = t.get_rect().move(*(np_pos.x, np_pos.y))
        color = constants.COLOR_DEFAULT
        if rect.collidepoint(self.mousepos):
            color = constants.COLOR_HOVERED

        t = self.editor.assets.font_render(None, "+ New project", color)
        self.surface.blit(t, (np_pos.x, np_pos.y))
