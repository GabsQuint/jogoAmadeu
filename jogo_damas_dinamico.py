import tkinter as tk
import random

# Configurações do tabuleiro
BOARD_SIZE = 8
PLAYER_1 = "O"
PLAYER_2 = "X"
EMPTY = "."
TRAP = "T"
BONUS = "B"

class CheckersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Damas Dinâmico")
        
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.selected_piece = None
        self.turn = PLAYER_1
        self.message = tk.StringVar(value="Turno: Jogador O")
        
        # Estados especiais das peças
        self.piece_states = {}  # { (x, y): {"bonus": bool, "trapped": bool} }
        
        self.initialize_board()
        self.add_dynamic_elements()
        self.create_ui()
    
    def initialize_board(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if i < 3 and (i + j) % 2 == 1:
                    self.board[i][j] = PLAYER_1
                elif i > 4 and (i + j) % 2 == 1:
                    self.board[i][j] = PLAYER_2

    def add_dynamic_elements(self):
        valid_positions = [
            (i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)
            if (i + j) % 2 == 1 and self.board[i][j] == EMPTY
        ]
        for _ in range(random.randint(3, 6)):
            if valid_positions:
                x, y = random.choice(valid_positions)
                self.board[x][y] = random.choice([TRAP, BONUS])
                valid_positions.remove((x, y))

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        
        self.draw_board()
        
        self.message_label = tk.Label(self.root, textvariable=self.message)
        self.message_label.pack()

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 400 // BOARD_SIZE
        
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                
                piece = self.board[i][j]
                if piece != EMPTY:
                    piece_color = {
                        PLAYER_1: "red",
                        PLAYER_2: "blue",
                        TRAP: "black",
                        BONUS: "green"
                    }.get(piece, "black")
                    self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=piece_color)
                    
                    # Indicação visual de estados especiais
                    if (i, j) in self.piece_states:
                        if self.piece_states[(i, j)].get("bonus"):
                            self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="green", width=3)
                        if self.piece_states[(i, j)].get("trapped"):
                            self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="black", width=3)
                        # Adicione um estado temporário para as peças com bônus
                        self.piece_states[(i, j)]["bonus_active"] = True
        
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        cell_size = 400 // BOARD_SIZE
        col, row = event.x // cell_size, event.y // cell_size

        if self.selected_piece:
            start_x, start_y = self.selected_piece
            if self.is_valid_move(start_x, start_y, row, col):
                self.make_move(start_x, start_y, row, col)
            self.selected_piece = None
        else:
            if self.board[row][col] == self.turn and not self.piece_states.get((row, col), {}).get("trapped", False):
                self.selected_piece = (row, col)
        
        self.draw_board()

    def is_valid_move(self, start_x, start_y, end_x, end_y):
        piece = self.board[start_x][start_y]
        state = self.piece_states.get((start_x, start_y), {})
    
        # Movimento de rainha (bônus ativo)
        if state.get("bonus") and abs(start_x - end_x) == abs(start_y - end_y):
            # Verifica caminho livre
            dx = 1 if end_x > start_x else -1
            dy = 1 if end_y > start_y else -1
            for step in range(1, abs(start_x - end_x)):
                if self.board[start_x + step * dx][start_y + step * dy] not in [EMPTY, BONUS, TRAP]:
                    return False
            return True
        
        # Movimento normal ou captura
        if abs(start_x - end_x) == 1 and abs(start_y - end_y) == 1 and self.board[end_x][end_y] in [EMPTY, BONUS, TRAP]:
            return True
        if abs(start_x - end_x) == 2 and abs(start_y - end_y) == 2:
            middle_x = (start_x + end_x) // 2
            middle_y = (start_y + end_y) // 2
            if self.board[middle_x][middle_y] in [PLAYER_1, PLAYER_2] and self.board[middle_x][middle_y] != self.turn:
                if self.board[end_x][end_y] in [EMPTY, BONUS, TRAP]:
                    return True
        return False


    def make_move(self, start_x, start_y, end_x, end_y):
        piece = self.board[start_x][start_y]
        state = self.piece_states.pop((start_x, start_y), {})

        # Captura de peça inimiga
        if abs(start_x - end_x) == 2 and abs(start_y - end_y) == 2:
            middle_x = (start_x + end_x) // 2
            middle_y = (start_y + end_y) // 2
            self.board[middle_x][middle_y] = EMPTY  # Remove a peça capturada
        
        # Movimentar peça
        target_cell = self.board[end_x][end_y]
        self.board[end_x][end_y] = piece
        self.board[start_x][start_y] = EMPTY

        # Atualizar estados
        if target_cell == TRAP:
            state["trapped"] = True
            self.message.set(f"A peça ficou presa!")
        elif target_cell == BONUS:
            state["bonus"] = True
            self.message.set(f"Bônus! A peça pode se mover como rainha na próxima jogada.")

        # Salva o estado atualizado
        if state:
            self.piece_states[(end_x, end_y)] = state

        # Verificar vitória
        winner = self.check_victory()
        if winner:
            self.message.set(f"Jogador {winner} venceu!")
            return

        # Alternar turno
        self.turn = PLAYER_1 if self.turn == PLAYER_2 else PLAYER_2
        self.message.set(f"Turno: Jogador {self.turn}")

    def check_victory(self):
        p1_pieces = sum(row.count(PLAYER_1) for row in self.board)
        p2_pieces = sum(row.count(PLAYER_2) for row in self.board)
        if p1_pieces == 0:
            return PLAYER_2
        elif p2_pieces == 0:
            return PLAYER_1
        return None

    def can_capture(self, piece, target):
        if self.piece_states[piece].get("bonus_active"):
            # Lógica para capturar como a rainha
            return True
        # Lógica normal de captura
        return False

    def move_piece(self, from_pos, to_pos):
        piece = self.board[from_pos[0]][from_pos[1]]
        if self.piece_states[piece].get("bonus_active"):
            self.piece_states[piece]["bonus_active"] = False
        # Lógica normal de movimento

def main():
    root = tk.Tk()
    game = CheckersGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
