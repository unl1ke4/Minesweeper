import pygame
import sys
import random

class GameBoard:
    # Клас для генерації ігрового поля та роботи з ним
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self.generate_board()

    def generate_board(self):
       # Розміщення мін та обчислення значень навколо них
       self.place_mines()
       self.calculate_numbers()

    def place_mines(self):
        # Розміщення мін на полі
        while len(self.mine_positions) < self.mines:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r,c) not in self.mine_positions:
                self.mine_positions.add((r,c))
                self.board[r][c] -= 1 # -1 - міна

    def calculate_numbers(self):
        #Обчислення чисел навколо мін (1, 2...)
        directions = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for r, c in self.mine_positions:
            for directions_r, directions_c in directions:
                numbers_r, numbers_c = r + directions_r, c + directions_c
                if 0 <= numbers_r < self.rows and 0 <= numbers_c < self.cols and self.board[numbers_r][numbers_c] != -1:
                    self.board[numbers_r][numbers_c] += 1

    def print_info(self):
    # Вивід у консоль для тестування
        for row in self.board:
            print("".join(str(cell) if cell != -1 else "*" for cell in row))

class MainPage:
    def __init__(self):
        pygame.init()
        
        # Налаштування вікна
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Minesweeper")
        self.background = pygame.image.load("assets/fon.png").convert()

        # Шрифти
        self.font = pygame.font.Font("type/Play-Regular.ttf", 36)
        self.small_font = pygame.font.Font("type/Play-Regular.ttf", 28)

        # Кнопка "Почати гру"
        self.start = pygame.image.load("assets/Start.png").convert_alpha()
        self.start = pygame.transform.scale(self.start, (150, 75))

        self.running = True
        self.choosing_difficulty = False
        self.board = None  
        self.show_menu()

    def show_menu(self):
        while self.running:
            self.screen.fill((200, 200, 200))
            self.screen.blit(self.background, (-50, 0))
            
            # Назва гри
            text_surface = self.font.render("Minesweeper", True, (250, 250, 250))
            self.screen.blit(text_surface, (200, 30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            # Почати гру
            start_pos = (225, 150)
            start_rect = pygame.Rect(start_pos[0], start_pos[1], self.start.get_width(), self.start.get_height())

            if start_rect.collidepoint(mouse_pos) and mouse_pressed:
                self.choosing_difficulty = True

            self.screen.blit(self.start, start_pos)

            # Відображення вікна вибору складності
            if self.choosing_difficulty:
                self.show_difficulty_popup()

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()
        sys.exit()

    def show_difficulty_popup(self):
        # Відображає невелике вікно вибору складності
        popup_rect = pygame.Rect(175, 100, 250, 200)  
        buttons = {
            "Простий": pygame.Rect(200, 130, 200, 40),
            "Стандартний": pygame.Rect(200, 180, 200, 40),
            "Складний": pygame.Rect(200, 230, 200, 40),
        }

        while self.choosing_difficulty:
            self.screen.blit(self.background, (-50, 0))  
            pygame.draw.rect(self.screen, (60, 60, 60), popup_rect, border_radius=10)  
            
           
            title_surface = self.font.render("Оберіть складність", True, (255, 255, 255))
            self.screen.blit(title_surface, (135, 45))  

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            for name, rect in buttons.items():
                color = (80, 181, 250)
                if rect.collidepoint(mouse_pos):
                    if mouse_pressed:
                        color = (50, 100, 180)
                        if name == "Простий":
                            self.start_game(8, 8, 10)
                        elif name == "Стандартний":
                            self.start_game(10, 10, 20)
                        elif name == "Складний":
                            self.start_game(12, 12, 30)
                        self.choosing_difficulty = False
                    else:
                        color = (100, 200, 255)

                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                
                
                text_surface = self.small_font.render(name, True, (255, 255, 255))
                text_x = rect.x + (rect.width - text_surface.get_width()) // 2 
                text_y = rect.y + (rect.height - text_surface.get_height()) // 2
                self.screen.blit(text_surface, (text_x, text_y))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not popup_rect.collidepoint(event.pos):  
                        self.choosing_difficulty = False  

    def start_game(self, rows, cols, mines):
    # Ініціалізація гри із заданим рівнем складності
        self.game_board = GameBoard(rows, cols, mines)
        print(f"Початок гри! Розмір {rows}x{cols}, міни: {mines}")
        self.game_board.print_info()

    """def start_easy_mode(self):
        # Запускає гру в простому режимі
        print("Запуск простого режиму...")"""

if __name__ == "__main__":
    MainPage()
