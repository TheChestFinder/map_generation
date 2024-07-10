import pygame
from typing import List, Sequence, Optional
from constants import WINDOW_HEIGHT, WINDOW_WIDTH 

def empty_slot() -> pygame.Surface:
    item_surface = pygame.Surface((64, 64))
    item_surface.fill((200, 200, 200))
    pygame.draw.rect(item_surface, (190, 190, 190), (4, 4, 56, 56), 64, 6)
    pygame.draw.rect(item_surface, (170, 170, 170), (4, 4, 56, 56), 2, 6)
    
    return item_surface


class InventoryItem:
    def __init__(self, filename: str) -> None:
        self.img = pygame.image.load(filename)
        self.icon = self.img.subsurface((0, 0, 64, 64))

    def display_icon(self, surface:pygame.Surface, coords: Sequence[float]) -> None:
        surface.blit(self.img, coords)

class PlayerInventory:
    def __init__(self) -> None:
        self.common_slots: List[List[InventoryItem | None]] = [[None] * 6 for _ in range(6)]
        self.tools: List[List[InventoryItem | None]] = [[None] * 6]
        self.clothes: List[List[InventoryItem | None]]= [[None] * 6]
        self.shown = 0
        
        self.moving_item: Optional[tuple[int, int]] = None
        self.mouse_pos = None
        
        self.all_slots = [self.common_slots, self.tools, self.clothes]
        self.slot_rects = [pygame.Rect(0, 0, 0, 0)] * 3
        
        self.common_slots_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    
    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.common_slots_rect.collidepoint(event.pos):
                i= (event.pos[1] - self.common_slots_rect.top) //64
                j = (event.pos[0] - self.common_slots_rect.left) //64
                if self.common_slots[i][j] is not None:    
                    self.moving_item = i, j
        
        if event.type == pygame.MOUSEBUTTONUP:
            if self.moving_item is not None and self.mouse_pos is not None:
                mi, mj = self.moving_item
                if self.common_slots_rect.collidepoint(event.pos):
                    i = (event.pos[1] - self.common_slots_rect.top) // 64
                    j = (event.pos[0] - self.common_slots_rect.left) // 64
                    self.common_slots[i][j], self.common_slots[mi][mj] = self.common_slots[mi][mj], self.common_slots[i][j]
                self.mouse_pos = None
                self.moving_item = None
        
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
    
    def render_slots(self, slots: List[List[InventoryItem | None]]) -> pygame.Surface:
        surface_width = len(slots[0]) * 64
        surface_height = len(slots) * 64
        result = pygame.Surface((surface_width, surface_height))
        for i in range(len(slots)):
            for j in range(len(slots[i])):
                item = slots[i][j]
                item_surface = empty_slot()
                if item is not None:
                    item.display_icon(item_surface, (0, 0))
                result.blit(item_surface, (j * 64, i * 64))
        return result
        
    
    def display(self, surface:pygame.Surface) -> None:
        if not self.shown:
            return
        
        bg_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA, 32)
        bg_surface.convert_alpha()
        bg_surface.fill((0, 0, 0, 200))
        
        for slots_group in self.all_slots:
            slots_group_img = self.render_slots(slots_group)
            # TODO: Calc dest_rect for group
        
        # common_slots_img = self.render_slots(self.common_slots)
        # common_slots_dest = common_slots_img.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.52))
        # self.common_slots_rect = bg_surface.blit(common_slots_img, common_slots_dest)
        
        # tools_img = self.render_slots([self.tools])
        # tools_dest = tools_img.get_rect(left=common_slots_dest.left, top=common_slots_dest.bottom + 2)
        # _ = bg_surface.blit(tools_img, tools_dest)
        
        if self.moving_item is not None and self.mouse_pos is not None:
            icon_surface = pygame.Surface((64,64))
            mi, mj = self.moving_item
            moving_item = self.common_slots[mi][mj]
            moving_item.display_icon(icon_surface, (0, 0))
            icon_surface.set_colorkey((0, 0, 0))
            bg_surface.blit(icon_surface, pygame.Vector2(self.mouse_pos) - pygame.Vector2(32, 32))
        surface.blit(bg_surface,(0, 0))