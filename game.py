# Example file showing a circle moving on screen
import pygame
import json
from scenes.game_scene import GameScene
from scenes.menu_scene import MenuScene
from scenes.options_scene import OptionsScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts
        self.font_scheherazade_reg = pygame.font.Font('resources/fonts/Scheherazade-Regular.ttf', 30)
        self.font_scheherazade_bold = pygame.font.Font('resources/fonts/Scheherazade-Bold.ttf', 30)
        self.font_title = pygame.font.Font('resources/fonts/Scheherazade-Regular.ttf', 90)
        self.font_heading_three = pygame.font.Font('resources/fonts/Scheherazade-Regular.ttf', 45)
        self.font_regular_one = pygame.font.Font('resources/fonts/Scheherazade-Regular.ttf', 35)

        # Scenes
        self.scene = None
        self.menu_scene = MenuScene(self)
        self.options_scene = OptionsScene(self)
        self.game_scene = GameScene(self)
        self.set_scene("menu")

        # Dictionary
        self.dictionary = {}
        self.init_dictionary()

    def init_dictionary(self):
        # Load Word Dictionary
        with open("resources/words/words.json", encoding="utf8") as file:
            json_file = json.load(file)
            for i in range(len(json_file)):
                self.dictionary[json_file[i]['value']['word']] = {
                    'id': i,
                    'type': json_file[i]['value']['type'],
                    'level': json_file[i]['value']['level'],
                    'origin': '',
                    'meanings': '',
                    'completed': False }


    def set_scene(self, scene_name):
        if scene_name == "menu":
            self.scene = self.menu_scene
        elif scene_name == "game":
            self.scene = self.game_scene
        elif scene_name == "options":
            self.scene = self.options_scene

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.scene.handle_event(event)

    def update(self):
        self.scene.update()

    def render(self):
        self.scene.render(self.screen)

    def render_debug(self):
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Render mouse position and framerate
        mouse_pos_surface = self.font_scheherazade_reg.render(f"Mouse Position: {mouse_x}, {mouse_y}", True, (200, 200, 200))
        framerate_surface = self.font_scheherazade_reg.render(f"Framerate: {self.clock.get_fps()}", True, (200, 200, 200))

        self.screen.blit(mouse_pos_surface, (15, 650))
        self.screen.blit(framerate_surface, (15, 670))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

            self.render_debug()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()