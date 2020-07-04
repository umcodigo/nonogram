

SAVED_PERMS = {} # dicts are hashtables

TRACK = {'count': 0}

def perms(list_):
    
    # print('f({})'.format(list_))
    
    if str(list_) in SAVED_PERMS:
        return SAVED_PERMS[str(list_)]
    
    TRACK['count'] += 1
    
    if len(list_) == 1:
        return [list_]
    else:
        return_list = []
        for i, item in enumerate(list_):
            others = list_.copy()
            others.pop(i)
            for p in perms(others):
                to_append = [item] + p
                if to_append not in return_list:
                    return_list.append( to_append )
            
        SAVED_PERMS.update({ str(list_): return_list })
        
        return return_list

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


print('---')

my_list = [ [1, 1], [1] ] + 2 * [None]

my_perms = perms(my_list)
print(len(my_perms), 'permutations')

# my_perms = remove_duplicates(my_perms)
# print(len(my_perms), 'permutations')

print(TRACK['count'], 'operations')
print(len(SAVED_PERMS), 'saved perms')

for p in my_perms:
    print(intersperse(p, 0))