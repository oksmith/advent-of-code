import copy
import itertools
from collections import Counter, defaultdict


INITIAL_CUBES = 'inputs/17_input.txt'


def count_neighbours(coord, coords_dict, n_dim):
    """
    Count active cubes surrounding a coordinate.
    """
    surrounding_cubes = [
        x for x in itertools.product(*[[coord[i]-1,coord[i],coord[i]+1] for i in range(n_dim)]) 
        if x != coord
    ]
    counter = Counter([coords_dict[cube] for cube in surrounding_cubes])
    return counter


def apply_rules(coords_dict, n_dim):
    new_coords_dict = {}
    
    surrounding_cubes = list(set([
        x 
        for c in dict(coords_dict).keys() 
        for x in itertools.product(*[[c[i]-1,c[i],c[i]+1] for i in range(n_dim)]) 
    ]))
    
    for coord in surrounding_cubes:
        counter = count_neighbours(coord, coords_dict, n_dim=n_dim)
        if coords_dict[coord] == '#':
            if counter['#'] in [2, 3]:
                new_coords_dict[coord] = '#'
            else:
                new_coords_dict[coord] = '.'
        elif coords_dict[coord] == '.':
            if counter['#'] in [3]:
                new_coords_dict[coord] = '#'
            else:
                new_coords_dict[coord] = '.'
    
    return defaultdict(lambda: '.', new_coords_dict)


def count_active_states_after_n_iterations(cubes, n_dim, n_iterations):
    initital_xy_coords = list(itertools.product(range(len(cubes[0])), range(len(cubes))))
    coords_dict = defaultdict(
        lambda: '.', 
        {(x, y, *[0]*(n_dim-2)): val for (x, y), val in zip(initital_xy_coords, [cubes[j][i] for i, j in initital_xy_coords])}
    )

    for i in range(n_iterations):
        coords_dict = apply_rules(coords_dict, n_dim=n_dim)
        
    return Counter(coords_dict.values())['#']


if __name__ == '__main__':

    with open(INITIAL_CUBES, 'r') as f:
        cubes = [list(line) for line in f.read().strip().split("\n")]

    print('Part 1 Solution: {}'.format(
        count_active_states_after_n_iterations(cubes, n_dim=3, n_iterations=6)
    ))
    
    print('Part 2 Solution: {}\n'.format(
        count_active_states_after_n_iterations(cubes, n_dim=4, n_iterations=6)
    ))
