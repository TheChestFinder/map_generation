import pygame
from pnoise import Noise
from random import randint, choice
from typing import Sequence, List
from map_objects import Map
from player import Player
import constants
from progress_bar import map, map_generator, percentage_calc, text, textRect, font
from inventory import InventoryItem, PlayerInventory, walk_cycle, InventorySlot

pygame.init()
window = pygame.display.set_mode((constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
clock = pygame.time.Clock()
player = Player()

game_surface = pygame.Surface(map.map_img.get_size())

delay = 0
minimap = None

for _ in range(2):
    for i in range(6):
        slot = InventorySlot()
        slot.item = choice(walk_cycle)
        slot.count = 1
        player.inventory.common_slots[i][_] = slot


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if player.inventory.shown:
            player.inventory.handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and map.is_loaded and not player.inventory.shown:
            if event.button == pygame.BUTTON_LEFT:
                map_col = round((-map.offset_px.x + event.pos[0])//32 + map.offset_tiles.x)
                map_row = round((-map.offset_px.y + event.pos[1])//32 + map.offset_tiles.y)
                player.set_target(pygame.Vector2(map_col, map_row), map.map)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.inventory.shown = not player.inventory.shown
            if event.key == pygame.K_SPACE:
                x, y = player.pos
                tile = map.map[int(y)][int(x)]
                #print(tile.resource)
                player.interact(tile)
                map.draw_map()

    pressed = pygame.key.get_pressed()
    if not player.inventory.shown:
        map.handle_pressed(pressed)
    map.handle_pressed(pressed)
    window.fill((200, 0, 0))
    
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(95, 550, 510, 70), 5)   
    window.blit(text, textRect)
    if not map.is_loaded:    
        try:
            done, total = next(map_generator)
            #print(done, "/", total, "-", percentage_calc(done, total), "%")
            
            bar_width = percentage_calc(done, total) * 5
            pygame.draw.rect(window, (255, 255, 0), pygame.Rect(100, 555, bar_width, 60))
            
            tiles_text = font.render(str(done) + "/" + str(total), True, (0, 0, 0))
            tiles_textRect = tiles_text.get_rect()
            tiles_textRect.midleft = (125, 585)
            window.blit(tiles_text, tiles_textRect)
            
            perc_text = font.render(str(percentage_calc(done, total)) + "%", True, (0, 0, 0))
            perc_textRect = perc_text.get_rect()
            perc_textRect.midright = (575, 585)
            window.blit(perc_text, perc_textRect)
        except StopIteration:
            map.is_loaded = True
            map.draw_map()
        
    else:
        game_surface.blit(map.map_img, (0, 0))
        if delay == 10:
            if player.stage < 7:
                player.stage += 1
            else:
                player.stage = 1
            delay = 0
        player.draw(game_surface, map.offset_tiles)
        player.update_pos()
        if minimap == None:
            minimap = map.get_minimap(map.map)
        window.blit(game_surface, map.offset_px)     
        window.blit(minimap, (0, 0))  
        player.inventory.display(window) 
        delay += 1
            
    pygame.display.update()
    clock.tick(60)