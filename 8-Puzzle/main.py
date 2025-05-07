import heapq
import tkinter as tk
from collections import deque
from heapq import heappop, heappush

class Puzzle8:
    def __init__(self, initial_state):
        self.initial_state = tuple(initial_state)
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.moves = {
            0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
            3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
            6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
        }
    
    def count_inversions(self, state):
        numbers = [num for num in state if num != 0]
        inversions = 0
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] > numbers[j]:
                    inversions += 1
        return inversions
    
    def is_solvable(self):
        return self.count_inversions(self.initial_state) % 2 == 0
    
    def bfs(self):
        queue = deque([(self.initial_state, [])])
        visited = set()
        tested_state = 0
        
        while queue:
            state, path = queue.popleft()
            tested_state += 1
            if state == self.goal_state:
                return path, tested_state
            
            visited.add(state)
            zero_index = state.index(0)
            
            for move in self.moves[zero_index]:
                new_state = list(state)
                new_state[zero_index], new_state[move] = new_state[move], new_state[zero_index]
                new_tuple = tuple(new_state)
                if new_tuple not in visited:
                    queue.append((new_tuple, path + [new_tuple]))
        return None, tested_state
    
    def misplaced_tiles(self, state):   
        misplaced = 0
        for i in range(9):
            if state[i] != 0 and state[i] != self.goal_state[i]:
                misplaced += 1 # Então a preça esta fora do lugar
        return misplaced
    
    def a_star(self):
        open_list = []
        closed_list = set()
        
        g = 0
        h = self.misplaced_tiles(self.initial_state)
        f = g + h
        
        heapq.heappush(open_list, (f, g, self.initial_state, [])) # Insere o primeiro item na open_list
        tested_state = 0
        
        while open_list:
                f, g, state, path = heapq.heappop(open_list)
                tested_state += 1
                
                if state == self.goal_state:
                    print("Caminho encontrado:", path)
                    return path, tested_state
                
                closed_list.add(state) # Se não é o objetivo final, adiciona ele à closed_list
                zero_index = state.index(0)
                
                for move in self.moves[zero_index]:
                    new_state = list(state) # state é uma tupla, converter para lista
                    new_state[zero_index], new_state[move] = new_state[move], new_state[zero_index] # Faz o swap entre o zero e o número que está na posição do movimento
                    new_tuple = tuple(new_state) # Converte de volta para tupla
                    
                    if new_tuple not in closed_list:
                        # Calcula heurística
                        new_g = g + 1
                        new_h = self.misplaced_tiles(new_tuple)
                        new_f = new_g + new_h
                        heapq.heappush(open_list, (new_f, new_g, new_tuple, path + [new_tuple])) # heurística + custo atual + estado atual + caminho atual
                                   
        return None, tested_state
     
class PuzzleGUI:
    def __init__(self, root, initial_state):
        self.root = root
        self.root.title("8-Puzzle Comparação: BFS vs A*")
        self.root.geometry("+100+100")  # Posiciona a janela no canto superior esquerdo (left=100, top=100)

        self.puzzle_bfs = Puzzle8(initial_state)
        self.puzzle_astar = Puzzle8(initial_state)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.bfs_frame = tk.Frame(self.main_frame)
        self.bfs_frame.grid(row=0, column=0, padx=20)

        self.astar_frame = tk.Frame(self.main_frame)
        self.astar_frame.grid(row=0, column=1, padx=20)

        tk.Label(self.bfs_frame, text="BFS", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))
        tk.Label(self.astar_frame, text="A*", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.buttons_bfs = self.create_grid(self.puzzle_bfs.initial_state, self.bfs_frame)
        self.buttons_astar = self.create_grid(self.puzzle_astar.initial_state, self.astar_frame)

        self.result_bfs = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_bfs.pack()

        self.result_astar = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_astar.pack()

        self.solve_button = tk.Button(self.root, text="Resolver", command=self.solve)
        self.solve_button.pack(pady=10)

    def create_grid(self, state, parent_frame):
        buttons = []
        for i in range(9):
            row, col = divmod(i, 3)
            btn = tk.Button(parent_frame, text=str(state[i]) if state[i] != 0 else "",
                            width=5, height=2, font=("Arial", 20))
            btn.grid(row=row+1, column=col, padx=2, pady=2)
            buttons.append(btn)
        return buttons

    def update_grid(self, buttons, state):
        for i in range(9):
            buttons[i].config(text=str(state[i]) if state[i] != 0 else "")
        self.root.update()
        self.root.after(200)

    def solve(self):
        if not self.puzzle_bfs.is_solvable():
            print("O estado inicial não é solucionável.")
            return

        path_bfs, tested_bfs = self.puzzle_bfs.bfs()
        path_astar, tested_astar = self.puzzle_astar.a_star()

        for state_bfs, state_astar in zip(path_bfs, path_astar):
            self.update_grid(self.buttons_bfs, state_bfs)
            self.update_grid(self.buttons_astar, state_astar)

        self.result_bfs.config(text=f"BFS - Movimentos: {len(path_bfs)} | Testados: {tested_bfs}")
        self.result_astar.config(text=f"A*  - Movimentos: {len(path_astar)} | Testados: {tested_astar}")

if __name__ == "__main__":
    initial_state = [8, 1, 2, 0, 4, 3, 7, 6, 5]  # Pode ser alterado para testar
    root = tk.Tk()
    app = PuzzleGUI(root, initial_state)
    root.mainloop()