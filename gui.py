from logic_magnet1 import State
import tkinter as tk
from tkinter import messagebox

class LogicMagnetsGameGUI:
    def __init__(self,root,state):
        self.root = root
        self.state = state
        self.grid_buttons = []
        self.selected_piece = None

        self.root.title("Logic Magnets")
        self.create_grid()
        self.update_grid()

    def create_grid(self):
        for row in range(self.state.board_size):
            button_row = []
            for col in range(self.state.board_size):
                button = tk.Button(self.root, width=6, height=4, command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.grid_buttons.append(button_row)

    def on_button_click(self, row, col):
        piece = self.state.board[row][col]

        if self.selected_piece is None:
            if piece in ('P', 'R'):
                self.selected_piece = (row, col)
                self.grid_buttons[row][col].config(bg="gray")
            else:
                messagebox.showinfo("Invalid Selection","Select a purple or red magnet to move.")
        else:
            prev_row, prev_col = self.selected_piece
            if self.state.board[prev_row][prev_col] == 'P':
                moved = self.state.repulsion(prev_row, prev_col, row, col)
            elif self.state.board[prev_row][prev_col] == 'R':
                moved = self.state.attraction(prev_row, prev_col, row, col)
            
            if moved:
                self.update_grid()
                if self.state.wining_state():
                    messagebox.showinfo("Congratulations","Game Over! You won!")
                    self.root.quit()
            else:
                messagebox.showinfo("Invalid Move","This move is not valid.")
            self.grid_buttons[prev_row][prev_col].config(bg="SystemButtonFace")
            self.selected_piece = None

    def update_grid(self):
        for row in range(self.state.board_size):
            for col in range(self.state.board_size):
                cell_value = self.state.board[row][col]
                button = self.grid_buttons[row][col]
                button.config(text=cell_value)

                if cell_value == 'P':
                    button.config(bg="purple", fg="purple")
                elif cell_value == 'R':
                    button.config(bg="red", fg="red")
                elif cell_value == 'G':
                    button.config(bg="black", fg="black")
                elif cell_value == '*':
                    button.config(bg="white", fg="white")
                else:
                    button.config(bg="light blue", fg="light blue")

board_size = 5
# #Red
# init_board = [
#     ['E', 'E', 'E', 'G'],
#     ['*', 'E', '*', 'E'],
#     ['G', '*', '*', 'E'],
#     ['G', 'E', 'E', 'R'],
# ]


#purple
# init_board=[
#     ['E', 'E', '*', 'E', 'E'],
#     ['E', 'E', 'G', 'E', 'E'],
#     ['*', 'G', '*', 'G', '*'],
#     ['E', 'E', 'G', 'E', 'E'],
#     ['P', 'E', '*', 'E', 'E']
# ]


#Red and purple
init_board=[
    ['*', 'G', '*', 'G', 'E'],
    ['E', 'E', 'P', 'E', '*'],
    ['E', 'E', 'R', 'E', '*'],
    ['E', 'E', 'E', 'E', 'E'],
    ['E', 'E', 'E', 'E', 'E']
]


# init_board=[
#     ['*', 'E', '*', 'G', 'E'],
#     ['E', 'E', 'P', 'E', '*'],
#     ['E', 'E', 'R', 'E', '*'],
#     ['E', 'G', 'E', 'E', 'E'],
#     ['E', 'G', 'E', 'E', 'E']
# ]


state = State(board_size,init_board)

# Create and run the GUI
root = tk.Tk()
game_gui = LogicMagnetsGameGUI(root, state)
root.mainloop()
