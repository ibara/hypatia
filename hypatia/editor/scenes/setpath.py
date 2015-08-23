import os
import pygame
import pygame.locals

from hypatia.editor.scenes.projscan import ProjectScanScene
from hypatia.editor import constants
from . import Scene


class SetPathScene(Scene):
    def __init__(self, editor):
        super(SetPathScene, self).__init__(editor)
        self.path = os.path.join(os.path.expanduser("~"), "Hypatia Projects")

    def handle_event(self, event):
        super(SetPathScene, self).handle_event(event)
        if event.type == pygame.locals.MOUSEBUTTONUP:
            if self.yes_rect.collidepoint(event.pos):
                self.makedir()
                self.editor.delay_load = False
                self.editor.load_config()
                self.editor.jump_scene(ProjectScanScene)

                return True

            if self.chg_rect.collidepoint(event.pos):
                # TODO: implement path changes

                return False

    def makedir(self):
        os.mkdir(self.path)
        fh = open(os.path.join(self.path, "config.ini"), "w+")
        fh.write(constants.CONFIG_DEFAULT)
        fh.close()

    def update(self):
        super(SetPathScene, self).update()
        self.surface.fill((255, 255, 255))

        boxsize = (self.editor.screen_size[0], 150)
        boxpos = (0, (self.editor.screen_size[1] / 2) - (boxsize[1] / 2))
        btnpad = (10, 5)

        # draw the box
        box = pygame.Surface(boxsize)
        box.fill(constants.COLOR_DEFAULT)

        t = self.editor.assets.font_render('title',
                                           "Choose your project directory",
                                           constants.COLOR_INVERTED)
        tpos = ((boxsize[0] / 2) - (t.get_rect().width / 2), 10)
        box.blit(t, tpos)

        msg = "We will create a Hypatia Projects directory in your home " + \
              "directory. Is this okay?"

        t = self.editor.assets.font_render(None, msg, constants.COLOR_INVERTED)
        tpos = ((boxsize[0] / 2) - (t.get_rect().width / 2), 40)
        box.blit(t, tpos)

        yestext = self.editor.assets.font_render(None, "Yes",
                                                 constants.COLOR_DEFAULT)
        yesbtn = pygame.Surface((yestext.get_rect().width + (btnpad[0] * 2),
                                 yestext.get_rect().height + (btnpad[1] * 2)))
        yesbtn.fill(constants.COLOR_INVERTED)
        yesbtn.blit(yestext, btnpad)

        chgtext = self.editor.assets.font_render(None, "Change path",
                                                 constants.COLOR_DEFAULT)
        chgbtn = pygame.Surface((chgtext.get_rect().width + (btnpad[0] * 2),
                                 chgtext.get_rect().height + (btnpad[1] * 2)))
        chgbtn.fill(constants.COLOR_INVERTED)
        chgbtn.blit(chgtext, btnpad)

        overallwidth = yesbtn.get_rect().width + 10 + chgbtn.get_rect().width
        overallheight = yesbtn.get_rect().height

        yespos = ((boxsize[0] / 2) - (overallwidth / 2),
                  boxsize[1] - overallheight - 10)

        chgpos = ((boxsize[0] / 2) - (overallwidth / 2) +
                  yesbtn.get_rect().width + 10, yespos[1])

        box.blit(yesbtn, yespos)
        box.blit(chgbtn, chgpos)

        self.yes_rect = yesbtn.get_rect().move(yespos).move(boxpos)
        self.chg_rect = chgbtn.get_rect().move(chgpos).move(boxpos)

        self.surface.blit(box, boxpos)
