from map_objects import Map
import pygame

map = Map()
map_generator = map.generate_map()

def percentage_calc(done, total):
    percentage = (done/total)*100
    return round(percentage, 2)


font = pygame.font.SysFont("Arial", 20, True)
text = font.render("Map Generating...", True, (0, 0, 0))
textRect = text.get_rect()
textRect.bottomleft = (95, 549)
#completion_text = font.render("")

    