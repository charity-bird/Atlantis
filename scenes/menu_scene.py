import pygame
from scenes.scene import Scene

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.menu_cursor_pos = 0
        print(self.game.screen_width)
        print(self.game.screen_height)
        self.title_surface = self.game.font_title.render("Atlantis", True, "white")
        self.menu_option_start = self.game.font_heading_three.render("Start", True, "white")
        self.menu_option_options = self.game.font_heading_three.render("Options", True, "white")
        self.menu_option_quit = self.game.font_heading_three.render("Quit", True, "white")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.game.menu_selection_sound.play()
                self.menu_cursor_pos += 1
                if self.menu_cursor_pos > 2:
                    self.menu_cursor_pos = 0
            elif event.key == pygame.K_UP:
                self.game.menu_selection_sound.play()
                self.menu_cursor_pos -= 1
                if self.menu_cursor_pos < 0:
                    self.menu_cursor_pos = 2
            elif event.key in [pygame.K_a, pygame.K_RETURN]:
                self.game.menu_selection_sound_2.play()
                if self.menu_cursor_pos == 0:
                    print("Setting scene to GameScene")
                    self.game.set_scene("game")
                elif self.menu_cursor_pos == 1:
                    print("Setting scene to OptionsScene")
                    self.game.set_scene("options")
                elif self.menu_cursor_pos == 2:
                    self.game.running = False  # Quit
            elif event.key == pygame.K_ESCAPE:
                self.game.running = False  # Quit

    def render(self, screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        screen.blit(self.title_surface, (self.game.screen_width / 2 - 108, self.game.screen_height / 3))
        screen.blit(self.menu_option_start, (self.game.screen_width / 2 - 32, self.game.screen_height / 3 + 120))
        screen.blit(self.menu_option_options, (self.game.screen_width / 2 - 52, self.game.screen_height / 3 + 155))
        screen.blit(self.menu_option_quit, (self.game.screen_width / 2 - 30, self.game.screen_height / 3 + 190))

        if (self.menu_cursor_pos == 0):
            pygame.draw.circle(screen, "white", (self.game.screen_width / 2 - 42, self.game.screen_height / 3 + 155), 5)
        elif (self.menu_cursor_pos == 1):
            pygame.draw.circle(screen, "white", (self.game.screen_width / 2 - 62, self.game.screen_height / 3 + 190), 5)
        elif (self.menu_cursor_pos == 2):
            pygame.draw.circle(screen, "white", (self.game.screen_width / 2 - 42, self.game.screen_height / 3 + 225), 5)
