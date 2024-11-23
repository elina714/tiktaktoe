import tkinter as tk
from tkinter import messagebox

# Tic Tac Toe Game
class TicTacToeGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Tic Tac Toe Game")
        self.board = [[' '] * 3  for _ in range(3)]
        self.buttons = [[None ]* 3 for _ in range(3)]
        self.player1 = "X"
        self.player2 = "O"
        self.current_player = self.player1
        self.game_mode = "Single Player"  # Default mode

        # Create title label
        title_label = tk.Label(
            window,
            text="Tic Tac Toe Game",
            font=("Arial", 25, "bold"),
            fg="darkgreen"
        )
        title_label.pack(pady=10)

        # Create grid frame
        self.grid_frame = tk.Frame(window)
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create buttons for the grid
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.grid_frame,
                    text="",
                    font=("Arial", 24),
                    bg="lightblue",
                    width=5,
                    height=2,
                    command=lambda r=i, c=j: self.make_move((r, c))
                )
                button.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                self.buttons[i][j] = button

        for i in range(3):
            self.grid_frame.rowconfigure(i, weight=1)
            self.grid_frame.columnconfigure(i, weight=1)

        # Add game mode selection buttons
        self.controls_frame = tk.Frame(window)
        self.controls_frame.pack(pady=10)
        single_player_button = tk.Button(
            self.controls_frame, text="Single Player",
            font=('Arial', 16),
            command=lambda: self.select_game_mode("Single Player")
        )
        single_player_button.pack(side="left", padx=5)

        multiplayer_button = tk.Button(
            self.controls_frame, text="Multiplayer",
            font=('Arial', 16),
            command=lambda: self.select_game_mode("Multiplayer")
        )
        multiplayer_button.pack(side="left", padx=5)

    def select_game_mode(self, mode):
        self.game_mode = mode
        self.reset_board()
        messagebox.showinfo("Game Mode", f"Game mode set to {mode}!")

    def make_move(self, position):
        row, col = position
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.update_board()

            # Check for a winner or a tie
            if self.check_winner(self.current_player):
                messagebox.showinfo(
                    "Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
                return
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_board()
                return

            # Switch player or let AI make a move
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            if self.current_player == self.player2 and self.game_mode == "Single Player":
                self.ai_make_move()

    def ai_make_move(self):
        best_move = self.find_best_move()
        if best_move:
            self.make_move(best_move)

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j])

    def check_winner(self, player):
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False

    def is_board_full(self):
        return all(all(cell != ' ' for cell in row) for row in self.board)

    def evaluate(self):
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                if self.board[i][0] == self.player1:
                    return 10
                elif self.board[i][0] == self.player2:
                    return -10
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                if self.board[0][i] == self.player1:
                    return 10
                elif self.board[0][i] == self.player2:
                    return -10
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == self.player1:
                return 10
            elif self.board[0][0] == self.player2:
                return -10
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == self.player1:
                return 10
            elif self.board[0][2] == self.player2:
                return -10
        return 0

    def minimax(self, depth, is_maximizing):
        score = self.evaluate()

        # Base cases
        if score == 10 or score == -10:
            return score
        if self.is_board_full():
            return 0

        if is_maximizing:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.player1
                        best = max(best, self.minimax(depth + 1, False))
                        self.board[i][j] = ' '  # Undo move
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.player2
                        best = min(best, self.minimax(depth + 1, True))
                        self.board[i][j] = ' '  # Undo move
            return best

    def find_best_move(self):
        best_val = float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.player2
                    move_val = self.minimax(0, True)
                    self.board[i][j] = ' '  # Undo move
                    if move_val < best_val:
                        best_val = move_val
                        best_move = (i, j)
        return best_move

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = self.player1
        self.update_board()


# Main application loop
window = tk.Tk()
game = TicTacToeGame(window)
window.mainloop()
