import pygame
import pkgutil

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
        
    """ Update the scene. Called before blitting to the parent surface.
    """
    def update(self):
        pass

    """ Handle input for the scene.
    """
    def handle_input(self):
        pass

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

    def startup(self):
        self.projects_text = self.editor.assets.title_font.render(u"Projects", 1, (51, 51, 51))

    def update(self):
        self.surface.fill((255, 255, 255))
        self.surface.blit(self.editor.assets.logotype_small, (8, 8))

        # blit projects text
        self.surface.blit(self.projects_text, (16, 64))
            
