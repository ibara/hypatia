import pygame
import pygame.locals

import hypatia
from hypatia.editor import constants
from . import Scene


class AboutScene(Scene):
    def __init__(self, editor):
        super(AboutScene, self).__init__(editor)
        self.click_targets = []

    def handle_event(self, event):
        super(AboutScene, self).handle_event(event)

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
        super(AboutScene, self).startup()

        # clear click targets as we reinitialize them in here
        self.click_targets = []

        self.ret = self.editor.assets.font_render('fa', b'\xf0\x0d',
                                                  constants.COLOR_DEFAULT)
        retpos = (self.editor.screen_size[0] - self.ret.get_rect().width - 8,
                  8)
        self.retpos = retpos

        self.click_targets.append({
            "rect": self.ret.get_rect().move(*self.retpos),
            "callback": lambda e: self.editor.pop_scene(),
        })

    def update(self):
        super(AboutScene, self).update()
        self.surface.fill((255, 255, 255))

        # blit return button
        self.surface.blit(self.ret, self.retpos)

        # blit logo
        logo_x = ((self.editor.screen_size[0] / 2) -
                  (self.editor.assets.logotype.get_rect().width / 2))
        logo_y = 40
        self.surface.blit(self.editor.assets.logotype, (logo_x, logo_y))

        msg = "Hypatia %s" % hypatia.__version__
        t = self.editor.assets.font_render(None, msg, constants.COLOR_DEFAULT)
        tpos = ((self.editor.screen_size[0] / 2) - (t.get_rect().width / 2),
                (logo_y + self.editor.assets.logotype.get_rect().height + 20))
        self.surface.blit(t, tpos)

        msg = "Brought to you by Lillian Lemmer and %d other contributors"
        msg = msg % (len(hypatia.__contributors__) - 1)
        t = self.editor.assets.font_render(None, msg, constants.COLOR_DEFAULT)
        tpos = ((self.editor.screen_size[0] / 2) - (t.get_rect().width / 2),
                (logo_y + self.editor.assets.logotype.get_rect().height + 40))
        self.surface.blit(t, tpos)
