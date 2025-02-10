import pygame
import sys

class MainPage:
    def __init__(self):
        pygame.init()
        
        # Налаштування вікна
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Minesweeper")
        
        # Шрифти
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.table = pygame.font.Font(None, 22)
        
        # Кнопки
        self.start_button = pygame.Rect(235, 133, 133, 68)
        self.records_button = pygame.Rect(10, 10, 150, 40)
        
        self.running = True
        self.show_menu()
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def show_menu(self):
        while self.running:
            self.screen.fill((200, 200, 200))
                       
            self.draw_text("Minesweeper", self.font, (0, 0, 0), 225, 30)            
            pygame.draw.rect(self.screen, (100, 100, 255), self.start_button)
            pygame.draw.rect(self.screen, (150, 150, 150), self.records_button)
            
            self.draw_text("Почати гру", self.small_font, (255, 255, 255), 249, 155)
            self.draw_text("Таблиця рекордів", self.table, (0, 0, 0), 17.5, 22)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False                       
        pygame.quit()
        sys.exit()
        
if __name__ == "__main__":
    MainPage()
