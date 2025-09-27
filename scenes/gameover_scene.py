import pygame

from scenes.scene import Scene

class GameOverScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.word = ""
        self.meanings = None

        self.text_game_over = self.game.font_title.render("Game Over", True, 'red')

    def setWordAndMeanings(self, word, meanings):
        self.word = word
        self.meanings = meanings
        self.text_correct_word = self.game.font_heading_three.render(f"The correct word was: {self.word}", True, 'white')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.game.menu_escape_sound.play()
                self.game.set_scene("menu")
    
    def render(self, screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        screen.blit(self.text_game_over, (self.game.screen_width / 2 - 150, self.game.screen_height / 8))
        screen.blit(self.text_correct_word, (self.game.screen_width / 2 - 200, self.game.screen_height / 8 + 100))

        # Display word meanings
        text = []
        for part_of_speech in self.meanings:
            text.append(f"({part_of_speech['partOfSpeech']})")

            for definition in part_of_speech['definitions'][0:2]:
                for i in range(0, len(definition['definition']), 100)[0:3]:
                    text.append(f" {definition['definition'][0+i:100+i]}")

        self.text_word_meanings = []
        for i in range(len(text)):
            self.text_word_meanings.append(self.game.font_regular_one.render(text[i], True, 'white'))

        for i in range(len(self.text_word_meanings)):
            screen.blit(self.text_word_meanings[i], (self.game.screen_width / 2 - 530, self.game.screen_height / 3 + i * 35))
