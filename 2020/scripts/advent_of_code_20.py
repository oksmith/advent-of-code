import itertools
import copy
import numpy as np
from collections import Counter


IMAGE_TILES = 'inputs/20_input.txt'

SEA_MONSTER_PATTERN = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "
]

N_TILES = 144


def flip_tile(tile):
    return tile[::-1]


def rotate_tile(tile, rot):
    return np.rot90(tile, rot)


def get_borders(tile):
    return {'top': ''.join(tile[0,:]), 'bottom': ''.join(tile[-1,:]), 'left': ''.join(tile[:,0]), 'right': ''.join(tile[:,-1])}


def find_corner_and_edge_tiles(tiles):
    corner_tiles, edge_tiles = [], []
    tile_borders = {}
    unique_borders_dict = {}
    
    for tile_id, tile in tiles.items():
        borders = set()
        for rot in [0,1,2,3]:
            for t in [tile, flip_tile(tile)]:
                borders = set(borders).union(list(get_borders(rotate_tile(t, rot)).values()))
        
        # Append unique borders for a given tile (all orientations)
        tile_borders[tile_id] = list(borders)
        
    all_possible_borders = list(itertools.chain.from_iterable(tile_borders.values()))
    print('Maximum number of times a given border appears in this set: {}!'.format(
        max(Counter(all_possible_borders).values())
    ))
    
    for tile_id, border_set in tile_borders.items():
        unique_borders = []
        for border in border_set:
            if all_possible_borders.count(border) == 1:
                unique_borders.append(border)
                
        
        if len(unique_borders) == 4:
            corner_tiles.append(tile_id)
        elif len(unique_borders) == 2:
            edge_tiles.append(tile_id)
            
        unique_borders_dict[tile_id] = unique_borders
        
    return corner_tiles, edge_tiles, unique_borders_dict


def product(list):
    prod = 1
    for x in list:
        prod = prod * x
        
    return prod


def get_types(corner_tile_id, unique_borders):
    borders = get_borders(tiles[corner_tile_id])
    t = []
    for type, border in borders.items():
        if border in unique_borders[corner_tile_id]:
            t.append(type)  
    return t

def classify_corner_tiles(tiles, corner_tiles, unique_borders):
    types = {}

    for corner_tile in corner_tiles:
        t = get_types(corner_tile, unique_borders)

        while '-'.join(t) in types.keys():
            # try rotating 90 degrees and try again - like a jigsaw
            tiles[corner_tile] = rotate_tile(tiles[corner_tile], 1)
            t = get_types(corner_tile, unique_borders)

        types['-'.join(t)] = corner_tile

    return types


def left_right_neighbours(left, right, tiles):
    left_tile = tiles[left]
    right_tile = tiles[right]

    if all(left_tile[:, -1] == right_tile[:, 0]):
        return True
    
    return False


def top_bottom_neighbours(top, bottom, tiles):
    top_tile = tiles[top]
    bottom_tile = tiles[bottom]
    if all(top_tile[-1, :] == bottom_tile[0, :]):
        return True
    return False


def find_bottom_neighbour(top, tiles, assembled_ids):
    for tile_id in tiles.keys():
        if tile_id not in assembled_ids:
            for rot in [0,1,2,3]:
                tiles[tile_id] = rotate_tile(tiles[tile_id], rot)
                neighbour = top_bottom_neighbours(top, tile_id, tiles)
                if neighbour:
                    return tile_id
                
                tiles[tile_id] = flip_tile(tiles[tile_id])
                neighbour = top_bottom_neighbours(top, tile_id, tiles)
                if neighbour:
                    return tile_id
                
    return None


def find_right_neighbour(left, tiles, assembled_ids):
    for tile_id in tiles.keys():
        if tile_id not in assembled_ids:
            for rot in [0,1,2,3]:
                tiles[tile_id] = rotate_tile(tiles[tile_id], rot)
                neighbour = left_right_neighbours(left, tile_id, tiles)
                if neighbour:
                    return tile_id
                
                tiles[tile_id] = flip_tile(tiles[tile_id])
                neighbour = left_right_neighbours(left, tile_id, tiles)
                if neighbour:
                    return tile_id
                
    return None


def assemble_grid(tiles, corner_tiles, edge_tiles, unique_borders):

    try:
        corner_tile_types = classify_corner_tiles(tiles, corner_tiles, unique_borders)

        # Initialise the grid
        grid_ids = np.array([[None for _ in range(int(np.sqrt(N_TILES)))]]*int(np.sqrt(N_TILES)))
        if 'top-left' in corner_tile_types.keys():
            grid_ids[0,0] = corner_tile_types['top-left']
        else:
            grid_ids[0,0] = corner_tile_types['left-top']

        assembled_ids = [grid_ids[0,0]]

        for i in range(int(np.sqrt(N_TILES))):
            for j in range(int(np.sqrt(N_TILES))):
                if grid_ids[i,j]:
                    # Encountered the tile already as a corner tile
                    pass

                elif j == 0:
                    # find the bottom neighbour
                    bottom_neighbour = find_bottom_neighbour(grid_ids[i-1, j], tiles, assembled_ids)
                    grid_ids[i,j] = bottom_neighbour
                    assembled_ids.append(bottom_neighbour)   

                else:
                    # find the right hand neighbour
                    right_neighbour = find_right_neighbour(grid_ids[i, j-1], tiles, assembled_ids)
                    grid_ids[i,j] = right_neighbour
                    assembled_ids.append(right_neighbour)

        print(grid_ids)
        return grid_ids

    except (IndexError, KeyError):
        # Debugging lines
        print('Configuration did not work!')
        print(grid_ids)
        
        print('top-left: {}'.format(grid_ids[0,0]))
        print(tiles[grid_ids[0,0]])
        print(unique_borders[grid_ids[0,0]])
        
        print('top-right: {}'.format(grid_ids[0,-1]))
        print(tiles[grid_ids[0,-1]])
        print(unique_borders[grid_ids[0,-1]])
        
        print('bottom-left: {}'.format(grid_ids[-1,0]))
        print(tiles[grid_ids[-1,0]])
        print(unique_borders[grid_ids[-1,0]])
        
        print('bottom-right: {}'.format(grid_ids[-1,-1]))
        print(tiles[grid_ids[-1,-1]])
        print(unique_borders[grid_ids[-1,-1]])
        

def trim_borders(tile):
    return tile[1:-1,1:-1]


def compile_image(tile_id_grid, tiles):
    return np.concatenate(
        [
            np.concatenate(
                [trim_borders(tiles[tile_id_grid[i,j]]) for j in range(int(np.sqrt(N_TILES)))], 
                axis=1
            )
            for i in range(int(np.sqrt(N_TILES)))
        ],
        axis=0
    )


def is_sea_monster(image_part, pattern):
    return np.sum(pattern == '#') == np.sum(image_part == pattern)


def count_non_sea_monster_pixels(image, pattern):
    # number of configurations to try
    n_vertical = image.shape[0] - pattern.shape[0]
    n_horizontal = image.shape[1] - pattern.shape[1]
    
    pattern_points = np.sum(pattern == '#')
    
    sea_monster_count = 0
    for i in range(n_vertical):
        for j in range(n_horizontal):
            image_part = image[i: i + pattern.shape[0], j: j + pattern.shape[1]]
            if is_sea_monster(image_part, pattern):
                sea_monster_count += 1
                
    if sea_monster_count == 0:
        return 0
    
    return np.sum(image == '#') - sea_monster_count * pattern_points


def count_pixels_all_orientations(image, pattern):
    for image_to_try in [image, flip_tile(image)]:
        for rot in [0,1,2,3]:
            count = count_non_sea_monster_pixels(rotate_tile(image_to_try, rot), pattern)
            if count > 0:
                return count


if __name__ == '__main__':

    with open(IMAGE_TILES, 'r') as f:
        tiles = {
            int(line.split('\n')[0].strip('Tile ').strip(':')): np.array([list(x) for x in line.split('\n')[1:]])
            for line in f.read().strip().split("\n\n")
        }
    
    corner_tiles, edge_tiles, unique_borders = find_corner_and_edge_tiles(tiles)
        
    print('Part 1 Solution: {}'.format(
        product(corner_tiles)
    ))
    
    tile_id_grid = assemble_grid(tiles, corner_tiles, edge_tiles, unique_borders)
    image = compile_image(tile_id_grid, tiles)
    
    pattern = np.array([list(x) for x in SEA_MONSTER_PATTERN])
    count_pixels_all_orientations(image, pattern)
    
    print('Part 2 Solution: {}\n'.format(
        count_pixels_all_orientations(image, pattern)
    ))
