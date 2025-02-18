# Example file showing a circle moving on screen
import pygame
import json
import requests
import random

# pygame setup
pygame.init()
screen_height = 1280
screen_width = 720
screen = pygame.display.set_mode((screen_height, screen_width))
clock = pygame.time.Clock()
running = True

url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

dictionary = {}
# Load Word Dictionary

with open("resources/words/words.json", encoding="utf8") as file:
    json_file = json.load(file)
    for i in range(len(json_file)):
        dictionary[json_file[i]['value']['word']] = {
            'id': i,
            'type': json_file[i]['value']['type'],
            'level': json_file[i]['value']['level'],
            'origin': '',
            'meanings': '',
            'completed': False
        }

# try:
#     with open("resources/words/words_meanings.json", encoding="utf8") as file:
#         dictionary = json.load(file)
# except:
#     print("Could not create a dictionary")
#     with open("resources/words/words.json", encoding="utf8") as file:
#         json_file = json.load(file)
#         for i in range(len(json_file)):
#             dictionary[json_file[i]['value']['word']] = {
#                 'id': i,
#                 'type': json_file[i]['value']['type'],
#                 'level': json_file[i]['value']['level'],
#                 'origin': '',
#                 'meanings': '',
#                 'completed': False
#             }

# print (dictionary)

with open("resources/words/words_meanings.json", 'w', encoding="utf8") as file:
    json.dump(dictionary, file)

# Scene
scene_state = 0

# Menu Logic
menu_cursor_pos = 0

# Mouse Position
mouse_x = 0
mouse_y = 0

# Game Logic
number_of_words = 0
word = ""
origin = ""
meanings = ""
guess = ""

# Fonts
font_scheherazade_reg = pygame.font.Font('resources/fonts/Scheherazade-Regular.ttf', 30)
font_scheherazade_bold = pygame.font.Font('resources/fonts/Scheherazade-Bold.ttf', 30)
font_title = pygame.font.Font('resources/fonts/Scheherazade-Regular.ttf', 90)
font_heading_three = pygame.font.Font('resources/fonts/Scheherazade-Regular.ttf', 45)
font_regular_one = pygame.font.Font('resources/fonts/Scheherazade-Regular.ttf', 35)

# Static text
title_surface = font_title.render("Atlantis", True, (255,255,255))
menu_option_start = font_heading_three.render("Start", True, (255,255,255))
menu_option_options = font_heading_three.render("Options", True, (255,255,255))
menu_option_quit = font_heading_three.render("Quit", True, (255,255,255))

options_title = font_heading_three.render("Options", True, (255, 255, 255))
options_bg_color = font_heading_three.render("Background Colour", True, (255,255,255))

text_game_score = font_heading_three.render(f"Score: {number_of_words}", True, (255, 255, 255))
text_word_origin = font_heading_three.render(f"Origin: {origin}", True, 'white')
text_word_meanings = font_heading_three.render(f"{meanings}", True, (255, 255, 255))


def scene_menu():
    screen.blit(title_surface, (screen_height / 2 - 108, screen_width / 3))
    screen.blit(menu_option_start, (screen_height / 2 - 32, screen_width / 3 + 120))
    screen.blit(menu_option_options, (screen_height / 2 - 52, screen_width / 3 + 155))
    screen.blit(menu_option_quit, (screen_height / 2 - 30, screen_width / 3 + 190))

    if (menu_cursor_pos == 0):
        pygame.draw.circle(screen, "white", (screen_height / 2 - 42, screen_width / 3 + 155), 5)
    elif (menu_cursor_pos == 1):
        pygame.draw.circle(screen, "white", (screen_height / 2 - 62, screen_width / 3 + 190), 5)
    elif (menu_cursor_pos == 2):
        pygame.draw.circle(screen, "white", (screen_height / 2 - 42, screen_width / 3 + 225), 5)

def scene_options():
    screen.blit(options_title, (screen_height / 2, screen_width / 5))
    screen.blit(options_bg_color, (screen_height / 2, screen_width / 5 + 100))

def scene_game():
    global word, origin, meanings, guess, text_game_score, text_word_origin, text_word_meanings
    if word == "":
        word = random.choice([key for key, value in dictionary.items() if not value['completed']])
        print(word)
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        print(response.json()[0])
        try:
            dictionary[word]['origin'] = response.json()[0]['origin']
        except Exception as e:
            print(e)
        dictionary[word]['meanings'] = response.json()[0]['meanings']
        origin = dictionary[word]['origin']
        meanings = dictionary[word]['meanings']

        text = []
        for part_of_speech in meanings:
            text.append(f"({part_of_speech['partOfSpeech']})")

            for definition in part_of_speech['definitions'][0:2]:
                for i in range(0, len(definition['definition']), 100)[0:3]:
                    text.append(f" {definition['definition'][0+i:100+i]}")

        text_word_meanings = []
        for i in range(len(text)):
            text_word_meanings.append(font_regular_one.render(text[i], True, (255, 255, 255)))

        text_game_score = font_heading_three.render(f"Score: {number_of_words}", True, (255, 255, 255))
        text_word_origin = font_heading_three.render(f"Origin: {origin}", True, 'white')

    text_player_guess = font_heading_three.render(f"_{guess}_", True, 'white')

    screen.blit(text_game_score, (screen_height / 2 - 140, screen_width / 5 - 100))
    screen.blit(text_word_origin, (screen_height / 2 - 530, screen_width / 5 - 35))
    screen.blit(text_player_guess, (screen_height / 2, 4 * screen_width / 5))

    for i in range(len(text_word_meanings)):
        screen.blit(text_word_meanings[i], (screen_height / 2 - 530, screen_width / 5 + i * 35))

correct = False
def check_guess():
    global correct, guess, word, number_of_words
    if word != guess:
        guess += "[x]"
    if word == guess and correct == False:
        guess += " -> correct!"
        correct = True
    elif correct == True:
        correct = False
        word = ""
        guess = ""
        number_of_words += 1


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if scene_state == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu_cursor_pos += 1
                    if menu_cursor_pos > 2:
                        menu_cursor_pos = 0
                elif event.key == pygame.K_UP:
                    menu_cursor_pos -= 1
                    if menu_cursor_pos < 0:
                        menu_cursor_pos = 2
                elif menu_cursor_pos == 0 and (event.key == pygame.K_a or event.key == pygame.K_RETURN):
                    scene_state = 1 # Main game
                elif menu_cursor_pos == 1 and (event.key == pygame.K_a or event.key == pygame.K_RETURN):
                    scene_state = 2 # Options menu
                elif menu_cursor_pos == 2 and (event.key == pygame.K_a or event.key == pygame.K_RETURN):
                    running = False # Quit

        elif scene_state == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene_state = 0
                elif event.key == pygame.K_a:
                    guess += 'a'
                elif event.key == pygame.K_b:
                    guess += 'b'
                elif event.key == pygame.K_c:
                    guess += 'c'
                elif event.key == pygame.K_d:
                    guess += 'd'
                elif event.key == pygame.K_e:
                    guess += 'e'
                elif event.key == pygame.K_f:
                    guess += 'f'
                elif event.key == pygame.K_g:
                    guess += 'g'
                elif event.key == pygame.K_h:
                    guess += 'h'
                elif event.key == pygame.K_i:
                    guess += 'i'
                elif event.key == pygame.K_j:
                    guess += 'j'
                elif event.key == pygame.K_k:
                    guess += 'k'
                elif event.key == pygame.K_l:
                    guess += 'l'
                elif event.key == pygame.K_m:
                    guess += 'm'
                elif event.key == pygame.K_n:
                    guess += 'n'
                elif event.key == pygame.K_o:
                    guess += 'o'
                elif event.key == pygame.K_p:
                    guess += 'p'
                elif event.key == pygame.K_q:
                    guess += 'q'
                elif event.key == pygame.K_r:
                    guess += 'r'
                elif event.key == pygame.K_s:
                    guess += 's'
                elif event.key == pygame.K_t:
                    guess += 't'
                elif event.key == pygame.K_u:
                    guess += 'u'
                elif event.key == pygame.K_v:
                    guess += 'v'
                elif event.key == pygame.K_w:
                    guess += 'w'
                elif event.key == pygame.K_x:
                    guess += 'x'
                elif event.key == pygame.K_y:
                    guess += 'y'
                elif event.key == pygame.K_z:
                    guess += 'z'
                elif event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                elif event.key == pygame.K_RETURN:
                    check_guess()

        elif scene_state == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene_state = 0


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Render some text
    mouse_pos_surface = font_scheherazade_reg.render(f"Mouse Position: {mouse_x}, {mouse_y}", True, (200, 200, 200))
    framerate_surface = font_scheherazade_reg.render(f"Framerate: {clock.get_fps()}", True, (200, 200, 200))

    screen.blit(mouse_pos_surface, (15, 650))
    screen.blit(framerate_surface, (15, 670))

    if (scene_state == 0):
        scene_menu()
    elif (scene_state == 1):
        scene_game()
    elif (scene_state == 2):
        scene_options()



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()