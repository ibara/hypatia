import pygame
import pygame.locals

from hypatia.editor import constants
from . import Scene


class ProjectScene(Scene):
    def __init__(self, editor, projname):
        super(ProjectScene, self).__init__(editor)
        self.project_name = projname
        self.click_targets = []

        self.in_dialog = False
        self.dialog_text = None

    def handle_event(self, event):
        super(ProjectScene, self).handle_event(event)

        if event.type == pygame.locals.MOUSEMOTION:
            self.mousepos = event.pos
            return True

        if event.type == pygame.locals.MOUSEBUTTONUP:
            if not self.in_dialog:
                for i, data in enumerate(self.click_targets):
                    if data["rect"].collidepoint(event.pos):
                        data["callback"](event)
                        return True

        return False

    def startup(self):
        super(ProjectScene, self).startup()

        # check that we have a valid project...
        found = None
        for i, v in enumerate(self.editor.projects):
            if v["name"] == self.project_name:
                found = i
                break

        # ...and jump back to where we came from if we don't
        if found is None:
            self.editor.pop_scene()

        self.project = self.editor.projects[found]

        # clear click targets as we reinitialize them in here
        self.click_targets = []

        self.ret = self.editor.assets.font_render('fa', b'\xf0\x60',
                                                  constants.COLOR_DEFAULT)
        self.retpos = (8, 8)

        self.click_targets.append({
            "rect": self.ret.get_rect().move(*self.retpos),
            "callback": lambda e: self.editor.pop_scene(),
        })

        self.nametext = self.editor.assets.font_render('title',
                                                       self.project_name,
                                                       constants.COLOR_DEFAULT)
        self.namepos = (self.ret.get_rect().width + self.retpos[0] + 8, 8)

        self.ovtext = self.editor.assets.font_render('title', 'overview',
                                                     constants.COLOR_INACTIVE)
        self.ovpos = (self.namepos[0] + self.nametext.get_rect().width + 8, 8)

    def update(self):
        super(ProjectScene, self).update()
        self.surface.fill((255, 255, 255))

        if self.in_dialog:
            boxsize = (self.editor.screen_size[0], 150)
            boxpos = (0, (self.editor.screen_size[1] / 2) - (boxsize[1] / 2))
            box = pygame.Surface(boxsize)
            box.fill(constants.COLOR_DEFAULT)

            t = self.editor.assets.font_render("title", self.dialog_text,
                                               constants.COLOR_INVERTED)
            tpos = ((boxsize[0] / 2) - (t.get_rect().width / 2),
                    (boxsize[1] / 2) - (t.get_rect().height / 2))
            box.blit(t, tpos)
            self.surface.blit(box, boxpos)

            return

        self.surface.blit(self.ret, self.retpos)
        self.surface.blit(self.nametext, self.namepos)
        self.surface.blit(self.ovtext, self.ovpos)
