import pygame

class Button:
    def __init__(self, surface, position, on_hover = None, on_exit = None, on_click = None):
        self.surface = surface
        self.rect = surface.get_rect(topleft=position)

        self._hovered = False

        self.on_hover = on_hover
        self.on_exit = on_exit
        self.on_click = on_click

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        currently_hovered = self.rect.collidepoint(mouse_pos)

        if currently_hovered and not self._hovered:
            self._hovered = True
            if self.on_hover:
                self.on_hover()
        elif not currently_hovered and self._hovered:
            self._hovered = False
            if self.on_exit:
                self.on_exit()

        clicked = pygame.mouse.get_just_pressed()[0] and self._hovered
        if self.on_click and clicked:
            self.on_click()

    def load_sounds():
        Button.tick_sound = pygame.mixer.Sound("tick.wav")
        Button.ding_sound = pygame.mixer.Sound("ding.wav")

    def draw(self, display_surf):
        display_surf.blit(self.surface, (self.rect.x, self.rect.y))