import pygame
import pygame.locals

from hypatia.editor import constants
from . import Scene


class ProjectScene(Scene):
    def __init__(self, editor, projname):
        super(ProjectScene, self).__init__(editor)
        self.project_name = projname
        self.click_targets = []

    def handle_event(self, event):
        super(ProjectScene, self).handle_event(event)

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
        super(ProjectScene, self).startup()

        # clear click targets as we reinitialize them in here
        self.click_targets = []

        self.ret = self.editor.assets.font_render('fa', b'\xf0\x60',
                                                  constants.COLOR_DEFAULT)
        self.retpos = (8, 8)

        self.click_targets.append({
            "rect": self.ret.get_rect().move(*self.retpos),
            "callback": lambda e: self.editor.pop_scene(),
        })

    def update(self):
        super(ProjectScene, self).update()
        self.surface.fill((255, 255, 255))

        # blit return button
        self.surface.blit(self.ret, self.retpos)

        # blit project name text
        t = self.editor.assets.font_render('title', self.project_name,
                                           constants.COLOR_DEFAULT)
        tpos = (self.ret.get_rect().width + self.retpos[0] + 8, 8)
        self.surface.blit(t, tpos)
