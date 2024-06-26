import pygame
from typing import List, Sequence, Optional


class InventoryItem:
    def __init__(self, filename: str) -> None:
        self.img = pygame.image.load(filename)
        self.icon = self.img.subsurface((0, 0, 64, 64))

    def display_icon(self, surface:pygame.Surface, coords: Sequence[float]) -> None:
        surface.blit(surface, coords)

class PlayerInventory:
    def __init__(self) -> None:
        self.common_slots: List[List[InventoryItem | None]] = [[None] * 6 for _ in range(6)]
        self.tools: List[InventoryItem | None] = [None] * 6
        self.clothes: List[InventoryItem | None] = [None] * 6
        self.shown = 0
        
        self.moving_item: Optional[InventoryItem] = None
    
    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        
        if event.type == pygame.MOUSEBUTTONUP:
            pass
        
        if event.type == pygame.MOUSEMOTION:
            pass
    
    def display(self, surface:pygame.Surface) -> None:
        if not self.shown:
            return
        for i in range(len(self.common_slots)):
            for j in range(len(self.common_slots[i])):
                item = self.common_slots[i][j]
                item_surface = pygame.Surface((64, 64))
                if item is not None:
                    item.display_icon(item_surface, (0, 0))
                surface.blit(item_surface, (j * 64, i * 64))