import random

### Funcoes para criar uma tabela

def print_grid(grid):
    for line in grid:
        print(line)

def pprint_grid(grid):
    for i, line in enumerate(grid):
        if i % 5 == 0:
            print('-')
        
        for j, num in enumerate(line):
            if j % 5 == 0:
                print('| ', end='')
            print(str(num) + ' ', end='')
        print('')

def create_grid(n):
    grid = []
    for i in range(n):
        line = []
        for j in range(n):
            rand = random.randint(0, 1)
            line.append(rand)
        grid.append(line)
    return grid

def create_easy_grid(n, chances):
    grid = []
    for i in range(n):
        line = []
        for j in range(n):
            rand = random.randint(0, chances)
            num = 0 if rand == 0 else 1
            line.append(num)
        grid.append(line)
    return grid
    
def transpose_grid(grid):
    return [[row[i] for row in grid] for i in range(len(grid))]
    
def valid_grid(grid):
    if grid == []:
        return False
        
    # checar linhas
    for line in grid:
        if sum(line) == 0:
            return False
            
    # checar colunas
    tgrid = transpose_grid(grid)
    for line in tgrid:
        if sum(line) == 0:
            return False
            
    return True

def get_counts(grid):
    
    lines = []
    n = len(grid)
    for i in range(n):
        line = []
        count = 0
        for j in range(n):
            
            if grid[i][j] == 1:
                count += 1
                
            elif grid[i][j] == 0:
                if count != 0:
                    line.append(count)
                    count = 0
                    
        if count != 0:
            line.append(count)
            count = 0
                    
        lines.append(line)
        
    return lines
        

### Funcoes para resolver

## Funcoes para linhas (permutacoes)

def flatten_perm(perm):
    flat_perm = []
    for item in perm:
        if type(item) is list:
            flat_perm += item
        else:
            flat_perm.append(item)
    return flat_perm
    
def filter_perms(perms, filter_):
    
    def _validate_perm_with_filter(perm, filter_):
        for perm_item, filter_item in zip(perm, filter_):
            if filter_item != None and perm_item != filter_item:
                return False
        return True
    
    return [perm for perm in perms if _validate_perm_with_filter(perm, filter_)]

def create_line_filter(perms):

    if len(perms) < 1: return None

    n = len(perms[0])
    filter_ = n*[None]
    
    for i in range(n):
        
        sum_ = 0
        for perm in perms:
            sum_ += perm[i]
            
        if sum_ == len(perms):
            filter_[i] = 1

        elif sum_ == 0:
            filter_[i] = 0
            
    return filter_

## Funcoes para grid

def is_done(grid):
    for line in grid:
        for item in line:
            if item == None:
                return False
    return True

def somas(m, soma):
    # ex: a + b + c = 2
    # print('somas', m, soma)

    if m < 0 or soma < 0:
        return []

    if soma == 0:
        return [m*[0]]

    if m == 1:
        return [[soma]]

    return_somas = []
    for i in range(soma+1):
        for s in somas(m-1, soma-i):
            return_somas.append([i] + s)

    return return_somas

def create_perms(n, counts):
    # print('\n\ncreate_perms', counts)
    
    blocks = [[0]] * (len(counts) * 2 - 1)
    blocks[0::2] = [[1]*c for c in counts]
    # print('blocks', blocks)
    
    zeros = n - sum([len(b) for b in blocks])
    # print('zeros', zeros)
    
    perms = []
    for abc_list in somas(len(blocks) + 1, zeros):
        
        perm = [None] * (len(blocks) + len(abc_list))
        perm[0::2] = [abc*[0] for abc in abc_list]
        perm[1::2] = blocks
        perms.append(flatten_perm(perm))
    
    # print(len(perms), perms)
    return perms

def update_grid(grid, filter_):
    return_grid = []
    n = len(grid)

    for i in range(n):
        temp_line = []
        for j in range(n):
            if filter_[i][j] != None:
                temp_line.append(filter_[i][j])
            else:
                temp_line.append(grid[i][j])
        return_grid.append(temp_line)
    return return_grid
    
def solve_grid(n, lines, cols, partial_grid=None):
    

    grid = n*[n*[None]]

    perm_lines = n*[[]]
    filter_lines = n*[[]]

    perm_cols = n*[[]]
    filter_cols = n*[[]]

    for i in range(n):
        perm_lines[i] = create_perms(n, lines[i])
        filter_lines[i] = create_line_filter(perm_lines[i])

        perm_cols[i] = create_perms(n, cols[i])
        filter_cols[i] = create_line_filter(perm_cols[i])

    count = 0
    last_grid = None
    while not is_done(grid):
        count += 1

        last_grid = grid.copy()

        grid = update_grid(grid, filter_lines)
        grid = update_grid(grid, transpose_grid(filter_cols))

        trasposed_grid = transpose_grid(grid)
        for i in range(n):
            perm_lines[i] = filter_perms(perm_lines[i], grid[i])
            filter_lines[i] = create_line_filter(perm_lines[i])

            perm_cols[i] = filter_perms(perm_cols[i], trasposed_grid[i])
            filter_cols[i] = create_line_filter(perm_cols[i])            


        # print_grid(grid)
        # print('----')
    
        if grid == last_grid:
            raise Exception('not convergent')
        
    return grid, count