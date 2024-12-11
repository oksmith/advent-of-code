import copy
import itertools
from collections import Counter, defaultdict

HEX_COORDINATES = 'inputs/24_input.txt'


HEX_COORDINATES_DICT = {
    'e': (2, 0), 
    'se': (1, -1), 
    'sw': (-1, -1), 
    'w': (-2, 0), 
    'nw': (-1, 1), 
    'ne': (1, 1)
}


def _split_string(line):
    split = []
    line_lst = list(line)
    while len(line_lst) > 0:
        char = line_lst.pop(0)
        if char in ['e', 'w']:
            split.append(char)
        else:
            second_char = line_lst.pop(0)
            split.append(char+second_char)
    return split


def get_neighbours(coord):
    return [(coord[0]+v[0], coord[1]+v[1]) for v in HEX_COORDINATES_DICT.values()]


def count_adjacent(coord, layout):
    return Counter([layout[c] for c in get_neighbours(coord)])


if __name__ == '__main__':

    with open(HEX_COORDINATES, 'r') as f:
        lines = f.read().strip().split('\n')
        split_lines = [_split_string(line) for line in lines]
        coordinates_lst = [[HEX_COORDINATES_DICT[x] for x in line] for line in split_lines]
        coordinates = [(sum([x[0] for x in lst]), sum([x[1] for x in lst])) for lst in coordinates_lst]
        
        
    flip_count = Counter(coordinates)
    layout = defaultdict(
        int,
        {coord: flip_count[coord] % 2 for coord in flip_count.keys()}  # 0 means white, 1 means black
    )
    

    print('Part 1 Solution: {}'.format(
        Counter(layout.values())[1]
    ))
    
    for _ in range(100):
        tlayout = copy.deepcopy(layout)

        keys_to_check = list(layout.keys())
        neighbours = list(itertools.chain.from_iterable(
            [get_neighbours(coord) for coord in keys_to_check]
        ))
        keys_to_check = list(set(keys_to_check + neighbours))
        
        for coord in keys_to_check:
            c = count_adjacent(coord, layout)[1]
            if layout[coord] == 1 and (c == 0 or c > 2):
                tlayout[coord] = 0
            elif layout[coord] == 0 and c == 2:
                tlayout[coord] = 1
            else:
                pass

        layout = tlayout

    print('Part 2 Solution: {}\n'.format(
        Counter(layout.values())[1]
    ))
