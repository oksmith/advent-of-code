import numpy as np

MAP = 'inputs/03_input.txt'

SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]


def number_of_trees_hit(layers, slope, horizontal_max):
    x = 0
    y = 0
    number_of_trees_hit = 0
    slope_horizontal, slope_vertical = slope

    for layer in range(len(layers)):

        if layers[y][x] == '#':
            number_of_trees_hit += 1

        x = (x + slope_horizontal) % horizontal_max
        y += slope_vertical
        
        if y >= len(layers):
            break
        
    return number_of_trees_hit

        

if __name__ == '__main__':

    with open(MAP, 'r') as f:
        layers = [str(line).strip('\n') for line in f.readlines()]
        
    assert all([len(layer) == len(layers[0]) for layer in layers]), 'ERROR: Unequal row lengths'
    horizontal_max = len(layers[0])
        
    print('Number of layers to traverse: {}'.format(len(layers)))
    print('Max number of horizontal squares before looping: {}\n'.format(horizontal_max))
    
    
    print('Part 1 Solution: {}'.format(
        number_of_trees_hit(layers, slope=(3,1), horizontal_max=horizontal_max)
    ))
    
    n_trees = []
    for slope in SLOPES:
        n_trees.append(number_of_trees_hit(layers, slope=slope, horizontal_max=horizontal_max))

    print('Part 2 Solution: {}\n'.format(np.prod(n_trees)))
