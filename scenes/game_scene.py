import pygame
import json
import requests
import random
from scenes.scene import Scene

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.word = ""
        self.origin = ""
        self.meanings = ""
        self.guess = ""
        self.number_of_words = 0
        self.correct = False
        self.text_word_meanings = []

        self.text_game_score = self.game.font_heading_three.render(f"Score: {self.number_of_words}", True, 'white')
        self.text_word_origin = self.game.font_heading_three.render(f"Origin: {self.origin}", True, 'white')
        self.text_word_meanings = self.game.font_heading_three.render(f"{self.meanings}", True, 'white')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_scene("menu")
            elif event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g,
                               pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n,
                               pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u,
                               pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z]:
                self.guess += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                self.guess = self.guess[:-1]
            elif event.key == pygame.K_RETURN:
                self.check_guess()

    def check_guess(self):
        if self.word != self.guess:
            self.guess += "[x]"
        if self.word == self.guess and self.correct == False:
            self.guess += " -> correct!"
            self.correct = True
        elif self.correct == True:
            self.correct = False
            self.word = ""
            self.guess = ""
            self.number_of_words += 1

    def get_word_definitions(self):
        self.word = random.choice([key for key, value in self.game.dictionary.items() if not value['completed']])
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}")
        try:
            # self.game.dictionary[self.word]['origin'] = response.json()[0]['origin']
            self.game.dictionary[self.word]['meanings'] = response.json()[0]['meanings']
        except Exception as e:
            print(e)

        self.origin = self.game.dictionary[self.word]['origin']
        self.meanings = self.game.dictionary[self.word]['meanings']

        print(f"JSON Response: {response.json()}")
        print(f"word: {self.word}")
        print(f"origin: {self.origin}")
        print(f"meanings: {self.meanings}")

        if not self.meanings:
            self.get_word_definitions()

    def render(self, screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        if self.word == "":
            self.get_word_definitions()

            text = []
            for part_of_speech in self.meanings:
                text.append(f"({part_of_speech['partOfSpeech']})")

                for definition in part_of_speech['definitions'][0:2]:
                    for i in range(0, len(definition['definition']), 100)[0:3]:
                        text.append(f" {definition['definition'][0+i:100+i]}")

            self.text_word_meanings = []
            for i in range(len(text)):
                self.text_word_meanings.append(self.game.font_regular_one.render(text[i], True, 'white'))

            self.text_game_score = self.game.font_heading_three.render(f"Score: {self.number_of_words}", True, 'white')
            self.text_word_origin = self.game.font_heading_three.render(f"Origin: {self.origin}", True, 'white')

        self.text_player_guess = self.game.font_heading_three.render(f"_{self.guess}_", True, 'white')

        screen.blit(self.text_game_score, (self.game.screen_width / 2 - 140, self.game.screen_height / 5 - 100))
        screen.blit(self.text_word_origin, (self.game.screen_width / 2 - 530, self.game.screen_height / 5 - 35))
        screen.blit(self.text_player_guess, (self.game.screen_width / 2, 4 * self.game.screen_height / 5))

        for i in range(len(self.text_word_meanings)):
            screen.blit(self.text_word_meanings[i], (self.game.screen_width / 2 - 530, self.game.screen_height / 5 + i * 35))

