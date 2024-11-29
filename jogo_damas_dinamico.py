import tkinter as tk

class CheckersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Damas")
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.turn_label = tk.Label(root, text="Vez do jogador: Branco")
        self.turn_label.pack()
        self.board = self.create_board()
        self.selected_piece = None
        self.turn = "white"
        self.possible_moves = []
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def create_board(self):
        board = []
        for row in range(8):
            board_row = []
            for col in range(8):
                if (row + col) % 2 == 0:
                    board_row.append(None)
                else:
                    if row < 3:
                        board_row.append("black")
                    elif row > 4:
                        board_row.append("white")
                    else:
                        board_row.append(None)
            board.append(board_row)
        return board

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                if (row, col) in self.possible_moves:
                    color = "lightgreen"
                self.canvas.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color)
                piece = self.board[row][col]
                if piece:
                    self.draw_piece(row, col, piece)

    def draw_piece(self, row, col, piece):
        x0, y0 = col * 50 + 10, row * 50 + 10
        x1, y1 = col * 50 + 40, row * 50 + 40
        color = "black" if piece == "black" else "white"
        self.canvas.create_oval(x0, y0, x1, y1, fill=color)
        if piece.endswith("Q"):
            self.canvas.create_text((col * 50 + 25, row * 50 + 25), text="Q", fill="red")

    def on_click(self, event):
        col, row = event.x // 50, event.y // 50
        if self.selected_piece:
            if (row, col) in self.possible_moves:
                self.move_piece(self.selected_piece, (row, col))
                self.selected_piece = None
                self.possible_moves = []
            else:
                self.selected_piece = None
                self.possible_moves = []
        else:
            if self.board[row][col] and self.board[row][col].startswith(self.turn):
                self.selected_piece = (row, col)
                self.possible_moves = self.get_possible_moves(row, col)
        self.draw_board()

    def move_piece(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        if self.is_valid_move(from_pos, to_pos):
            self.board[to_row][to_col] = self.board[from_row][from_col]
            self.board[from_row][from_col] = None
            if abs(from_row - to_row) == 2:
                mid_row, mid_col = (from_row + to_row) // 2, (from_col + to_col) // 2
                self.board[mid_row][mid_col] = None
                # Verifica se há capturas adicionais possíveis
                self.selected_piece = (to_row, to_col)
                self.possible_moves = self.get_possible_moves(to_row, to_col)
                if self.possible_moves:
                    self.draw_board()
                    return
            if (to_row == 0 and self.board[to_row][to_col] == "white") or (to_row == 7 and self.board[to_row][to_col] == "black"):
                self.board[to_row][to_col] += "Q"
            self.turn = "black" if self.turn == "white" else "white"
            self.turn_label.config(text=f"Vez do jogador: {'Branco' if self.turn == 'white' else 'Preto'}")
            self.draw_board()

    def is_valid_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        if self.board[to_row][to_col] is not None:
            return False
        piece = self.board[from_row][from_col]
        if piece.endswith("Q"):
            return self.is_valid_queen_move(from_pos, to_pos)
        if piece.startswith("white") and to_row >= from_row:
            return False
        if piece.startswith("black") and to_row <= from_row:
            return False
        if abs(from_row - to_row) == 1 and abs(from_col - to_col) == 1:
            return True
        if abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            mid_row, mid_col = (from_row + to_row) // 2, (from_col + to_col) // 2
            if self.board[mid_row][mid_col] and self.board[mid_row][mid_col].startswith("black" if piece.startswith("white") else "white"):
                return True
        return False

    def is_valid_queen_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
        step_row = 1 if to_row > from_row else -1
        step_col = 1 if to_col > from_col else -1
        row, col = from_row + step_row, from_col + step_col
        while row != to_row and col != to_col:
            if self.board[row][col] is not None:
                return False
            row += step_row
            col += step_col
        return True

    def get_possible_moves(self, row, col):
        piece = self.board[row][col]
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8 and self.is_valid_move((row, col), (new_row, new_col)):
                moves.append((new_row, new_col))
            new_row, new_col = row + 2 * dr, col + 2 * dc
            if 0 <= new_row < 8 and 0 <= new_col < 8 and self.is_valid_move((row, col), (new_row, new_col)):
                moves.append((new_row, new_col))
        return moves

def main():
    root = tk.Tk()
    game = CheckersGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()