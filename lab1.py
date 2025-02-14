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
        self.start = pygame.image.load("D:/Нова папка/git/Minesweeper/assets/Start.png").convert_alpha()
        self.start = pygame.transform.scale(self.start, (150, 75))
        self.table = pygame.image.load("D:/Нова папка/git/Minesweeper/assets/Table.png").convert_alpha()
        self.table = pygame.transform.scale(self.table, (150, 55))

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
            start_pos = (225, 150)
            if pygame.Rect(start_pos[0], start_pos[1], self.start.get_width(), self.start.get_height()).collidepoint(mouse_pos):
                if mouse_pressed:
                    darkened_start = self.start.copy()
                    darkened_start.fill((150, 150, 150, 200), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(darkened_start, start_pos)
                    
                else:
                    self.screen.blit(self.start, start_pos)
            else:
                self.screen.blit(self.start, start_pos)

            #Таблиця рекордів
            table_pos = (227, 235)
            if pygame.Rect(table_pos[0], table_pos[1], self.table.get_width(), self.table.get_height()).collidepoint(mouse_pos):
                if mouse_pressed:
                    darkened_table = self.table.copy()
                    darkened_table.fill((150, 150, 150, 200), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(darkened_table, table_pos)
                    
                else:
                    self.screen.blit(self.table, table_pos)
            else:
                self.screen.blit(self.table, table_pos)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False                       
        pygame.quit()
        sys.exit()
        
if __name__ == "__main__":
    MainPage()
