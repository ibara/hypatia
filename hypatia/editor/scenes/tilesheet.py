import pygame
import pygame.locals

from hypatia.tiles import Tilesheet
from hypatia.editor import constants
from . import Scene


class TilesheetScene(Scene):
    def __init__(self, editor, project, tilesheet):
        super(TilesheetScene, self).__init__(editor)
        self.click_targets = []
        self.renderables = []
        self.project_name = project
        self.tilesheet_name = tilesheet

    def handle_event(self, event):
        super(TilesheetScene, self).handle_event(event)

        if event.type == pygame.locals.MOUSEMOTION:
            self.mousepos = event.pos
            return True

        if event.type == pygame.locals.MOUSEBUTTONUP:
            for i, data in enumerate(self.click_targets):
                if data["rect"].collidepoint(event.pos):
                    data["callback"](event)
                    return True

        return False

    def decr_tile(self, e):
        self.update_pos = True
        if self.current_tile == 0:
            return

        self.current_tile -= 1

    def incr_tile(self, e):
        self.update_pos = True
        if self.current_tile == len(self.tilesheet.tiles) - 1:
            return

        self.current_tile += 1

    def reset_scale(self, e):
        self.tile_scale = 1

    def incr_scale(self, e):
        self.tile_scale += 1

    def decr_scale(self, e):
        if self.tile_scale == 1:
            return

        self.tile_scale -= 1

    def startup(self):
        super(TilesheetScene, self).startup()
        self.click_targets = []
        self.renderables = []
        self.current_tile = 0
        self.tile_scale = 1
        self.update_pos = True

        found = None
        for i, v in enumerate(self.editor.projects):
            if v["name"] == self.project_name:
                found = i
                break

        if found is None:
            self.editor.pop_scene()

        self.project = self.editor.projects[found]

        if not self.tilesheet_name in self.project["tilesheets"]:
            self.editor.pop_scene()

        self.tilesheet = Tilesheet.from_resources(self.tilesheet_name, 
                                                  prefix=self.project["path"])

        ret = self.editor.assets.font_render('fa', b'\xf0\x60',
                                             constants.COLOR_INVERTED)
        retpos = (8, 8)
        self.click_targets.append({
            "rect": ret.get_rect().move(*retpos),
            "callback": lambda e: self.editor.pop_scene(),
        })
        self.renderables.append((ret, retpos)) 

        nametext = self.editor.assets.font_render('title',
                                                  self.tilesheet_name,
                                                  constants.COLOR_INVERTED)
        namepos = (ret.get_rect().width + retpos[0] + 8, 8)
        self.renderables.append((nametext, namepos))

        btn_pad = (5, 2)
        btn_left = [
            ("-", self.decr_scale),
            ("0", self.reset_scale),
            ("+", self.incr_scale),
            ("<", self.decr_tile),
            (">", self.incr_tile),
        ]
        left = 8

        for i, v in enumerate(btn_left):
            t = self.editor.assets.font_render(0, v[0],
                                               constants.COLOR_DEFAULT)
            s = pygame.Surface((t.get_rect().width + (btn_pad[0] * 2),
                                t.get_rect().height + (btn_pad[1] * 2)))
            s.fill(constants.COLOR_INVERTED)
            s.blit(t, btn_pad)

            pos = (left, self.editor.screen_size[1] - s.get_rect().height - 8)
            left += s.get_rect().width + btn_pad[0]

            self.renderables.append((s, pos))
            self.click_targets.append({
                "rect": s.get_rect().move(*pos),
                "callback": v[1],
            })

        self.button_left = left

    def update(self):
        super(TilesheetScene, self).update()
        self.surface.fill(constants.COLOR_DEFAULT)

        # render current selected tile
        tile = self.tilesheet.tiles[self.current_tile]
        size = (self.tilesheet.tile_size[0] * self.tile_scale,
                self.tilesheet.tile_size[1] * self.tile_scale)

        scaled = pygame.transform.scale(tile.subsurface, size)
        tpos = ((self.editor.screen_size[0] / 2) - (size[0] / 2),
                (self.editor.screen_size[1] / 2) - (size[1] / 2))

        self.surface.blit(scaled, tpos)

        tilename = self.editor.assets.font_render(0,
                                                  "tile %s" % self.current_tile,
                                                  constants.COLOR_INVERTED)
        tilepos = (self.button_left,
                   self.editor.screen_size[1] - tilename.get_rect().height - 8)

        self.surface.blit(tilename, tilepos)

        for i in self.renderables:
            self.surface.blit(*i)

