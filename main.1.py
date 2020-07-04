import random
from itertools import permutations

n = 5

### building grid

def print_grid(grid):
    for line in grid:
        print(line)

def create_grid(n):
    grid = []
    for i in range(n):
        grid.append([])
        for j in range(n):
            grid[i].append(random.randint(0, 1))
    return grid
    
def valid_grid(grid):
    if grid == []:
        return False
        
    for line in grid:
        if sum(line) == 0:
            return False
    return True

def get_counts(grid):
    lines = []
    for i in range(n):
        lines.append([0])
        for j in range(n):
            # print('at', i, j, '- line', lines[i])
            if grid[i][j] == 1:
                lines[i][-1] += 1
            else:
                if lines[i][-1] != 0:
                    lines[i].append(0)
                    
        if lines[i][-1] == 0:
            lines[i].pop()
        
        print(i, lines[i])
    return lines
        
def transpose_grid(grid):
    n = len(grid)
    return [[row[i] for row in grid] for i in range(n)]

print('--- grid')
grid = []
while not valid_grid(grid):
    grid = create_grid(n)
    
print_grid(grid)

print('--- lines')
lines = get_counts(grid)

print('--- cols')
cols = get_counts(transpose_grid(grid))

### now trying to solve
check_grid = n*[n*[None]]

def fill_determined(lines, grid):
    for i in range(n):
        if sum(lines[i]) + len(lines[i]) - 1 == n:
            temp_line = []
            for k in lines[i]:
                temp_line += k*[1]
                if len(temp_line) < n:
                    temp_line += [0]
            grid[i] = temp_line
    return grid

print('--- check lines')
check_grid = fill_determined(lines, check_grid)            
print_grid(check_grid)

print('--- check cols')
check_grid = transpose_grid(check_grid)
check_grid = fill_determined(cols, check_grid)   
check_grid = transpose_grid(check_grid)
print_grid(check_grid)


print('--- ')


def flatten_perm(perm):
    flat_perm = []
    for item in perm:
        if type(item) is list:
            flat_perm += item
        else:
            flat_perm.append(item)
    return flat_perm

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

def create_perms(counts, n):
    # fo [2, 1] in 5
    # 1 1 0 1 0
    # 3 pos for 2 zeros
    # k lists ( 2 lists [1, 1] and [1] ) --> k+1 spaces
    # 0 -> n - sum(counts)
    
    # ( [0], [0], [1, 1], [1] )
    # 
    
    zeros = n - sum(counts)
    l = zeros * [0]
    
    for k in counts:
        l += [k * [1]]
        
    return_perms = []
    for perm in permutations(l):
        flat_perm = flatten_perm(perm)
        if is_valid_perm(perm) and flat_perm not in return_perms:
            return_perms.append(flat_perm)
            
    return return_perms
    
def create_filter(perms, n):
    filter_ = n*[None]
    
    for i in range(n):
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
            
            
            
    
# print('--- ')
# perms = create_perms([2, 1], 5)
# for perm in perms:
#     print(perm)


# print('--- ')  
# filter_ = [None, None, None, None, 0]
# perms = filter_perms(perms, filter_)
# for perm in perms:
#     print(perm)

print('Possible lines')
for i in range(n):
    print(i, lines[i], n)
    perms = create_perms(lines[i], n)
    print('  p', perms)
    print('  f', create_filter(perms, n))
    
print('Possible cols')
for i in range(n):
    print(i, cols[i], n)
    perms = create_perms(cols[i], n)
    print('  p', perms)
    print('  f', create_filter(perms, n))