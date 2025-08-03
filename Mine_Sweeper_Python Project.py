import os
import tkinter as tk
from tkinter import messagebox
import random

class MineSweeper:
    def __init__(self, master, rows, cols, bombs):
        self.master = master
        self.master.title("Minesweeper")
        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        self.score = 0
        self.moves = 0
        self.game_over = False
        self.first_click = True  
        self.high_score_file = "high_score.txt"  
        self.high_scores = self.load_high_scores()
 
        self.create_widgets()
        self.create_board()


    def load_high_scores(self):
        high_scores = []
        if os.path.exists(self.high_score_file):
            with open(self.high_score_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    name, score = line.strip().split(",")
                    high_scores.append((name, int(score)))
        return high_scores

    def save_high_scores(self):
        with open(self.high_score_file, "w") as file:
            for name, score in self.high_scores:
                file.write(f"{name},{score}\n")

    def update_high_score(self):
        if not self.high_scores:
            self.high_scores = [("Previous", 0)]

        highest_score = max(self.high_scores, key=lambda x: x[1])[1]
        if self.score > highest_score:
            player_name = self.ADD_Name()
            self.high_scores.append((player_name, self.score))
            self.high_scores.sort(key=lambda x: x[1], reverse=True)
            self.high_scores = self.high_scores[:5]
            self.save_high_scores()

    def ADD_Name(self):
        player_name = input("Congratulations! You achieved a high score! Enter your name: ")
        return player_name


    def display_high_score(self):
        if self.high_scores:
            high_scores_text = ""
            for name, score in self.high_scores:
                high_scores_text += f"{name}: {score}\n"
            messagebox.showinfo("High Scores", f"Highest Scores:\n{high_scores_text}")
        else:
            messagebox.showinfo("High Scores", "No high scores yet.")


    def create_widgets(self):
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(
                    self.master,
                    text="",
                    width=2,
                    height=1,
                    font=("Arial", 15, "bold"),
                    bg="#AAD751",
                    command=lambda r=row, c=col, b=1: self.click(r, c, b),
                )
                button.bind("<Button-3>", lambda event, r=row, c=col, b=3: self.click(r, c, b))
                button.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[row][col] = button

        self.score_label = tk.Label(
            self.master,
            text="Score: 0",
            font=("Arial", 12),
            bg="#E0E0E0"
        )
        self.score_label.grid(row=self.rows + 1, columnspan=self.cols, pady=5)

        self.try_again_button = tk.Button(
            self.master,
            text="Try Again",
            command=self.try_again,
            state=tk.DISABLED,
            font=("Arial", 15, "bold"),
            bg="gray",
            fg="white",
        )
        self.try_again_button.grid(row=self.rows, columnspan=self.cols, pady=10)

        self.high_score_button = tk.Button(
            self.master,
            text="High Score",
            command=self.display_high_score,
            font=("Arial", 15, "bold"),
            bg="#4CAF50",
            fg="white",
        )
        self.high_score_button.grid(row=self.rows + 2, columnspan=self.cols, pady=10)

    def create_board(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def plant_bombs(self, first_click_row, first_click_col):
        bomb_positions = random.sample(range(self.rows * self.cols), self.bombs)
        while first_click_row * self.cols + first_click_col in bomb_positions:
            bomb_positions = random.sample(range(self.rows * self.cols), self.bombs)

        for position in bomb_positions:
            row = position // self.cols
            col = position % self.cols
            self.board[row][col] = -1

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1:
                    bomb_count = 0

                    for i in range(max(0, row - 1), min(row + 2, self.rows)):
                        for j in range(max(0, col - 1), min(col + 2, self.cols)):
                            if self.board[i][j] == -1:
                                bomb_count += 1

                    self.board[row][col] = bomb_count

    def click(self, row, col, button):
        if self.game_over:
            return

        self.moves += 1

        if self.first_click: 
            self.plant_bombs(row, col)
            self.first_click = False

        if button == 1:
            if self.board[row][col] == -1:
                self.game_over = True
                self.reveal_board()
                messagebox.showinfo("Game Over", f"You hit a bomb! Game over. Your final score: {self.calculate_score('loss')}")
                self.try_again_button["state"] = tk.NORMAL
            else:
                self.reveal(row, col)
                self.update_score(10)
                if self.check_win():
                    self.game_over = True
                    self.try_again_button["state"] = tk.NORMAL
                    messagebox.showinfo("You Win!", f"Congratulations! You successfully cleared the board. Your final score: {self.calculate_score('win')}")
        elif button == 3:
            if self.buttons[row][col]["text"] == "":
                self.buttons[row][col]["text"] = "🚩"
            else:
                self.buttons[row][col]["text"] = ""

    def reveal(self, row, col):
        button = self.buttons[row][col]

        if button["text"] != "" or button["state"] == tk.DISABLED:
            return

        value = self.board[row][col]
        if value > 0:
            button["text"] = str(value)
            button["bg"] = "#D2B48C" 
        else:
            button["bg"] = "#D2B48C" 
            button["text"] = ""

        button["state"] = tk.DISABLED
        button["relief"] = tk.SUNKEN

        if value == 0:
            for i in range(max(0, row - 1), min(row + 2, self.rows)):
                for j in range(max(0, col - 1), min(col + 2, self.cols)):
                    self.reveal(i, j)

    def reveal_board(self):
        for row in self.buttons:
            for button in row:
                button["state"] = tk.DISABLED
                if self.board[self.buttons.index(row)][row.index(button)] == -1:
                    button["text"] = "💣"
                    button["font"] = ("Arial", 15, "bold")
                    button["bg"] = "red"
                    button["fg"] = "white"
                else:
                    button["relief"] = tk.SUNKEN

    def update_score(self, points):
        self.score += points
        self.score_label["text"] = f"Score: {self.score}"

    def calculate_score(self, game_result):
        if game_result == "loss":
            self.score = max(0, self.score // 2) 
        elif game_result == "win":
            self.score += 50  
        self.update_high_score()  
        return self.score

    def try_again(self):
        self.game_over =  False
        self.try_again_button["state"] = tk.DISABLED
        self.score = 0
        self.moves = 0
        self.score_label["text"] = "Score: 0"
        self.first_click = True

        for row in self.buttons:
            for button in row:
                button["text"] = ""
                button["state"] = tk.NORMAL
                button["relief"] = tk.RAISED
                button["bg"] = "#AAD751"
                button["fg"] = "black"

        self.create_board()

    def check_win(self):
        for row in self.buttons:
            for button in row:
                if button["state"] == tk.NORMAL and self.board[self.buttons.index(row)][row.index(button)] != -1:
                    return False
        return True

def set_difficulty():
    try:
        print("Choose difficulty level...")
        print("1. Easy(5 bombs)\n2. Normal(18 bombs)\n3. Hard(30 bombs)")
        difficulty = int(input("Your Choice of Difficulty: "))
        bombs = 0

        if difficulty == 1:
            bombs = 5
            rows = 5
            cols = 5
        elif difficulty == 2:
            bombs = 18
            rows = 8
            cols = 8
        elif difficulty == 3:
            bombs = 30
            rows = 10
            cols = 10
        else:
            print("Please choose correct difficulty")
            return set_difficulty()
        
        return rows, cols, bombs
    except ValueError:
        print("Invalid input. Please enter valid integers.\n\n")
        return set_difficulty()

def main():
    rows, cols, bombs = set_difficulty()

    game = tk.Tk()
    game.configure(bg="#E0E0E0")

    minesweeper_game = MineSweeper(game, rows, cols, bombs)
    game.mainloop()

if __name__ == "__main__":
    main()
