import random
import tkinter as tk
from tkinter import messagebox, font
from functools import partial
from copy import deepcopy
import json
import os
from datetime import datetime

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe Deluxe")
        self.window.geometry("500x650")
        self.window.resizable(False, False)
        self.window.config(bg="#2C3E50")
        
        # Set custom font and colors
        self.header_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12)
        self.game_font = font.Font(family="Helvetica", size=14, weight="bold")
        
        # Colors
        self.primary_color = "#3498DB"  # Blue
        self.secondary_color = "#2ECC71"  # Green
        self.accent_color = "#E74C3C"  # Red
        self.text_color = "#ECF0F1"  # White
        self.bg_color = "#2C3E50"  # Dark Blue
        
        # Game variables
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.player_score = {"X": 0, "O": 0, "Ties": 0}
        self.difficulty = "Medium"  # Default difficulty
        self.game_mode = "single"  # Default game mode
        self.player_names = {"X": "Player 1", "O": "Player 2/CPU"}
        self.game_buttons = []
        self.game_active = False
        self.moves_history = []
        
        # Create stats file if doesn't exist
        self.stats_file = "tictactoe_stats.json"
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, "w") as f:
                json.dump({"games_played": 0, "player_wins": 0, "cpu_wins": 0, "ties": 0}, f)
        
        self.show_main_menu()
        
    def create_button(self, parent, text, font, bg, fg, width, height=None, command=None, **kwargs):
        """Create standardized buttons for consistent UI"""
        # Remove the hardcoded activebackground
        button = tk.Button(
            parent,
            text=text,
            font=font,
            bg=bg,
            fg=fg,
            width=width,
            command=command,
            **kwargs
        )
        if height:
            button.config(height=height)
        return button

    def create_label(self, parent, text, font, bg, fg, pady=5, **kwargs):
        """Create standardized labels for consistent UI"""
        return tk.Label(
            parent,
            text=text,
            font=font,
            bg=bg,
            fg=fg,
            pady=pady,
            **kwargs
        )

    def show_main_menu(self):
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
            
        # Header
        header = self.create_label(
            self.window, 
            text="TIC-TAC-TOE DELUXE",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            pady=20
        )
        header.pack(fill=tk.X)
        
        # Menu frame
        menu_frame = tk.Frame(self.window, bg=self.bg_color, pady=20)
        menu_frame.pack()
        
        # Game mode buttons
        mode_label = self.create_label(
            menu_frame,
            text="SELECT GAME MODE",
            font=self.header_font,
            bg=self.bg_color,
            fg=self.text_color,
            pady=10
        )
        mode_label.pack()
        
        single_player_btn = self.create_button(
            menu_frame,
            text="Single Player",
            font=self.button_font,
            bg=self.primary_color,
            fg=self.text_color,
            width=20,
            height=2,
            command=self.setup_single_player
        )
        single_player_btn.pack(pady=10)
        
        multi_player_btn = self.create_button(
            menu_frame,
            text="Multi Player",
            font=self.button_font,
            bg=self.primary_color,
            fg=self.text_color,
            width=20,
            height=2,
            command=self.setup_multi_player
        )
        multi_player_btn.pack(pady=10)
        
        stats_btn = self.create_button(
            menu_frame,
            text="Game Statistics",
            font=self.button_font,
            bg=self.primary_color,
            fg=self.text_color,
            width=20,
            height=2,
            command=self.show_statistics
        )
        stats_btn.pack(pady=10)
        
        exit_btn = self.create_button(
            menu_frame,
            text="Exit Game",
            font=self.button_font,
            bg=self.accent_color,
            fg=self.text_color,
            width=20,
            height=2,
            activebackground="#C0392B",
            command=self.window.quit
        )
        exit_btn.pack(pady=10)
        
        # Version
        version_label = self.create_label(
            self.window,
            text="v2.0",
            font=("Helvetica", 8),
            bg=self.bg_color,
            fg=self.text_color,
            pady=10
        )
        version_label.pack(side=tk.BOTTOM)
    
    def setup_single_player(self):
        self.game_mode = "single"
        self.setup_difficulty_screen()
    
    def setup_difficulty_screen(self):
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
            
        header = self.create_label(
            self.window, 
            text="SELECT DIFFICULTY",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            pady=20
        )
        header.pack(fill=tk.X)
        
        diff_frame = tk.Frame(self.window, bg=self.bg_color, pady=20)
        diff_frame.pack()
        
        easy_btn = self.create_button(
            diff_frame,
            text="Easy",
            font=self.button_font,
            bg=self.secondary_color,
            fg=self.text_color,
            width=20,
            height=2,
            command=lambda: self.set_difficulty("Easy")
        )
        easy_btn.pack(pady=10)
        
        medium_btn = self.create_button(
            diff_frame,
            text="Medium",
            font=self.button_font,
            bg=self.secondary_color,
            fg=self.text_color,
            width=20,
            height=2,
            command=lambda: self.set_difficulty("Medium")
        )
        medium_btn.pack(pady=10)
        
        hard_btn = self.create_button(
            diff_frame,
            text="Hard",
            font=self.button_font,
            bg=self.secondary_color,
            fg=self.text_color,
            width=20,
            height=2,
            command=lambda: self.set_difficulty("Hard")
        )
        hard_btn.pack(pady=10)
        
        back_btn = self.create_button(
            diff_frame,
            text="Back",
            font=self.button_font,
            bg=self.accent_color,
            fg=self.text_color,
            width=20,
            height=2,
            activebackground="#C0392B",
            command=self.show_main_menu
        )
        back_btn.pack(pady=30)
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.setup_player_names()
    
    def setup_multi_player(self):
        self.game_mode = "multi"
        self.setup_player_names()
    
    def setup_player_names(self):
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
            
        header = self.create_label(
            self.window, 
            text="PLAYER NAMES",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            pady=20
        )
        header.pack(fill=tk.X)
        
        name_frame = tk.Frame(self.window, bg=self.bg_color, pady=20)
        name_frame.pack()
        
        # Player 1 name
        p1_label = self.create_label(
            name_frame,
            text="Player 1 (X):",
            font=self.button_font,
            bg=self.bg_color,
            fg=self.text_color,
            pady=5
        )
        p1_label.pack()
        
        p1_entry = tk.Entry(
            name_frame,
            font=self.button_font,
            width=20,
            justify='center'
        )
        p1_entry.insert(0, "Player 1")
        p1_entry.pack(pady=5)
        
        # Player 2 / CPU name
        p2_text = "Player 2 (O):" if self.game_mode == "multi" else "CPU (O):"
        p2_label = self.create_label(
            name_frame,
            text=p2_text,
            font=self.button_font,
            bg=self.bg_color,
            fg=self.text_color,
            pady=5
        )
        p2_label.pack()
        
        p2_entry = tk.Entry(
            name_frame,
            font=self.button_font,
            width=20,
            justify='center'
        )
        p2_default = "Player 2" if self.game_mode == "multi" else f"CPU ({self.difficulty})"
        p2_entry.insert(0, p2_default)
        p2_entry.pack(pady=5)
        
        if self.game_mode == "single":
            p2_entry.config(state=tk.DISABLED)
        
        # Start game button
        start_btn = self.create_button(
            name_frame,
            text="Start Game",
            font=self.button_font,
            bg=self.primary_color,
            fg=self.text_color,
            width=20,
            height=2,
            command=lambda: self.start_game(p1_entry.get(), p2_entry.get())
        )
        start_btn.pack(pady=30)
        
        back_btn = self.create_button(
            name_frame,
            text="Back",
            font=self.button_font,
            bg=self.accent_color,
            fg=self.text_color,
            width=20,
            height=2,
            activebackground="#C0392B",
            command=self.show_main_menu
        )
        back_btn.pack(pady=10)
    
    def start_game(self, p1_name, p2_name):
        self.player_names["X"] = p1_name if p1_name.strip() else "Player 1"
        self.player_names["O"] = p2_name if p2_name.strip() else ("Player 2" if self.game_mode == "multi" else f"CPU ({self.difficulty})")
        
        # Reset game state
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_active = True
        self.moves_history = []
        
        self.create_game_board()
    
    def create_game_board(self):
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
            
        # Score header
        score_frame = tk.Frame(self.window, bg=self.bg_color, pady=10)
        score_frame.pack(fill=tk.X)
        
        # Player X info
        px_frame = tk.Frame(score_frame, bg=self.bg_color)
        px_frame.pack(side=tk.LEFT, expand=True)
        
        px_name = self.create_label(
            px_frame,
            text=self.player_names["X"],
            font=self.header_font,
            bg=self.bg_color,
            fg=self.primary_color,
            pady=5
        )
        px_name.pack()
        
        px_score = self.create_label(
            px_frame,
            text=f"Score: {self.player_score['X']}",
            font=self.button_font,
            bg=self.bg_color,
            fg=self.text_color,
            pady=5
        )
        px_score.pack()
        
        # Ties
        ties_frame = tk.Frame(score_frame, bg=self.bg_color)
        ties_frame.pack(side=tk.LEFT, expand=True)
        
        ties_label = self.create_label(
            ties_frame,
            text="Ties",
            font=self.header_font,
            bg=self.bg_color,
            fg="#F39C12",
            pady=5
        )
        ties_label.pack()
        
        ties_score = self.create_label(
            ties_frame,
            text=f"{self.player_score['Ties']}",
            font=self.button_font,
            bg=self.bg_color,
            fg=self.text_color,
            pady=5
        )
        ties_score.pack()
        
        # Player O info
        po_frame = tk.Frame(score_frame, bg=self.bg_color)
        po_frame.pack(side=tk.RIGHT, expand=True)
        
        po_name = self.create_label(
            po_frame,
            text=self.player_names["O"],
            font=self.header_font,
            bg=self.bg_color,
            fg=self.secondary_color,
            pady=5
        )
        po_name.pack()
        
        po_score = self.create_label(
            po_frame,
            text=f"Score: {self.player_score['O']}",
            font=self.button_font,
            bg=self.bg_color,
            fg=self.text_color,
            pady=5
        )
        po_score.pack()
        
        # Current turn indicator
        self.turn_indicator = self.create_label(
            self.window,
            text=f"Current Turn: {self.player_names[self.current_player]} ({self.current_player})",
            font=self.header_font,
            bg=self.bg_color,
            fg=self.primary_color if self.current_player == "X" else self.secondary_color,
            pady=10
        )
        self.turn_indicator.pack()
        
        # Game board
        board_frame = tk.Frame(self.window, bg=self.bg_color, pady=20)
        board_frame.pack()
        
        self.game_buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Helvetica", 24, "bold"),
                    width=4,
                    height=2,
                    bg="#34495E",
                    fg=self.text_color,
                    command=lambda r=i, c=j: self.make_move(r, c)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.game_buttons.append(row)
            
        # Control buttons
        control_frame = tk.Frame(self.window, bg=self.bg_color, pady=20)
        control_frame.pack()
        
        undo_btn = self.create_button(
            control_frame,
            text="Undo Move",
            font=self.button_font,
            bg="#9B59B6",
            fg=self.text_color,
            width=15,
            command=self.undo_move
        )
        undo_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = self.create_button(
            control_frame,
            text="Reset Board",
            font=self.button_font,
            bg="#E67E22",
            fg=self.text_color,
            width=15,
            command=self.reset_board
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        menu_btn = self.create_button(
            control_frame,
            text="Main Menu",
            font=self.button_font,
            bg=self.accent_color,
            fg=self.text_color,
            width=15,
            command=self.confirm_exit_game
        )
        menu_btn.pack(side=tk.LEFT, padx=5)
        
        # If single player and computer goes first
        if self.game_mode == "single" and self.current_player == "O":
            self.window.after(500, self.computer_move)
    
    def make_move(self, row, col):
        # Check if the cell is empty and the game is active
        if self.board[row][col] == " " and self.game_active:
            # Record move for undo feature
            self.moves_history.append((row, col, self.current_player))
            
            # Update board
            self.board[row][col] = self.current_player
            self.game_buttons[row][col].config(
                text=self.current_player,
                bg=self.primary_color if self.current_player == "X" else self.secondary_color,
                state=tk.DISABLED
            )
            
            # Check for win or tie
            if self.check_winner(self.current_player):
                self.end_game(f"{self.player_names[self.current_player]} wins!")
                self.player_score[self.current_player] += 1
                self.update_stats(self.current_player)
                return
            elif self.is_board_full():
                self.end_game("It's a tie!")
                self.player_score["Ties"] += 1
                self.update_stats("tie")
                return
            
            # Switch player
            self.current_player = "O" if self.current_player == "X" else "X"
            self.turn_indicator.config(
                text=f"Current Turn: {self.player_names[self.current_player]} ({self.current_player})",
                fg=self.primary_color if self.current_player == "X" else self.secondary_color
            )
            
            # If single player mode and it's computer's turn
            if self.game_mode == "single" and self.current_player == "O":
                self.window.after(500, self.computer_move)
    
    def computer_move(self):
        if not self.game_active:
            return
            
        if self.difficulty == "Easy":
            move = self.get_easy_move()
        elif self.difficulty == "Medium":
            if random.random() < 0.7:  # 70% chance of smart move
                move = self.get_smart_move()
            else:
                move = self.get_easy_move()
        else:  # Hard difficulty
            move = self.get_smart_move()
            
        if move:
            self.make_move(move[0], move[1])
    
    def get_easy_move(self):
        # Just make a random move
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    empty_cells.append((i, j))
        
        if empty_cells:
            return random.choice(empty_cells)
        return None
    
    def get_smart_move(self):
        # Try to win
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    if self.check_winner("O"):
                        self.board[i][j] = " "
                        return (i, j)
                    self.board[i][j] = " "
        
        # Block player's win
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "X"
                    if self.check_winner("X"):
                        self.board[i][j] = " "
                        return (i, j)
                    self.board[i][j] = " "
        
        # Try to take center
        if self.board[1][1] == " ":
            return (1, 1)
        
        # Take corners
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        empty_corners = [corner for corner in corners if self.board[corner[0]][corner[1]] == " "]
        if empty_corners:
            return random.choice(empty_corners)
        
        # Take edges
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        empty_edges = [edge for edge in edges if self.board[edge[0]][edge[1]] == " "]
        if empty_edges:
            return random.choice(empty_edges)
        
        return None
    
    def check_winner(self, player):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                return True
        
        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        
        return False
    
    def is_board_full(self):
        for row in self.board:
            if " " in row:
                return False
        return True
    
    def end_game(self, message):
        self.game_active = False
        self.turn_indicator.config(text=message, fg="#F39C12")
        
        # Highlight winning cells
        if "wins" in message:
            winner = "X" if "X" in message else "O"
            self.highlight_winning_cells(winner)
            
        # Create play again button
        play_again_btn = self.create_button(
            self.window,
            text="Play Again",
            font=self.button_font,
            bg=self.secondary_color,
            fg=self.text_color,
            width=15,
            height=2,
            command=self.reset_board
        )
        play_again_btn.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
    
    def highlight_winning_cells(self, player):
        # Rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                for j in range(3):
                    self.game_buttons[i][j].config(bg="#F1C40F")  # Yellow
                return
        
        # Columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                for j in range(3):
                    self.game_buttons[j][i].config(bg="#F1C40F")
                return
        
        # Diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            self.game_buttons[0][0].config(bg="#F1C40F")
            self.game_buttons[1][1].config(bg="#F1C40F")
            self.game_buttons[2][2].config(bg="#F1C40F")
            return
            
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            self.game_buttons[0][2].config(bg="#F1C40F")
            self.game_buttons[1][1].config(bg="#F1C40F")
            self.game_buttons[2][0].config(bg="#F1C40F")
            return
    
    def reset_board(self):
        # Clear board
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_active = True
        self.moves_history = []
        
        # Remove play again button if exists
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Play Again":
                widget.destroy()
        
        # Reset buttons
        for i in range(3):
            for j in range(3):
                self.game_buttons[i][j].config(
                    text="",
                    bg="#34495E",
                    state=tk.NORMAL
                )
        
        # Reset turn indicator
        self.turn_indicator.config(
            text=f"Current Turn: {self.player_names[self.current_player]} ({self.current_player})",
            fg=self.primary_color
        )
        
        # If computer goes first
        if self.game_mode == "single" and self.current_player == "O":
            self.window.after(500, self.computer_move)
    
    def undo_move(self):
        if not self.moves_history:
            return
            
        # If playing against computer, need to undo both moves
        if self.game_mode == "single":
            if len(self.moves_history) < 2:
                return
                
            # Undo computer's move
            row, col, player = self.moves_history.pop()
            self.board[row][col] = " "
            self.game_buttons[row][col].config(text="", bg="#34495E", state=tk.NORMAL)
        
        # Undo player's move
        row, col, player = self.moves_history.pop()
        self.board[row][col] = " "
        self.game_buttons[row][col].config(text="", bg="#34495E", state=tk.NORMAL)
        
        # Reset turn to the player who just undid their move
        self.current_player = player
        self.game_active = True
        
        # Update turn indicator
        self.turn_indicator.config(
            text=f"Current Turn: {self.player_names[self.current_player]} ({self.current_player})",
            fg=self.primary_color if self.current_player == "X" else self.secondary_color
        )
    
    def confirm_exit_game(self):
        if messagebox.askyesno("Exit Game", "Are you sure you want to return to the main menu?"):
            self.show_main_menu()
    
    def show_statistics(self):
        # Load stats from file
        try:
            with open(self.stats_file, "r") as f:
                stats = json.load(f)
        except:
            stats = {"games_played": 0, "player_wins": 0, "cpu_wins": 0, "ties": 0}
        
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
            
        header = self.create_label(
            self.window, 
            text="GAME STATISTICS",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            pady=20
        )
        header.pack(fill=tk.X)
        
        stats_frame = tk.Frame(self.window, bg=self.bg_color, pady=20)
        stats_frame.pack()
        
        # Display stats
        stats_text = f"""
        Games Played: {stats['games_played']}
        
        Player Wins: {stats['player_wins']} ({self.percentage(stats['player_wins'], stats['games_played'])}%)
        
        CPU Wins: {stats['cpu_wins']} ({self.percentage(stats['cpu_wins'], stats['games_played'])}%)
        
        Ties: {stats['ties']} ({self.percentage(stats['ties'], stats['games_played'])}%)
        """
        
        stats_label = self.create_label(
            stats_frame,
            text=stats_text,
            font=self.button_font,
            bg=self.bg_color,
            fg=self.text_color,
            justify=tk.LEFT,
            pady=10
        )
        stats_label.pack(pady=20)
        
        # Current session stats
        session_label = self.create_label(
            stats_frame,
            text="CURRENT SESSION",
            font=self.header_font,
            bg=self.bg_color,
            fg="#F39C12",
            pady=10
        )
        session_label.pack()
        
        session_text = f"""
        Player X ({self.player_names['X']}): {self.player_score['X']} wins
        
        Player O ({self.player_names['O']}): {self.player_score['O']} wins
        
        Ties: {self.player_score['Ties']}
        """
        
        session_stats = self.create_label(
            stats_frame,
            text=session_text,
            font=self.button_font,
            bg=self.bg_color,
            fg=self.text_color,
            justify=tk.LEFT,
            pady=10
        )
        session_stats.pack(pady=10)
        
        # Back button
        back_btn = self.create_button(
            stats_frame,
            text="Back to Menu",
            font=self.button_font,
            bg=self.primary_color,
            fg=self.text_color,
            width=20,
            height=2,
            command=self.show_main_menu
        )
        back_btn.pack(pady=20)
    
    def percentage(self, part, total):
        if total == 0:
            return 0
        return round((part / total) * 100, 1)
    
    def update_stats(self, winner):
        try:
            with open(self.stats_file, "r") as f:
                stats = json.load(f)
        except:
            stats = {"games_played": 0, "player_wins": 0, "cpu_wins": 0, "ties": 0}
        
        stats["games_played"] += 1
        
        if winner == "tie":
            stats["ties"] += 1
        elif winner == "X":
            stats["player_wins"] += 1
        elif winner == "O" and self.game_mode == "single":
            stats["cpu_wins"] += 1
        elif winner == "O" and self.game_mode == "multi":
            stats["player_wins"] += 1
            
        with open(self.stats_file, "w") as f:
            json.dump(stats, f)

if __name__ == "__main__":
    game = TicTacToe()
    game.window.mainloop()  # Add this line to start the Tkinter event loop