from datetime import datetime
import random

from lib import *


if __name__ == '__main__':
    start = datetime.now()
    
    good = 0
    bad = 0
    
    for i in range(100):
        print('---')
        
        n = 5*random.randint(1, 6)
        print(i+1, 'Tamanho', n)
        grid = []
        while not valid_grid(grid):
            # grid = create_easy_grid(n, chances=2)
            grid = create_grid(n)
            
        # print_grid(grid)
        
        lines = get_counts(grid)
        cols = get_counts(transpose_grid(grid))
    
        try:
            grid, count = solve_grid(n, lines, cols)
            # print_grid(grid)
            print('Tabela convergiu em {} iterações!'.format(count))
            good += 1
            
        except:
            print('Tabela não convergiu')
            bad += 1
        
    
    print('good', good)
    print('bad', bad)

    end = datetime.now()
    print(end-start)
