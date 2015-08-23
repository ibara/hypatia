import pygame
import pygame.locals

from hypatia.editor.scenes.about import AboutScene
from hypatia.editor import constants
from . import Scene


class HomeScene(Scene):
    def __init__(self, editor):
        super(HomeScene, self).__init__(editor)
        self.click_targets = []

    def handle_event(self, event):
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
        # clear click targets as we reinitialize them in here
        self.click_targets = []

        about = self.editor.assets.font_render('fa', b'\xf0\x59',
                                               constants.COLOR_DEFAULT)
        aboutpos = (self.editor.screen_size[0] - about.get_rect().width - 8, 8)
        self.about = about
        self.aboutpos = aboutpos

        self.click_targets.append({
            "rect": self.about.get_rect().move(*self.aboutpos),
            "callback": lambda e: self.editor.push_scene(AboutScene),
        })


    def update(self):
        super(HomeScene, self).update()

        self.surface.fill((255, 255, 255))
        self.surface.blit(self.editor.assets.logotype_small, (8, 8))

        self.surface.blit(self.about, self.aboutpos)

        t = self.editor.assets.font_render('title', "Projects",
                                           constants.COLOR_DEFAULT)
        self.surface.blit(t, (16, 48))

        for i, __ in enumerate(self.editor.projects):
            name = self.editor.projects[i]['name']
            pos = (32, 80 + ((self.editor.assets.font_size + 5) * i))

            color = constants.COLOR_DEFAULT
            if "_rect" in self.editor.projects[i]:
                rect = self.editor.projects[i]["_rect"]
                if rect.collidepoint(self.mousepos):
                    color = constants.COLOR_HOVERED

            t = self.editor.assets.font_render(None, name, color)
            rect = t.get_rect().move(*pos)
            self.editor.projects[i]["_rect"] = rect

            self.surface.blit(t, pos)

        if len(self.editor.projects) > 1:
            last_pos = self.editor.projects[-1]["_rect"]
            np_pos = last_pos.move(0, self.editor.assets.font_size + 5)
        else:
            np_pos = pygame.Rect(32, 80, 1, 1)

        # Render the new projects text once, get it's rect so we can determine
        # hover state, and then re-render it with appropriate color
        t = self.editor.assets.font_render(None, "+ New project", (0, 0, 0))
        rect = t.get_rect().move(*(np_pos.x, np_pos.y))
        color = constants.COLOR_DEFAULT
        if rect.collidepoint(self.mousepos):
            color = constants.COLOR_HOVERED

        t = self.editor.assets.font_render(None, "+ New project", color)
        self.surface.blit(t, (np_pos.x, np_pos.y))

