import pygame
from pnoise import Noise
from random import randint
from typing import Sequence, List
from map_objects import Map
from player import Player
import constants
from progress_bar import map, map_generator, percentage_calc, text, textRect, font
from inventory import InventoryItem, PlayerInventory

pygame.init()
window = pygame.display.set_mode((constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
clock = pygame.time.Clock()
player = Player()

game_surface = pygame.Surface(map.map_img.get_size())

delay = 0
minimap = None

robe_hood = InventoryItem("assets\png\walkcycle\HEAD_robe_hood.png")
inventory = PlayerInventory()
inventory.common_slots[2][2] = robe_hood
inventory.common_slots[2][4] = robe_hood

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if inventory.shown:
            inventory.handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and map.is_loaded and not inventory.shown:
            if event.button == pygame.BUTTON_LEFT:
                map_col = round((-map.offset_px.x + event.pos[0])//32 + map.offset_tiles.x)
                map_row = round((-map.offset_px.y + event.pos[1])//32 + map.offset_tiles.y)
                player.set_target(pygame.Vector2(map_col, map_row), map.map)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                inventory.shown = not inventory.shown

    pressed = pygame.key.get_pressed()
    if not inventory.shown:
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
        inventory.display(window) 
        delay += 1
            
    pygame.display.update()
    clock.tick(60)