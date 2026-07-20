import pygame
import random
import time
import pyttsx3
import threading


WIDTH, HEIGHT = 600, 750 
FPS = 60

BG_COLOR    = (45, 52, 54)   
HEADER_COLOR = (34, 47, 62)  
RED_DIM     = (214, 48, 49)  
GREEN_DIM   = (38, 222, 129) 
BLUE_DIM    = (69, 170, 242) 
YELLOW_DIM  = (247, 183, 49) 
WHITE       = (255, 255, 255)
BUTTON_HOVER = (99, 110, 114)

class NeuroPlay:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("NeuroPlay - Intelligent Game")
        self.clock = pygame.time.Clock()

        self.state = "MENU"
        self.mode = ""
        self.ai_algorithm = None
        self.ai_turn_done = False

        size = 250
        gap = 20
        self.buttons = {
            "red":    pygame.Rect(WIDTH//2 - size - gap//2, 200, size, size),
            "green":  pygame.Rect(WIDTH//2 + gap//2, 200, size, size),
            "blue":   pygame.Rect(WIDTH//2 - size - gap//2, 200 + size + gap, size, size),
            "yellow": pygame.Rect(WIDTH//2 + gap//2, 200 + size + gap, size, size)
        }

        self.sequence = []
        self.player_sequence = []
        self.level = 0
        self.score = 0
        self.waiting_for_input = False
        self.running = True

        self.ai_buttons = {
            "Minimax": pygame.Rect(WIDTH//2 - 150, 250, 300, 60),
            "BFS": pygame.Rect(WIDTH//2 - 150, 330, 300, 60),
            "A*": pygame.Rect(WIDTH//2 - 150, 410, 300, 60),
        }


    def speak(self, text):
        def _run():
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.say(text)
            engine.runAndWait()
        threading.Thread(target=_run, daemon=True).start()

    def display_text(self, text, x, y, size=30, color=WHITE, center=False):
        font = pygame.font.SysFont("Arial", size, bold=True)
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        rect.topleft = (x, y)
        if center:
            rect.center = (x, y)
        self.screen.blit(surface, rect)


    def draw_menu(self):
        self.screen.fill(BG_COLOR)
        self.display_text("NeuroPlay Game", WIDTH//2, 80, size=50, center=True)
        self.display_text("Select Game Mode:", WIDTH//2, 160, size=25, color=YELLOW_DIM, center=True)

        self.modes_buttons = {
            "Visual Mode": pygame.Rect(WIDTH//2 - 150, 250, 300, 50),
            "Audio Mode":  pygame.Rect(WIDTH//2 - 150, 320, 300, 50),
            "Mixed Mode":  pygame.Rect(WIDTH//2 - 150, 390, 300, 50),
            "Agent Mode (AI)": pygame.Rect(WIDTH//2 - 150, 460, 300, 50)
        }

        for text, rect in self.modes_buttons.items():
            color = HEADER_COLOR
            if rect.collidepoint(pygame.mouse.get_pos()):
                color = BUTTON_HOVER

            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=10)
            self.display_text(text, rect.centerx, rect.centery, size=20, center=True)


    def draw_ai_select(self):
        self.screen.fill(BG_COLOR)
        self.display_text("AI Algorithms", WIDTH//2, 80, size=45, center=True)

        descriptions = {
            "Minimax": "Maximize score / Minimize loss",
            "BFS": "Explore all states (optimal)",
            "A*": "Heuristic fast solution"
        }

        for name, rect in self.ai_buttons.items():
            color = HEADER_COLOR
            if rect.collidepoint(pygame.mouse.get_pos()):
                color = BUTTON_HOVER

            pygame.draw.rect(self.screen, color, rect, border_radius=12)
            pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=12)

            self.display_text(name, rect.centerx, rect.centery - 15, size=25, center=True)
            self.display_text(descriptions[name], rect.centerx, rect.centery + 15, size=16, color=YELLOW_DIM, center=True)


    def draw_board(self):
        self.screen.fill(BG_COLOR)
        pygame.draw.rect(self.screen, HEADER_COLOR, (0, 0, WIDTH, 150))
        self.display_text(f"Mode: {self.mode}", 20, 30, size=20, color=YELLOW_DIM)
        self.display_text(f"Level: {self.level}", WIDTH//2, 50, size=40, center=True)
        self.display_text(f"Score: {self.score}", WIDTH//2, 100, size=25, center=True)

        for name, rect in self.buttons.items():
            color = {
                "red": RED_DIM,
                "green": GREEN_DIM,
                "blue": BLUE_DIM,
                "yellow": YELLOW_DIM
            }[name]

            pygame.draw.rect(self.screen, color, rect, border_radius=15)
            pygame.draw.rect(self.screen, WHITE, rect, 3, border_radius=15)

    def game_over_screen(self):
        self.screen.fill(BG_COLOR)
        self.display_text("GAME OVER!", WIDTH//2, HEIGHT//2 - 50, size=60, color=RED_DIM, center=True)
        self.display_text(f"Final Score: {self.score}", WIDTH//2, HEIGHT//2 + 20, size=30, center=True)
        pygame.display.flip()

        self.speak("Game Over")

        time.sleep(2)
        self.state = "MENU"
        self.level = 0
        self.score = 0
        self.sequence = []


    def flash_button(self, name):
        original_color = {
            "red": RED_DIM, "green": GREEN_DIM,
            "blue": BLUE_DIM, "yellow": YELLOW_DIM
        }[name]

        flash_color = tuple(min(c + 100, 255) for c in original_color)

        pygame.draw.rect(self.screen, flash_color, self.buttons[name], border_radius=15)
        pygame.display.update()
        pygame.time.delay(350)

        self.draw_board()
        pygame.display.update()

        if self.mode == "Mixed Mode":
            self.speak(name)



    def bfs_play(self):
        from collections import deque
        queue = deque([(0, [])])

        while queue:
            index, path = queue.popleft()

            if index == len(self.sequence):
                for move in path:
                    self.flash_button(move)
                    time.sleep(0.4)
                return

            next_move = self.sequence[index]
            queue.append((index + 1, path + [next_move]))

    def astar_play(self):
        import heapq
        heap = []
        heapq.heappush(heap, (0, 0, []))

        while heap:
            cost, index, path = heapq.heappop(heap)

            if index == len(self.sequence):
                for move in path:
                    self.flash_button(move)
                    time.sleep(0.2)
                return

            next_move = self.sequence[index]
            heuristic = len(self.sequence) - index
            new_cost = cost + 1 + heuristic

            heapq.heappush(heap, (new_cost, index + 1, path + [next_move]))

    def minimax_play(self):
        def minimax(index):
            if index == len(self.sequence):
                return 1, []

            move = self.sequence[index]
            score, path = minimax(index + 1)
            return score + 1, [move] + path

        score, best_path = minimax(0)

        for move in best_path:
            self.flash_button(move)
            time.sleep(0.4)

    def ai_play(self):
        if self.ai_algorithm == "BFS":
            self.bfs_play()
        elif self.ai_algorithm == "A*":
            self.astar_play()
        elif self.ai_algorithm == "Minimax":
            self.minimax_play()

        self.score += 10
        self.ai_turn_done = True
        self.waiting_for_input = False


    def next_level(self):
        self.level += 1
        self.player_sequence = []
        self.sequence.append(random.choice(["red", "green", "blue", "yellow"]))

        time.sleep(1)

        if self.mode in ["Audio Mode", "Mixed Mode"]:
            seq = " ".join(self.sequence)
            self.speak(f"Level {self.level}. {seq}. Now your turn.")

        if self.mode != "Audio Mode":
            for move in self.sequence:
                self.flash_button(move)

        if self.mode == "Agent Mode (AI)":
            self.ai_play()
            return
        self.waiting_for_input = True




    def run(self):
        while self.running:

            if self.state == "MENU":
                self.draw_menu()

            elif self.state == "AI_SELECT":
                self.draw_ai_select()

            elif self.state == "PLAYING":
                if not self.waiting_for_input:
                    self.next_level()
                self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos

                    if self.state == "MENU":
                        for mode_name, rect in self.modes_buttons.items():
                            if rect.collidepoint(pos):
                                self.mode = mode_name
                                self.state = "AI_SELECT" if mode_name == "Agent Mode (AI)" else "PLAYING"

                    elif self.state == "AI_SELECT":
                        for name, rect in self.ai_buttons.items():
                            if rect.collidepoint(pos):
                                self.ai_algorithm = name
                                self.state = "PLAYING"

                    elif self.state == "PLAYING" and self.waiting_for_input:
                        for name, rect in self.buttons.items():
                            if rect.collidepoint(pos):
                                self.player_sequence.append(name)

                                if self.player_sequence[-1] != self.sequence[len(self.player_sequence)-1]:
                                    self.game_over_screen()
                                    break

                                if len(self.player_sequence) == len(self.sequence):
                                    self.score += 10
                                    self.waiting_for_input = False

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    NeuroPlay().run()                