import pygame
from scenes.scene import Scene

class OptionsScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.options_title = self.game.font_heading_three.render("Options", True, (255, 255, 255))
        self.options_bg_color = self.game.font_heading_three.render("Background Colour", True, (255, 255, 255))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_scene("menu")

    def render(self, screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        screen.blit(self.options_title, (self.game.screen_height / 2, self.game.screen_width / 5))
        screen.blit(self.options_bg_color, (self.game.screen_height / 2, self.game.screen_width / 5 + 100))

