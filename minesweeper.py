import pygame
import sys
import random
import time

class GameBoard:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self.generate_board()

    def generate_board(self):
       self.place_mines()
       self.calculate_numbers()

    def place_mines(self):
        while len(self.mine_positions) < self.mines:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r,c) not in self.mine_positions:
                self.mine_positions.add((r,c))
                self.board[r][c] -= 1 

    def calculate_numbers(self):
        directions = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for r, c in self.mine_positions:
            for directions_r, directions_c in directions:
                numbers_r, numbers_c = r + directions_r, c + directions_c
                if 0 <= numbers_r < self.rows and 0 <= numbers_c < self.cols and self.board[numbers_r][numbers_c] != -1:
                    self.board[numbers_r][numbers_c] += 1


WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FLAG_COLOR = (80, 181, 250)

CELL_SIZE = 30  
HEADER_HEIGHT = 50  

class MinesweeperGame:
    def __init__(self, rows, cols, mines):
        pygame.init()
        
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.width = cols * CELL_SIZE
        self.height = rows * CELL_SIZE + HEADER_HEIGHT
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper")
        
        self.font = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 18)  # Шрифт для таймера і лічильника
        self.font_numbers = pygame.font.Font(None, 24)  # Шрифт для чисел на полі
        self.game_board = GameBoard(rows, cols, mines)
        self.revealed = [[False] * cols for _ in range(rows)]
        self.flags = set()
        self.running = True
        self.paused = False
        
        self.start_time = time.time()

        self.mines_counter = mines
        
        # Кнопки
        self.flag_button = pygame.Rect(10, 10, 30, 30)
        self.flag_button_pressed = False  
        self.flag_icon = pygame.image.load("assets/flag.png")  
        self.flag_icon = pygame.transform.scale(self.flag_icon, (CELL_SIZE, CELL_SIZE))
        self.pause_button = pygame.Rect(self.width - 40, 10, 30, 30)

        self.run_game()
        

    def check_win(self):
     for r in range(len(self.game_board.board)):
        for c in range(len(self.game_board.board[0])):
            if self.game_board.board[r][c] != -1 and not self.revealed[r][c]:
                return  # Гра ще не виграна
    
     self.show_win_message()  # Відображаємо вікно виграшу


    def show_win_message(self):
        """ Викликає екран завершення гри після виграшу """
        self.running = False  # Зупиняємо гру
        self.win_screen()  # Викликаємо вікно виграшу

    def win_screen(self):
        """ Показує екран виграшу з двома кнопками: 'Головне меню' і 'Рестарт' """
        font = pygame.font.Font("type/Play-Regular.ttf", 20)
        
        menu_width, menu_height = 205, 150
        menu_x, menu_y = (self.width - menu_width) // 2, (self.height - menu_height) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        
        button_width, button_height = 142, 38
        restart_button = pygame.Rect(menu_x + 32, menu_y + 45, button_width, button_height)
        menu_button = pygame.Rect(menu_x + 32, menu_y + 95, button_width, button_height)

        while True:
            self.screen.fill((50, 50, 50))  # Фон

            pygame.draw.rect(self.screen, (0, 200, 0), menu_rect, border_radius=10)
            
            text = font.render("Ви виграли!", True, WHITE)
            self.screen.blit(text, (menu_x + 41, menu_y + 15))

            pygame.draw.rect(self.screen, (80, 181, 250), restart_button, border_radius=5)
            pygame.draw.rect(self.screen, (80, 181, 250), menu_button, border_radius=5)

            restart_text = font.render("Рестарт", True, WHITE)
            menu_text = font.render("Головне меню", True, WHITE)

            self.screen.blit(restart_text, (restart_button.x + 36, restart_button.y + 8))
            self.screen.blit(menu_text, (menu_button.x + 5, menu_button.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        self.__init__(self.rows, self.cols, self.mines)  # Перезапускаємо гру
                        return
                    elif menu_button.collidepoint(event.pos):
                        self.running = False
                        return MainPage()  # Повертаємось у головне меню


    def draw_board(self):
        self.screen.fill(WHITE)

        pygame.draw.rect(self.screen, GRAY, (0, 0, self.width, HEADER_HEIGHT))
        
        # Віконце для таймера та лічильника мін
        pygame.draw.rect(self.screen, DARK_GRAY, (self.width // 2 - 50, 5, 100, 40), border_radius=5)

    # Таймер
        elapsed_time = int(time.time() - self.start_time)
        timer_text = self.font_small.render(f"Time: {elapsed_time}s", True, WHITE)
        self.screen.blit(timer_text, (self.width // 2 - 40, 8)) 

    # Лічильник мін 
        mines_text = self.font_small.render(f"Mines: {self.mines_counter}", True, WHITE)
        self.screen.blit(mines_text, (self.width // 2 - 40, 24))  


        pygame.draw.rect(self.screen, DARK_GRAY, self.pause_button)
        pygame.draw.rect(self.screen, WHITE, (self.pause_button.x + 8, self.pause_button.y + 5, 5, 20))
        pygame.draw.rect(self.screen, WHITE, (self.pause_button.x + 18, self.pause_button.y + 5, 5, 20))


        for r in range(self.rows):
            for c in range(self.cols):
                x, y = c * CELL_SIZE, r * CELL_SIZE + HEADER_HEIGHT
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                if self.revealed[r][c]:
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)
                    if self.game_board.board[r][c] == -1:
                        pygame.draw.circle(self.screen, RED, rect.center, CELL_SIZE // 3)
                    elif self.game_board.board[r][c] > 0:
                        text = self.font_numbers.render(str(self.game_board.board[r][c]), True, BLUE)
                        self.screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 4))
                else:
                    pygame.draw.rect(self.screen, GRAY, rect)
                    if (r, c) in self.flags:
                        self.screen.blit(self.flag_icon, (x, y))
                
                pygame.draw.rect(self.screen, BLACK, rect, 2)

    def pause_menu(self):
        self.font = pygame.font.Font("type/Play-Regular.ttf", 14)

        menu_width = 140
        menu_height = 160
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

        button_width = 120
        button_height = 28
        button_spacing = 12  

        buttons = {
            "Продовжити": pygame.Rect(menu_x + (menu_width - button_width) // 2, menu_y + 25, button_width, button_height),
            "Рестарт": pygame.Rect(menu_x + (menu_width - button_width) // 2, menu_y + 25 + button_height + button_spacing, button_width, button_height),
            "Головне меню": pygame.Rect(menu_x + (menu_width - button_width) // 2, menu_y + 25 + 2 * (button_height + button_spacing), button_width, button_height)
        }

        while self.paused:
            pygame.draw.rect(self.screen, (60, 60, 60), menu_rect, border_radius=10)

            for name, rect in buttons.items():
                pygame.draw.rect(self.screen, FLAG_COLOR, rect, border_radius=8)
                text = self.font.render(name, True, BLACK)
                text_x = rect.x + (rect.width - text.get_width()) // 2
                text_y = rect.y + (rect.height - text.get_height()) // 2
                self.screen.blit(text, (text_x, text_y))

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons["Продовжити"].collidepoint(event.pos):
                        self.paused = False
                    elif buttons["Рестарт"].collidepoint(event.pos):
                        self.__init__(self.rows, self.cols, self.mines)
                    elif buttons["Головне меню"].collidepoint(event.pos):
                        self.running = False
                        self.paused = False
                        return MainPage()

    def reveal_cell(self, r, c):
        if (r, c) in self.flags or self.revealed[r][c]:
            return
        
        self.revealed[r][c] = True
        
        if self.game_board.board[r][c] == -1:
            self.show_explosion_message()  # Викликаємо функцію для показу вибуху
        elif self.game_board.board[r][c] == 0:
            self.reveal_adjacent(r, c)
        self.check_win()  # Додаємо перевірку на виграш

        

    def show_explosion_message(self):
        """ Викликає екран завершення гри після вибуху """
        self.running = False  # Зупиняємо гру
        self.game_over_screen()  # Викликаємо вікно програшу

    def game_over_screen(self):
        """ Показує екран програшу з двома кнопками: 'Головне меню' і 'Рестарт' """
        font = pygame.font.Font("type/Play-Regular.ttf", 20)
        
        menu_width, menu_height = 205, 150
        menu_x, menu_y = (self.width - menu_width) // 2, (self.height - menu_height) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        
        button_width, button_height = 142, 38
        restart_button = pygame.Rect(menu_x + 32, menu_y + 45, button_width, button_height)
        menu_button = pygame.Rect(menu_x + 32, menu_y + 95, button_width, button_height)

        while True:
            self.screen.fill((50, 50, 50))  # Фон

            pygame.draw.rect(self.screen, (200, 0, 0), menu_rect, border_radius=10)
            
            text = font.render("Ви програли!", True, WHITE)
            self.screen.blit(text, (menu_x + 41, menu_y + 15))

            pygame.draw.rect(self.screen, (0, 200, 0), restart_button, border_radius=5)
            pygame.draw.rect(self.screen, (80, 181, 250), menu_button, border_radius=5)

            restart_text = font.render("Рестарт", True, WHITE)
            menu_text = font.render("Головне меню", True, WHITE)

            self.screen.blit(restart_text, (restart_button.x + 36, restart_button.y + 8))
            self.screen.blit(menu_text, (menu_button.x + 5, menu_button.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        self.__init__(self.rows, self.cols, self.mines)  # Перезапускаємо гру
                        return
                    elif menu_button.collidepoint(event.pos):
                        self.running = False
                        return MainPage()  # Повертаємось у головне меню

    
    def reveal_adjacent(self, r, c):
        directions = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.revealed[nr][nc]:
                self.reveal_cell(nr, nc)
    
    def handle_click(self, pos, button):
        if pos[1] < HEADER_HEIGHT:
            return
        
        r = (pos[1] - HEADER_HEIGHT) // CELL_SIZE
        c = pos[0] // CELL_SIZE
        
        if button == 1:  
            self.reveal_cell(r, c)
        elif button == 3:  
            if (r, c) in self.flags:
                self.flags.remove((r, c))
                self.mines_counter += 1  # Якщо знімаємо прапорець, додаємо назад до лічильника
            elif len(self.flags) < self.mines:
                self.flags.add((r, c))
                self.mines_counter -= 1  # Якщо ставимо прапорець, зменшуємо лічильник
        #Флаг
        if self.flag_button.collidepoint(pos):  
            self.flag_button_pressed = not self.flag_button_pressed  
            self.draw_board() 
            pygame.display.flip()  

    def run_game(self):
        while self.running:
            self.draw_board()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button.collidepoint(event.pos):  # Перевіряємо, чи натиснули паузу
                        self.paused = True
                        self.pause_menu()
                    else:
                        self.handle_click(event.pos, event.button)



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
         
        self.show_menu()

    def show_menu(self):
        while self.running:
            self.screen.fill((200, 200, 200))
            self.screen.blit(self.background, (-50, 0))

            text_surface = self.font.render("Minesweeper", True, (250, 250, 250))
            self.screen.blit(text_surface, (200, 30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            # Почати гру
            start_pos = (225, 150)
            start_rect = pygame.Rect(start_pos[0], start_pos[1], self.start.get_width(), self.start.get_height())

            # Вийти з гри
            exit_pos = (229, 250)
            exit_rect = pygame.Rect(exit_pos[0], exit_pos[1], 145, 75)

            if start_rect.collidepoint(mouse_pos):
                if mouse_pressed and not self.mouse_held:
                    self.mouse_held = True
                    darkened_start = self.start.copy()
                    darkened_start.fill((150, 150, 150, 200), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(darkened_start, start_pos)
                elif not mouse_pressed and self.mouse_held:
                    self.mouse_held = False
                    self.choosing_difficulty = True
                    self.screen.blit(self.start, start_pos)
                else:
                    self.screen.blit(self.start, start_pos)

            elif exit_rect.collidepoint(mouse_pos):
                if mouse_pressed:
                    pygame.quit()
                    sys.exit()
            else:
                self.mouse_held = False
                self.screen.blit(self.start, start_pos)

            pygame.draw.rect(self.screen, (240, 0, 0), exit_rect, border_radius=8)
            exit_text = self.font.render("Вихід", True, (255, 255, 255))
            self.screen.blit(exit_text, (exit_pos[0] + 27, exit_pos[1] + 17))

            if self.choosing_difficulty:
                self.show_difficulty_popup()
             
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()
        sys.exit()

    def show_difficulty_popup(self):
        popup_rect = pygame.Rect(175, 110, 250, 230)  
        buttons = {
            "Простий": pygame.Rect(200, 130, 200, 40),
            "Стандартний": pygame.Rect(200, 180, 200, 40),
            "Складний": pygame.Rect(200, 230, 200, 40),
            "Назад": pygame.Rect(200, 280, 200, 40),
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
                        elif name == "Назад":
                            return 
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
                elif name == "Назад":
                    if not popup_rect.collidepoint(event.pos):  
                        self.choosing_difficulty = False  

    def start_game(self, rows, cols, mines):
        self.running = False 
        MinesweeperGame(rows, cols, mines) 


if __name__ == "__main__":
    MainPage()
