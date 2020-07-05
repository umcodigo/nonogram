from datetime import datetime
from lib import *


if __name__ == '__main__':
    
    start = datetime.now()
    
    # Teste
    n = 5

    grid = []
    while not valid_grid(grid):
        grid = create_easy_grid(n, chances=2)
        
    # print_grid(grid)
    
    lines = get_counts(grid)
    cols = get_counts(transpose_grid(grid))

    # Solve
    grid, count = solve_grid(n, lines, cols)
    print_grid(grid)
    print('Tabela convergiu em {} iterações!'.format(count))
    
    
    end = datetime.now()
    print(end-start)
