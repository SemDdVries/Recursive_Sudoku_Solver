import os
from Game import Game
from Sudoku import Sudoku
import re

sudoku_folder = os.path.join(os.path.dirname(__file__), "Sudokus")

class App:

    @staticmethod
    def solve_sudoku(sudoku_file):
        game = Game(Sudoku(sudoku_file))
        game.show_sudoku()
        #Make sure to change the heuristic by adjusting game.solve() to either:
        #game.solve('fifo') --> baseline
        #game.solve('mrv') --> minimum remaining values
        #game.solve('lcv') --> prioritize finalized arc fields, Least Constraining Values
        if (game.solve('mrv') and game.valid_solution()):
            print("\nSolved sudoku:")
            game.show_sudoku()
        else:
            print("Could not solve this sudoku :(")

    @staticmethod
    def start():
        while True:
            file_num = input("Enter Sudoku file (1-5): ")
            print("\n")

            file = None
            for filename in os.listdir(sudoku_folder):
                if file_num in filename:
                    file = filename
            if file is not None:
                App.solve_sudoku(os.path.join(sudoku_folder, file))
            else:
                print("Invalid choice")

            continue_input = input("Continue? (yes/no): ")
            if not re.search(r'^y[a-z]*', continue_input.lower()):
                break

if __name__ == "__main__":
    App.start()

