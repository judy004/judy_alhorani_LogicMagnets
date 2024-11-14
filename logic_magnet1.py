from copy import deepcopy
import tkinter as tk
from tkinter import messagebox
from queue import Queue

class State:
    def __init__(self, board_size, init_board):
        self.board_size = board_size
        self.board = init_board
        self.original_board = [['E' if cell == 'G' else cell for cell in row] for row in init_board]
        self.purple_magnet_pre_value = 'E'
        self.red_magnet_pre_value = 'E'
        self.directions = ['up', 'down', 'left', 'right']
        self.stack = []
        self.queue = Queue()
        self.stack.append(init_board)
        self.queue.put(init_board)
        self.current_board = deepcopy(init_board)

    def valid_move(self, current_row, current_col, next_row, next_col):
        if next_row < 0 or next_row >= self.board_size or next_col < 0 or next_col >= self.board_size:
            return False
        return self.board[next_row][next_col] in ['E', '*']

    def repulsion(self, current_row, current_col, next_row, next_col):
        if not self.valid_move(current_row, current_col, next_row, next_col):
            return False
        self.board[current_row][current_col] = self.purple_magnet_pre_value
        self.purple_magnet_pre_value = self.original_board[next_row][next_col] if self.purple_magnet_pre_value == 'E' else self.board[next_row][next_col]
        self.board[next_row][next_col] = 'P'
        # Repulsion effect logic
        for i in range(self.board_size):
            if self.board[next_row][i] == 'G':
                if i < next_col and self.valid_move(next_row, i, next_row, i-1):
                    self.board[next_row][i-1] = 'G'
                    self.board[next_row][i] = self.original_board[next_row][i]
                elif i > next_col and self.valid_move(next_row, i, next_row, i+1):
                    self.board[next_row][i+1] = 'G'
                    self.board[next_row][i] = self.original_board[next_row][i]
            if self.board[i][next_col] == 'G':
                if i < next_row and self.valid_move(i, next_col, i-1, next_col):
                    self.board[i-1][next_col] = 'G'
                    self.board[i][next_col] = self.original_board[i][next_col]
                elif i > next_row and self.valid_move(i, next_col, i+1, next_col):
                    self.board[i+1][next_col] = 'G'
                    self.board[i][next_col] = self.original_board[i][next_col]
        return True

    def attraction(self, current_row, current_col, next_row, next_col):
        if not self.valid_move(current_row, current_col, next_row, next_col):
            return False
        self.board[current_row][current_col] = self.red_magnet_pre_value
        self.red_magnet_pre_value = self.original_board[next_row][next_col] if self.red_magnet_pre_value == 'E' else self.board[next_row][next_col]
        self.board[next_row][next_col] = 'R'
        # Attraction effect logic
        for i in range(self.board_size):
            if self.board[next_row][i] == 'G':
                if i < next_col and self.valid_move(next_row, i, next_row, i+1):
                    self.board[next_row][i+1] = 'G'
                    self.board[next_row][i] = self.original_board[next_row][i]
                elif i > next_col and self.valid_move(next_row, i, next_row, i-1):
                    self.board[next_row][i-1] = 'G'
                    self.board[next_row][i] = self.original_board[next_row][i]
            if self.board[i][next_col] == 'G':
                if i < next_row and self.valid_move(i, next_col, i+1, next_col):
                    self.board[i+1][next_col] = 'G'
                    self.board[i][next_col] = self.original_board[i][next_col]
                elif i > next_row and self.valid_move(i, next_col, i-1, next_col):
                    self.board[i-1][next_col] = 'G'
                    self.board[i][next_col] = self.original_board[i][next_col]
        return True

    def winning_state(self):
        for row in self.board:
            if '*' in row:
                return False
        return True

    def get_possible_moves(self):
        moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] in ('P', 'R'):
                    for direction in self.directions:
                        dr, dc = 0, 0
                        if direction == 'up': dr = -1
                        elif direction == 'down': dr = 1
                        elif direction == 'left': dc = -1
                        elif direction == 'right': dc = 1
                        next_row, next_col = row + dr, col + dc
                        if self.valid_move(row, col, next_row, next_col) and self.board[next_row][next_col] != 'G':
                            moves.append((row, col, next_row, next_col, self.board[row][col]))
        return moves

def dfs(state, visited):
    while state.stack:
        current_board = state.stack.pop()
        state.board = current_board
        if state.winning_state():
            return True, state.board
        board_tuple = tuple(tuple(row) for row in state.board)
        visited.add(board_tuple)
        for move in state.get_possible_moves():
            next_state = State(state.board_size, [row[:] for row in state.board])
            if move[4] == 'P':
                success = next_state.repulsion(*move[:4])
            else:
                success = next_state.attraction(*move[:4])

            if success:
                board_tuple = tuple(tuple(row) for row in next_state.board)
                if board_tuple not in visited:
                    state.stack.append(next_state.board)
    return False, None

def bfs(state, visited):
    while not state.queue.empty():
        current_board = state.queue.get()
        state.board = current_board
        if state.winning_state():
            return True, state.board
        board_tuple = tuple(tuple(row) for row in state.board)
        visited.add(board_tuple)
        for move in state.get_possible_moves():
            next_state = State(state.board_size, [row[:] for row in state.board])
            if move[4] == 'P':
                success = next_state.repulsion(*move[:4])
            else:
                success = next_state.attraction(*move[:4])

            if success:
                board_tuple = tuple(tuple(row) for row in next_state.board)
                if board_tuple not in visited:
                    state.queue.put(next_state.board)
    return False, None

def solve_game(board_size, init_board, method):
    state = State(board_size, init_board)
    visited = set()
    if method == 'dfs':
        success, solution = dfs(state, visited)
    else:
        success, solution = bfs(state, visited)
    return solution if success else None

def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

def create_game_board(board_size, initial_board):
    root = tk.Tk()
    root.title("Magnet Game")

    cell_size = 50
    canvas = tk.Canvas(root, width=board_size * cell_size, height=board_size * cell_size)
    canvas.pack()

    for row in range(board_size):
        for col in range(board_size):
            cell_color = "white"
            if initial_board[row][col] == 'E':
                cell_color = "white"
            elif initial_board[row][col] == '*':
                cell_color = "gray"
            elif initial_board[row][col] == 'P':
                cell_color = "purple"
            elif initial_board[row][col] == 'R':
                cell_color = "red"
            elif initial_board[row][col] == 'G':
                cell_color = "green"
            canvas.create_rectangle(col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size, fill=cell_color)

    def solve_button_click(method):
        print("Initial Board:")
        print_board(initial_board)

        solution = solve_game(board_size, initial_board, method)
        if solution is None:
            messagebox.showinfo("No Solution", "There is no solution to this game.")
        else:
            print("Solution:")
            print_board(solution)

            for row in range(board_size):
                for col in range(board_size):
                    cell_color = "white"
                    if solution[row][col] == 'E':
                        cell_color = "white"
                    elif solution[row][col] == '*':
                        cell_color = "gray"
                    elif solution[row][col] == 'P':
                        cell_color = "purple"
                    elif solution[row][col] == 'R':
                        cell_color = "red"
                    elif solution[row][col] == 'G':
                        cell_color = "green"
                    canvas.create_rectangle(col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size, fill=cell_color)

    dfs_button = tk.Button(root, text="Solve with DFS", command=lambda: solve_button_click('dfs'))
    bfs_button = tk.Button(root, text="Solve with BFS", command=lambda: solve_button_click('bfs'))
    dfs_button.pack()
    bfs_button.pack()

    root.mainloop()

initial_board = [
     ['E', 'E', '*', 'E', 'E'],
    ['E', 'E', 'G', 'E', 'E'],
    ['*', 'G', '*', 'G', '*'],
    ['E', 'E', 'G', 'E', 'E'],
    ['P', 'E', '*', 'E', 'E']
]
create_game_board(5, initial_board)
