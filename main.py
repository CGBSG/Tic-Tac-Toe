from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
import random

Window.size = (300, 400)

class TicTacToe(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 4
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        
        # Title
        self.title = Label(text="Tic Tac Toe", font_size=30, color=(0, 0.5, 1, 1))
        self.add_widget(self.title)
        
        # Create board
        self.cells = []
        for _ in range(9):
            cell = Button(text='', font_size=40, background_normal='', 
                          background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
            cell.bind(on_press=self.player_move)
            self.cells.append(cell)
            self.add_widget(cell)
        
        # Reset Button
        self.reset_btn = Button(text='Reset Game', font_size=20, background_color=(0.8, 0, 0, 1))
        self.reset_btn.bind(on_press=self.reset_game)
        self.add_widget(self.reset_btn)

    def player_move(self, instance):
        if self.game_over or self.current_player == 'O':
            return
            
        index = self.cells.index(instance)
        if self.board[index] == '':
            instance.text = 'X'
            instance.background_color = (0.8, 0.8, 1, 1)
            self.board[index] = 'X'
            if self.check_winner('X'):
                self.show_winner('Player Wins!')
                return
            if self.check_tie():
                self.show_winner("It's a Tie!")
                return
            self.current_player = 'O'
            Clock.schedule_once(lambda dt: self.bot_move(), 0.5)

    def bot_move(self):
        if self.game_over:
            return
        
        # Simple AI with minimax
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                score = self.minimax(self.board, False)
                self.board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
        
        if best_move is not None:
            self.board[best_move] = 'O'
            self.cells[best_move].text = 'O'
            self.cells[best_move].background_color = (1, 0.8, 0.8, 1)
            if self.check_winner('O'):
                self.show_winner('Bot Wins!')
                return
            if self.check_tie():
                self.show_winner("It's a Tie!")
                return
            self.current_player = 'X'

    def minimax(self, board, is_maximizing):
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif self.check_tie():
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.minimax(board, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.minimax(board, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def check_tie(self):
        return '' not in self.board

    def show_winner(self, message):
        self.game_over = True
        popup = Popup(title='Game Over',
                     content=Label(text=message, font_size=24),
                     size_hint=(0.7, 0.4))
        popup.open()

    def reset_game(self, instance):
        self.game_over = False
        self.current_player = 'X'
        self.board = [''] * 9
        for cell in self.cells:
            cell.text = ''
            cell.background_color = (1, 1, 1, 1)

class TicTacToeApp(App):
    def build(self):
        return TicTacToe()

if __name__ == '__main__':
    TicTacToeApp().run()
