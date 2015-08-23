import pkgutil
import pygame
import tempfile
import os

class Assets(object):
    items = [
        'logotype.png',
        'chivo.ttf',
        'chivo_bold.ttf',
    ]

    def __init__(self):
        self.files = {}
        self.tmpdir = tempfile.mkdtemp()
        for i in self.items:
            d = pkgutil.get_data(__name__, os.path.join("assets", i))
            fh = open(os.path.join(self.tmpdir, i), 'wb')
            fh.write(d)
            fh.close()
        
        self.logotype = pygame.image.load(os.path.join(self.tmpdir, 'logotype.png')).convert_alpha()
        self.logotype_small = pygame.transform.smoothscale(self.logotype, (181, 31)).convert_alpha()

        self.primary_font = pygame.font.Font(os.path.join(self.tmpdir, 'chivo.ttf'), 12)
        self.title_font = pygame.font.Font(os.path.join(self.tmpdir, 'chivo_bold.ttf'), 12)

