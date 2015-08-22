import pkgutil
import pygame
import io

# logotype
__logotype_data = pkgutil.get_data(__name__, "assets/logotype.bin")
logotype = pygame.image.fromstring(__logotype_data, (724, 124), "RGBA").convert_alpha()
logotype_small = pygame.transform.smoothscale(logotype, (181, 31)).convert_alpha()

# fonts
__chivo_data = io.BytesIO(pkgutil.get_data(__name__, "assets/chivo.ttf"))
__chivo_bold_data = io.BytesIO(pkgutil.get_data(__name__, "assets/chivo_bold.ttf"))
primary_font = pygame.font.Font(__chivo_data, 12)
title_font = pygame.font.Font(__chivo_bold_data, 14)

