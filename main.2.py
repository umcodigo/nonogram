import random
from itertools import permutations

from datetime import datetime

SIZE = 10

### Funcoes para criar uma tabela

def print_grid(grid):
    for line in grid:
        print(line)

def create_grid():
    grid = []
    for i in range(SIZE):
        grid.append([])
        for j in range(SIZE):
            grid[i].append(random.randint(0, 1))
    return grid
    
def transpose_grid(grid):
    return [[row[i] for row in grid] for i in range(SIZE)]
    
def valid_grid(grid):
    if grid == []:
        return False
        
    for line in grid:
        if sum(line) == 0:
            return False
            
    tgrid = transpose_grid(grid)
    for line in tgrid:
        if sum(line) == 0:
            return False
            
    return True

def get_counts(grid):
    lines = []
    for i in range(SIZE):
        lines.append([0])
        for j in range(SIZE):
            # print('at', i, j, '- line', lines[i])
            if grid[i][j] == 1:
                lines[i][-1] += 1
            else:
                if lines[i][-1] != 0:
                    lines[i].append(0)
                    
        if lines[i][-1] == 0:
            lines[i].pop()
        
        # print(i, lines[i])
    return lines
        

### Funcoes para resolver

def flatten_perm(perm):
    flat_perm = []
    for item in perm:
        if type(item) is list:
            flat_perm += item
        else:
            flat_perm.append(item)
    return flat_perm
    
def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    
    return [x for x in result if x != None]

def is_valid_perm(perm):
    # cant have two lists (not zeros) side by side
    for i in range(len(perm) - 1):
        if perm[i] != 0 and perm[i+1] != 0:
            return False
    return True
    
def filter_perms(perms, filter_):
    
    def _validate_perm_with_filter(perm, filter_):
        for perm_item, filter_item in zip(perm, filter_):
            if filter_item != None and perm_item != filter_item:
                return False
        return True
    
    return [perm for perm in perms if _validate_perm_with_filter(perm, filter_)]

def create_perms(counts):
    # for [2, 1] in 5
    # 1 1 0 1 0
    # 3 pos for 2 zeros
    # k lists ( 2 lists [1, 1] and [1] ) --> k+1 spaces
    # 0 -> n - sum(counts)
    
    # ( 0, 0, [1, 1], [1] )
    # 
    
    # 0, 0, 0, 0, [1]
    
    # distribuir k listas em SIZE-k+1 espacos
    # C(2, Size-k+1) < 2^size
    
    # [1, 1], [1] --> (k)!
    
    # ^7
    
    # ABC
    # ACB
    # BAC
    # BCA
    # CAB
    # CBA
    
    zeros = SIZE - sum(counts)
    l = zeros * [0]
    
    for k in counts:
        l += [k * [1]]
        
    return_perms = []
    perms = permutations(l)
    
    print('--- counts', counts, l)
    print('--- len ', len(list(perms)))
    
    for perm in perms:
        flat_perm = flatten_perm(perm)
        if is_valid_perm(perm) and flat_perm not in return_perms:
            return_perms.append(flat_perm)
            
    return return_perms
    
def create_filter(perms):
    filter_ = SIZE*[None]
    
    for i in range(SIZE):
        all_equal = True
        
        # if all are 1, sum is len(perms)
        # if all are 0, sum is 0
        # any other value becomes None
        
        sum_ = 0
        for perm in perms:
            sum_ += perm[i]
            
        if sum_ == len(perms):
            filter_[i] = 1
        elif sum_ == 0:
            filter_[i] = 0
            
    return filter_
            
def is_done(grid):
        for line in grid:
            for item in line:
                if item == None:
                    return False
        return True
    
            
def solve_grid(lines, cols):
    
    possible_lines = SIZE*[[]]
    filter_lines = SIZE*[[]]
    for i in range(SIZE):
        possible_lines[i] = create_perms(lines[i])
        filter_lines[i] = create_filter(possible_lines[i])
    
    # print('Possible lines')
    # print_grid(possible_lines)
    # print_grid(filter_lines)
        
    
    possible_cols = SIZE*[[]]
    filter_cols = SIZE*[[]]
    for i in range(SIZE):
        possible_cols[i] = create_perms(cols[i])
        filter_cols[i] = create_filter(possible_cols[i])
        
    # print('Possible cols')
    # print_grid(possible_cols)
    # print_grid(filter_cols)

    count = 0
    last_filter_lines = None
    while not is_done(filter_lines):
        print('--- iter -----------------------')
        count += 1
        
        # checlk last
        if last_filter_lines == filter_lines:
            print('Tabela não convergiu. Defina algum dos valores:')
            i = int(input('Linha (1 - {}): '.format(SIZE)))
            j = int(input('Coluna (1 - {}): '.format(SIZE)))
            v = int(input('Valor (0 ou 1): '))
            filter_cols[j-1][i-1] = v
            
            
        last_filter_lines = filter_lines.copy()
        
        # check lines with col filters
        for i in range(SIZE):
            possible_lines[i] = filter_perms(
                possible_lines[i],
                [filter_cols[j][i] for j in range(SIZE)]
            )
            filter_lines[i] = create_filter(possible_lines[i])
            
        print('Possible lines')
        # print_grid(possible_lines)
        print_grid(filter_lines)
            
        
        # check cols with lines filters
        for i in range(SIZE):
            possible_cols[i] = filter_perms(
                possible_cols[i],
                [filter_lines[j][i] for j in range(SIZE)]
            )
            filter_cols[i] = create_filter(possible_cols[i])
        
        # print('Possible cols')
        # print_grid(possible_cols)
        # print_grid(filter_cols)
        
    print('Tabela convergiu em {} iterações!'.format(count))


if __name__ == '__main__':
    
    start = datetime.now()
    
    # Teste
    grid = []
    while not valid_grid(grid):
        grid = create_grid()
        
    print_grid(grid)
    
    lines = get_counts(grid)
    cols = get_counts(transpose_grid(grid))
    
    # Real
    # lines = [ [6], [3, 1], [1, 2], [2, 3], [6], [4], [5], [2, 4], [2, 4, 1], [3, 6] ]
    # cols = [ [1], [1, 3, 3], [2, 7], [2, 3], [2, 7], [1, 8], [5, 4], [3], [1], [2] ]
    
    # lines = []
    # cols = []
    
    
    # Solve
    solve_grid(lines, cols)
    
    end = datetime.now()
    print(end-start)