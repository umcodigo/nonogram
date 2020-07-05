from datetime import datetime
import random

from lib import *


if __name__ == '__main__':
    start = datetime.now()
    
    

    MAX_BOARD = 6 # 5*5
    MAX_ITER = 5
    
    for odds in range(2, 5):
        print('Odds', odds)

        for m in range(1, MAX_BOARD):
            n = 5*m
            good = 0
            bad = 0
            
            for i in range(MAX_ITER):
                # print('---')
                
                grid = []
                while not valid_grid(grid):
                    grid = create_easy_grid(n, odds)
                    # grid = create_grid(n)
                    
                # print_grid(grid)
                
                lines = get_counts(grid)
                cols = get_counts(transpose_grid(grid))
            
                try:
                    grid, count = solve_grid(n, lines, cols)
                    # print_grid(grid)
                    # print('Tabela convergiu em {} iterações!'.format(count))
                    good += 1
                    
                except:
                    # print('Tabela não convergiu')
                    bad += 1
                
            # print('good', good)
            # print('bad', bad)

            print('  Tamanho', n, 100*good/(good+bad), '%')

    end = datetime.now()
    print(end-start)
