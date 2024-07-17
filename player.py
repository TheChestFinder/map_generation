import pygame
from typing import List, Tuple
from map_objects import Tile
from math import dist
from itertools import pairwise
from random import randint, shuffle, choice
from inventory import PlayerInventory

class Player:
    def __init__(self) -> None:
        self.pos = pygame.Vector2(10, 9)
        self.body_sprites = pygame.image.load("./assets\png/walkcycle\BODY_male.png")
        self.direction = 2
        self.stage = 0
        self.walking_target = self.pos
        self.route: List[Tuple[int,int]] = []
        self.animation_counter = 0
        self.animation_frame = 10
        self.inventory = PlayerInventory()
        
    def set_target(self, target: pygame.Vector2, game_map: List[List[Tile]]) -> None:
        if game_map[round(target.y)][round(target.x)].biome not in (0, 1, 5):
            self.walking_target = target
            self.calculate_route(game_map)
    
    def calculate_route(self, map: List[List[Tile]]) -> None:
        open_set, closed_set = set(), set()
        start = tuple(self.pos)
        open_set.add(start)
        g_score, h_score = dict(), dict()
        g_score[start] = 0
        #h_score[start] = dist(start, self.walking_target)
        h_score[start] = abs(start[0] - self.walking_target[0])+abs(start[1] - self.walking_target[1])
        came_from = {}
        
        while open_set:
            #pos = min(open_set, key=lambda item: g_score[item] + h_score[item])
            min_score = min(g_score[item] + h_score[item] for item in open_set)
            min_neighbors = [item for item in open_set if g_score[item] + h_score[item] == min_score]
            pos = choice(min_neighbors)
            
            open_set.remove(pos)
            closed_set.add(pos)
            if pos == tuple(self.walking_target):
                break
            neighbors = [
                (pos[0] + 1, pos[1]),
                (pos[0], pos[1] + 1),
                (pos[0] - 1, pos[1]),
                (pos[0], pos[1] - 1)             
            ]
            shuffle(neighbors)
            
            for m in neighbors:
                if m in closed_set:
                    continue
                
                tile_row, tile_col = round(m[1]), round(m[0])
                if tile_row < 0 or tile_col < 0:
                    continue
                if tile_row >= len(map):
                    continue
                if tile_col >= len(map[tile_row]):
                    continue
                if map[tile_row][tile_col].biome in (0, 1, 5):
                    continue
                open_set.add(m)
                
                if m[0] != pos[0] and m[1] != pos[1]:
                    cost = g_score[pos] + dist(m, pos) * 0.8 
                else: 
                    cost = g_score[pos] + dist(m, pos)

                if m not in g_score or cost < g_score[m]:
                    g_score[m] = cost
                    h_score[m] = dist(m, self.walking_target)
                    came_from[m] = pos        
                
    
        rev_route = [tuple(self.walking_target)]
        while (last_pos := rev_route[-1]) != start:
            if last_pos not in came_from:
                return
            rev_route.append(came_from[rev_route[-1]])
            
        self.route = list(reversed(rev_route))
    
    def update_pos(self):
        if len(self.route) == 0:
            self.direction = 2
            return
        next_pos = self.route[0]
        if self.pos == next_pos:
            self.route.pop(0)
            return 
        
        #self.pos = next_pos
        #return
        
        target = pygame.Vector2(next_pos) - self.pos
        step = pygame.Vector2(0.2, 0)
        angle = step.angle_to(target)
        self.pos = self.pos+step.rotate(angle)
        self.pos = pygame.Vector2(round(self.pos.x, 1), round(self.pos.y, 1))
        self.direction = 3 - (angle % 360)//90
    
    def draw_line(self, surface:pygame.Surface, map_offset: pygame.Vector2):
        for p1, p2 in pairwise(self.route):
            p1_pos = (pygame.Vector2(p1) - map_offset) * 32 + pygame.Vector2(16, 16)
            p2_pos = (pygame.Vector2(p2) - map_offset) * 32 + pygame.Vector2(16, 16)
            pygame.draw.line(surface,(255, 0, 0), p1_pos, p2_pos, 2)
    
    
    
    def draw(self, surface:pygame.Surface, map_offset: pygame.Vector2) -> None:
        self.animation_counter +=1        
        if self.animation_counter == self.animation_frame:
            self.animation_counter = 0
            self.stage %= 7
            self.stage +=1
            
        
        crop_x = self.stage * 64
        crop_y = self.direction * 64
        crop_rect = pygame.Rect((crop_x, crop_y), (64, 64))
        img = self.body_sprites.subsurface(crop_rect)
        img = pygame.transform.scale(img, (32, 32))
        
        player_pos = (self.pos - map_offset) * 32
        surface.blit(img, player_pos)
        
        for line in self.inventory.clothes:
            for item in line:
                if item is None:
                    continue
                img = item.img.subsurface(crop_rect)
                img = pygame.transform.scale(img, (32, 32))
                surface.blit(img, player_pos)
        self.draw_line(surface, map_offset)
        