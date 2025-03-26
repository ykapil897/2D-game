from OpenGL.GL import *
from utils.window_manager import Window
from game import Game
import imgui
from imgui.integrations.glfw import GlfwRenderer
import json
import os

class App:
    def __init__(self, width, height):
        self.window = Window(height, width)
        self.game = Game(height, width)
        self.show_main_menu = True
        imgui.create_context()
        self.impl = GlfwRenderer(self.window.window)
        self.save_filename = "save_game.json"

    def RenderLoop(self):

        while self.window.IsOpen():
            inputs, time = self.window.StartFrame(0.0, 0.0, 0.0, 1.0)

            self.impl.process_inputs() 
            imgui.new_frame()

            # If not showing main menu, check game status
            if not self.show_main_menu:
                if self.game.is_game_over:
                    self.show_game_over_screen()
                elif self.game.is_game_won:
                    self.show_you_won_screen()
                else:
                    self.game.ProcessFrame(inputs, time)
                    # self.game.show_switch_map_button()
            else:
                self.show_main_menu_screen(inputs)

            imgui.render()
            self.impl.render(imgui.get_draw_data())
            self.window.EndFrame()

        # If the game is closed without Game Over or Victory, save current progress
        if not (self.game.is_game_over or self.game.is_game_won):
            self.save_current_game()
        
        self.window.Close()


    def save_current_game(self):
        data = {
            "map": self.game.current_map,
            "lives": self.game.lives,
            "health": self.game.health,
            "total_time": self.game.total_time,
        }
        with open(self.save_filename, "w") as f:
            json.dump(data, f)

    def show_you_won_screen(self):
        # Center the window
        center_x = (self.window.windowWidth - 550) / 2
        center_y = (self.window.windowHeight - 400) / 2
        imgui.set_next_window_position(center_x, center_y)
        imgui.set_next_window_size(600, 400)

        imgui.begin("Victory!", True)
        # Make the text larger
        imgui.set_window_font_scale(10.0)
        imgui.text_unformatted("YOU WON!")
        imgui.set_window_font_scale(5.0)  # slightly smaller for the next lines
        imgui.text_unformatted(f"Time taken: {int(self.game.total_time)}s")
        imgui.end()

    def show_game_over_screen(self):
        # Center the window
        center_x = (self.window.windowWidth - 850) / 2
        center_y = (self.window.windowHeight - 600) / 2
        imgui.set_next_window_position(center_x, center_y)
        imgui.set_next_window_size(850, 600)

        imgui.begin("Game Over", True)
        # Make the text larger
        imgui.set_window_font_scale(10.0)
        imgui.text_unformatted("GAME OVER")
        imgui.set_window_font_scale(5.0)
        imgui.text_unformatted("You lost all your lives!")
        if imgui.button("Return to Main Menu", 750, 100):
            self.show_main_menu = True
        imgui.end()
    
    def show_main_menu_screen(self, inputs):
        imgui.begin("Main Menu", True, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
    
        # Get window size and calculate the center position
        window_width = imgui.get_window_width()
        window_height = imgui.get_window_height()
        button_width = 200
        button_height = 50
        center_x = (window_width - button_width) / 2
        center_y = (window_height - button_height) / 2

        # Set window position to center of the screen
        # imgui.set_window_pos((self.window.windowWidth - window_width) / 2, (self.window.windowHeight - window_height) / 2)
        imgui.set_window_size(400, 300)

        # Center the "NEW GAME" button
        imgui.set_cursor_pos_x(center_x)
        imgui.set_cursor_pos_y(center_y - button_height)
        if imgui.button("NEW GAME", button_width, button_height):
            # print("Game started")
            self.start_new_game()

        # Center the "LOAD GAME" button
        imgui.set_cursor_pos_x(center_x)
        imgui.set_cursor_pos_y(center_y + button_height)
        if imgui.button("LOAD GAME", button_width, button_height):
            self.load_game()

        imgui.end()

    def start_new_game(self):
        self.show_main_menu = False
        self.game = Game(self.window.windowHeight, self.window.windowWidth)
        self.game.screen = 0
        self.game.InitScreen()

    def load_game(self):
        self.show_main_menu = False
        # Check if the save file exists
        if os.path.exists(self.save_filename):
            with open(self.save_filename, "r") as f:
                data = json.load(f)
                # Restore saved values
                self.game.screen = data["map"]
                self.game.lives = data["lives"]
                self.game.health = data["health"]
                self.game.total_time = data["total_time"]
            self.game.InitScreen()
        else:
            # If no save file, just start a new game or handle gracefully
            self.start_new_game()

if __name__ == "__main__":
    app = App(1000, 1000)
    app.RenderLoop()


