import pygame
import pygame.locals

from . import constants


class Scene(object):
    """ A generic editor scene.

    Args:
      editor (hypatia.editor.Editor): The editor instance this scene belongs
        to.
    """
    def __init__(self, editor):
        self.editor = editor
        self.surface = pygame.Surface(editor.screen_size)
        self.started = False
        self.mousepos = (-1, -1)

    """ Update the scene. Called before blitting to the parent surface.
    """
    def update(self):
        pass

    """ Handle a single event for the scene.

        This function must return True if the event is handled within the
        scene, or return False if it wasn't.
    """
    def handle_event(self, event):
        if event.type == pygame.locals.MOUSEMOTION:
            self.mousepos = event.pos
            return True

        return False

    """ Scene setup. Called after Pygame is initialized.
    """
    def startup(self):
        self.started = True

    """ Perform scene shutdown.
    """
    def shutdown(self):
        pass


class HomeScene(Scene):
    def __init__(self, editor):
        super(HomeScene, self).__init__(editor)

    def update(self):
        super(HomeScene, self).update()

        self.surface.fill((255, 255, 255))
        self.surface.blit(self.editor.assets.logotype_small, (8, 8))

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

        last_pos = self.editor.projects[-1]["_rect"]
        np_pos = last_pos.move(0, self.editor.assets.font_size + 5)

        # Render the new projects text once, get it's rect so we can determine
        # hover state, and then re-render it with appropriate color
        t = self.editor.assets.font_render(None, "+ New project", (0, 0, 0))
        rect = t.get_rect().move(*(np_pos.x, np_pos.y))
        color = constants.COLOR_DEFAULT
        if rect.collidepoint(self.mousepos):
            color = constants.COLOR_HOVERED

        t = self.editor.assets.font_render(None, "+ New project", color)
        self.surface.blit(t, (np_pos.x, np_pos.y))
