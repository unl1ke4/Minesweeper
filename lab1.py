import pygame
import sys

class MainPage:
    def __init__(self):
        pygame.init()
        
        # Налаштування вікна
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Minesweeper")
        
        self.background = pygame.image.load("D:/Нова папка/git/Minesweeper/assets/fon.png").convert()

        # Шрифти
        self.font = pygame.font.Font("D:/Нова папка/git/Minesweeper/type/Play-Regular.ttf", 36)
        self.small_font = pygame.font.Font("D:/Нова папка/git/Minesweeper/type/Play-Regular.ttf", 28)
        self.table = pygame.font.Font("D:/Нова папка/git/Minesweeper/type/Play-Bold.ttf", 16)
        
        # Кнопки
        
        self.records_button = pygame.Rect(227, 250, 150, 40)
        
        self.icon = pygame.image.load("D:/Нова папка/git/Minesweeper/assets/Start.png").convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (150, 75))


        self.running = True
        self.show_menu()
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def show_menu(self):
        while self.running:
            self.screen.fill((200, 200, 200))
            # Фон
            self.screen.blit(self.background, (-50, 0))          
            self.draw_text("Minesweeper", self.font, (250, 250, 250), 200, 30)            
            

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

             # Почати гру
            icon_pos = (225, 150)
            if pygame.Rect(icon_pos[0], icon_pos[1], self.icon.get_width(), self.icon.get_height()).collidepoint(mouse_pos):
                if mouse_pressed:
                    darkened_icon = self.icon.copy()
                    darkened_icon.fill((150, 150, 150, 100), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(darkened_icon, icon_pos)
                    
                else:
                    self.screen.blit(self.icon, icon_pos)
            else:
                self.screen.blit(self.icon, icon_pos)
            
            self.records_pressed = False 

            if self.records_button.collidepoint(mouse_pos):
                if mouse_pressed:
                    self.records_pressed = True  # Запам’ятовуємо, що кнопку натиснули
                elif self.records_pressed:  
                    self.records_pressed = False  # Скидаємо стан після обробки

                color = (180, 180, 180) if mouse_pressed else (200, 200, 200)  # Затемнення при натисканні
            else:
                color = (80, 181, 250)  # Звичайний колір

            pygame.draw.rect(self.screen, color, self.records_button, border_radius=8)    
            self.draw_text("Таблиця рекордів", self.table, (250, 250, 250), 232, 260)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False                       
        pygame.quit()
        sys.exit()
        
if __name__ == "__main__":
    MainPage()
