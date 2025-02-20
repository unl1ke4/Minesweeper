import pygame
import sys
import random

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
FLAG_COLOR = (255, 165, 0)

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
        self.game_board = GameBoard(rows, cols, mines)
        self.revealed = [[False] * cols for _ in range(rows)]
        self.flags = set()
        self.running = True
        
        self.run_game()

    def draw_board(self):
        self.screen.fill(WHITE)

        pygame.draw.rect(self.screen, GRAY, (0, 0, self.width, HEADER_HEIGHT))

        for r in range(self.rows):
            for c in range(self.cols):
                x, y = c * CELL_SIZE, r * CELL_SIZE + HEADER_HEIGHT
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                if self.revealed[r][c]:
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)
                    if self.game_board.board[r][c] == -1:
                        pygame.draw.circle(self.screen, RED, rect.center, CELL_SIZE // 3)
                    elif self.game_board.board[r][c] > 0:
                        text = self.font.render(str(self.game_board.board[r][c]), True, BLUE)
                        self.screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 4))
                else:
                    pygame.draw.rect(self.screen, GRAY, rect)
                    if (r, c) in self.flags:
                        pygame.draw.polygon(self.screen, FLAG_COLOR, [(x + 5, y + 25), (x + 15, y + 5), (x + 25, y + 25)])
                
                pygame.draw.rect(self.screen, BLACK, rect, 2)

    def reveal_cell(self, r, c):
        if (r, c) in self.flags or self.revealed[r][c]:
            return
        
        self.revealed[r][c] = True
        
        if self.game_board.board[r][c] == -1:
            self.running = False
            print("💥 Вибух! Гра закінчена!")
        elif self.game_board.board[r][c] == 0:
            self.reveal_adjacent(r, c)
    
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
            elif len(self.flags) < self.mines:
                self.flags.add((r, c))
    
    def run_game(self):
        while self.running:
            self.draw_board()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
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
            
            # Назва гри
            text_surface = self.font.render("Minesweeper", True, (250, 250, 250))
            self.screen.blit(text_surface, (200, 30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            # Почати гру
            start_pos = (225, 150)
            start_rect = pygame.Rect(start_pos[0], start_pos[1], self.start.get_width(), self.start.get_height())

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
            else:
                self.mouse_held = False
                self.screen.blit(self.start, start_pos)

            if self.choosing_difficulty:
                self.show_difficulty_popup()

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()
        sys.exit()

    def show_difficulty_popup(self):
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
        self.running = False 
        MinesweeperGame(rows, cols, mines) 

    """def start_easy_mode(self):
        # Запускає гру в простому режимі
        print("Запуск простого режиму...")"""

if __name__ == "__main__":
    MainPage()
