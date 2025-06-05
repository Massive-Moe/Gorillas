import pygame

from button import Button

class Title():
    def __init__(self, screen, channel, font):
        self.screen = screen
        self.channel = channel

        self.quit = False
        self.play = False
        self.mute = False

        Title.logo = pygame.image.load("logo.png").convert_alpha()
        Title.volume_icon = pygame.image.load("volume.png").convert_alpha()
        Title.volume_icon = pygame.transform.scale_by(Title.volume_icon, 0.25)

        Title.play_text = font.render("Play", True, "black")
        Title.quit_text = font.render("Quit", True, "black")
        Title.credit = font.render("Created by Mostafa Elmansory", True, "purple")

        midpoint = self.screen.get_width()/2
        self.play_button = Button(Title.play_text, 
                                  (midpoint - Title.play_text.get_width()/2, 150),
                                  self.on_hover,
                                  self.on_exit,
                                  self.set_play
                                  )
        self.quit_button = Button(Title.quit_text, 
                                  (midpoint - Title.quit_text.get_width()/2, 250),
                                  self.on_hover,
                                  self.on_exit,
                                  self.set_quit
                                  )
        self.volume_button = Button(Title.volume_icon,
                                    (20, self.screen.get_height() - 80),
                                    self.on_hover,
                                    self.on_exit,
                                    self.toggle_volume
                                    )

        self.buttons = [self.play_button, self.quit_button, self.volume_button]
    
    def on_hover(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        self.channel.play(Button.tick_sound)

    def on_exit(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def set_play(self):
        self.play = True
        self.channel.play(Button.ding_sound)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def set_quit(self):
        self.quit = True

    def toggle_volume(self):
        self.mute = not self.mute
        self.channel.set_volume(0 if self.mute else 1)
        self.channel.play(Button.ding_sound)

    def update(self, dt):
        for button in self.buttons:
            button.update()

    def draw(self):
        self.screen.fill((245,245,245))
        self.screen.blit(Title.logo, (self.screen.get_width()/2 - Title.logo.get_width()/2, 20))
        self.screen.blit(Title.credit, 
                         (self.screen.get_width()/2 - Title.credit.get_width()/2,
                          self.screen.get_height() - 60
                          ))

        for button in self.buttons:
            button.draw(self.screen)
        
        if self.mute:
            pygame.draw.line(self.screen, "red", 
                             (20, 450),
                             (60, 410),
                             6
                             )
        
