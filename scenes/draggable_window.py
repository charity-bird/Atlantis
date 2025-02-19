import pygame

class DraggableWindow:
    def __init__(self, x, y, width, height, scene, header_text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0

        self.scene = scene

        self.header_text = header_text
        self.words = []
        self.word_surfaces = self.create_word_surfaces()
        self.header_font = self.scene.game.font_heading_three
        self.content_font = self.scene.game.font_heading_three

        self.header = self.header_font.render(header_text, True, 'black')
        self.header_height = 40

    def update_words(self, new_words):
        self.words = new_words
        self.word_surfaces = self.create_word_surfaces()

    def create_word_surfaces(self):
        return [self.content_font.render(word, True, 'white') for word in self.words]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.is_mouse_on_window(mouse_x, mouse_y):
                self.is_dragging = True
                self.offset_x = mouse_x - self.x
                self.offset_y = mouse_y - self.y

        if event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.x = event.pos[0] - self.offset_x
                self.y = event.pos[1] - self.offset_y

        if event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False

    def is_mouse_on_window(self, mouse_x, mouse_y):
        """ Check if the mouse is inside the window's boundaries"""
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    def render(self, screen):
        # Draw the draggable window (including the header)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2) # Window border
        pygame.draw.rect(screen, (0, 0, 0), (self.x+2, self.y+2, self.width-4, self.height-4)) # Window inner colour

        # Draw the header (white)
        pygame.draw.rect(screen, 'white', (self.x, self.y, self.width, self.header_height))

        # Center the header text inside the header
        text_rect = self.header.get_rect(center=(self.x + self.width // 2, self.y + (self.header_height+7) // 2))
        screen.blit(self.header, text_rect)

        # Draw the content area below the header (rendering the list of words)
        content_rect = pygame.Rect(self.x, self.y + self.header_height, self.width, self.height - self.header_height)
        pygame.draw.rect(screen, 'white', content_rect, 1)

        # # Render the list of words as the content of the window
        # y_offset = self.y + self.header_height + 10 # Start drawing content a little below the header
        # for i, word_surface in enumerate(self.word_surfaces):
        #     screen.blit(word_surface, (self.x + 10, y_offset - 25 + i * 30)) # Add some padding from the left side
        #     #y_offset += word_surface.get_height() +5 # Space between lines

        for i, word_surface in enumerate(self.word_surfaces[:10]):
            screen.blit(word_surface, (self.x + 10, self.y + 40 + i * 30))
        for i, word_surface in enumerate(self.word_surfaces[10:]):
            screen.blit(word_surface, (self.x + 260, self.y + 40 + i * 30))