import pkgutil
import pygame
import tempfile
import os


class Assets(object):
    items = [
        'logotype.png',
        'chivo.ttf',
        'chivo_bold.ttf',
        'fontawesome.ttf',
    ]

    def __init__(self):
        self.files = {}
        self.tmpdir = tempfile.mkdtemp()
        for i in self.items:
            d = pkgutil.get_data(__name__, os.path.join("assets", i))
            fh = open(os.path.join(self.tmpdir, i), 'wb')
            fh.write(d)
            fh.close()

        self.font_size = 18

        __logotype_path = os.path.join(self.tmpdir, 'logotype.png')
        self.logotype = pygame.image.load(__logotype_path).convert_alpha()
        self.logotype_small = pygame.transform.smoothscale(self.logotype,
                                                           (181, 31))
        self.logotype_small.convert_alpha()

        __primary_path = os.path.join(self.tmpdir, 'chivo.ttf')
        __title_path = os.path.join(self.tmpdir, 'chivo_bold.ttf')
        __fa_path = os.path.join(self.tmpdir, 'fontawesome.ttf')

        __fallback_fonts = "dejavusans,bitstreamverasans"
        __fallback = pygame.font.match_font(__fallback_fonts)

        self.primary_font = pygame.font.Font(__primary_path, self.font_size)
        self.primary_font_fb = pygame.font.Font(__fallback, self.font_size)

        self.title_font = pygame.font.Font(__title_path, self.font_size)
        self.title_font_fb = pygame.font.Font(__fallback, self.font_size)
        self.title_font_fb.set_bold(True)

        self.fontawesome = pygame.font.Font(__fa_path, self.font_size)

    def font_render(self, type, text, color):
        f = self.primary_font
        fb = self.primary_font_fb

        if type == 'title':
            f = self.title_font
            fb = self.title_font_fb

        if type == 'fa':
            f = self.fontawesome
            fb = None

        try:
            return f.render(text, True, color)
        except pygame.error:
            return fb.render(text, True, color)
