import pygame
import pygame.locals


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
        return False

    """ Scene setup. Called after Pygame is initialized.
    """
    def startup(self):
        self.started = True

    """ Perform scene shutdown.
    """
    def shutdown(self):
        pass
