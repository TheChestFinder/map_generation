import pygame
from inventory import InventoryItem, Materials
inventory_icnons = pygame.image.load("./assets/nails.png")

class Resource:
    def __init__(self) -> None:
        self.icon = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.icon.convert_alpha()
        self.count = 5

    def get_item(self) -> InventoryItem:
        pass

    def draw(self, surface: pygame.Surface, pos: tuple[int, int]):
        surface.blit(surface, pos)

class Animal(Resource):
    pass

class Wood(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.icon.blit(inventory_icnons, (0, 0), (32, 0, 32, 32))

    def get_item(self) -> InventoryItem:
        return InventoryItem("./assets/nails.png", Materials, (32, 0, 32, 32))

class Stone(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.icon.blit(inventory_icnons, (0, 0), (32 * 2, 32, 32, 32))
        
    def get_item(self) -> InventoryItem:
        return InventoryItem("./assets/nails.png", Materials, (64, 32, 32, 32))

class Metal(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.icon.blit(inventory_icnons, (0, 0), (64, 64, 32, 32))
        
    def get_item(self) -> InventoryItem:
        return InventoryItem("./assets/nails.png", Materials, (64, 64, 32, 32))

class Diamond(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.icon.blit(inventory_icnons, (0, 0), (64, 96, 32, 32))
        
    def get_item(self) -> InventoryItem:
        return InventoryItem("./assets/nails.png", Materials, (64, 96, 32, 32))
