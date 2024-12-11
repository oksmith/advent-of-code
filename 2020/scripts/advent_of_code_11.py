import itertools
import copy
import numpy as np

from collections import Counter


INITIAL_FLOOR_PLAN = 'inputs/11_input.txt'


def pad_with(vector, pad_width, iaxis, kwargs):
    """
    String padder utility function.
    https://stackoverflow.com/questions/49049852/numpy-string-array-pad-with-string
    """
    pad_value = kwargs.get('padder', '?')
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector


def pad_floor_plan(floor_plan):
    return np.pad(np.array(floor_plan), 1, pad_with, padder='.')


def count_adjacent_occupied_seats(padded_floor_plan, row_num, col_num):
    seat_grid_indices = [
        (i, j) for i, j in itertools.product(range(row_num-1, row_num+2), range(col_num-1, col_num+2))  
        if (i, j) != (row_num, col_num)
    ]
    counts = Counter([padded_floor_plan[i, j] for i, j in seat_grid_indices])
    return counts['#'] 

def count_visible_occupied_seats(padded_floor_plan, row_num, col_num):
    n_col = len(seats.padded_floor_plan[0])
    n_row = len(seats.padded_floor_plan)
    
    horizontal_r = min([i for i in range(1, n_row-row_num) if padded_floor_plan[row_num+i, col_num] != '.'], default=1)
    horizontal_l = min([i for i in range(1, row_num) if padded_floor_plan[row_num-i, col_num] != '.'], default=1)
    vertical_d = min([i for i in range(1, n_col-col_num) if padded_floor_plan[row_num, col_num+i] != '.'], default=1)
    vertical_u = min([i for i in range(1, col_num) if padded_floor_plan[row_num, col_num-i] != '.'], default=1)
    diagonal_rd = min([i for i in range(1, min(n_row-row_num, n_col-col_num)) if padded_floor_plan[row_num+i, col_num+i] != '.'], default=1)
    diagonal_ld = min([i for i in range(1, min(row_num, n_col-col_num)) if padded_floor_plan[row_num-i, col_num+i] != '.'], default=1)
    diagonal_lu = min([i for i in range(1, min(row_num, col_num)) if padded_floor_plan[row_num-i, col_num-i] != '.'], default=1)
    diagonal_ru = min([i for i in range(1, min(n_row-row_num, col_num)) if padded_floor_plan[row_num+i, col_num-i] != '.'], default=1)
    
#     print(horizontal_r)
#     print(horizontal_l)
#     print(vertical_d)
#     print(vertical_u)
#     print(diagonal_rd)
#     print(diagonal_ld)
#     print(diagonal_lu)
#     print(diagonal_ru)
    
    seat_grid_indices = [(row_num, col_num+vertical_d), (row_num, col_num-vertical_u), (row_num-horizontal_l, col_num),
                        (row_num+horizontal_r, col_num), (row_num+diagonal_rd, col_num+diagonal_rd), 
                         (row_num-diagonal_ld, col_num+diagonal_ld),  (row_num-diagonal_lu, col_num-diagonal_lu), 
                         (row_num+diagonal_ru, col_num-diagonal_ru)
                        ]
#     print(seat_grid_indices)
    counts = Counter([padded_floor_plan[i, j] for i, j in seat_grid_indices])
    return counts['#'] 


class SeatingSystem(object):
    def __init__(self, initial_floor_plan):
        self.initial_floor_plan = np.array(initial_floor_plan)
        self.padded_floor_plan = pad_floor_plan(self.initial_floor_plan)
        self.round = 0 
        self.equilibrium = False
        
    def apply_rules(self, unoccupy_threshold=4, occupied_seats_counter=count_adjacent_occupied_seats):
        
        new_floor_plan = copy.deepcopy(self.padded_floor_plan)
        
        for row_num, row in enumerate(self.padded_floor_plan):
            for col_num, seat in enumerate(row):
                if seat == '.':
                    pass
                
                elif seat == 'L':
                    # if NO adjacent seats, then it becomes occupied
                    n = occupied_seats_counter(self.padded_floor_plan, row_num, col_num)
                    if n == 0:
                        new_floor_plan[row_num, col_num] = '#'
                    
                else:
                    # if 4 or more adjacent seats, then it becomes unoccupied
                    n = occupied_seats_counter(self.padded_floor_plan, row_num, col_num)
                    if n >= unoccupy_threshold:
                        new_floor_plan[row_num, col_num] = 'L'
        
        if np.array_equal(new_floor_plan, self.padded_floor_plan):
            self.equilibrium = True
        
        self.padded_floor_plan = new_floor_plan
        self.round += 1
        
    def find_equilibrium_arrangement(self, **kwargs):
        while not self.equilibrium:
            self.apply_rules(**kwargs)
        
    def number_of_occupied_seats(self):
        return np.sum(self.padded_floor_plan == '#')  
        

if __name__ == '__main__':

    with open(INITIAL_FLOOR_PLAN, 'r') as f:
        floor_plan = [list(line) for line in f.read().strip().split("\n")]
        
    seats = SeatingSystem(initial_floor_plan=floor_plan)
    seats.find_equilibrium_arrangement()
    
    print('Part 1 Solution: {}'.format(
        seats.number_of_occupied_seats()
    ))
    
    # re-initialise seating system object 
    seats = SeatingSystem(initial_floor_plan=floor_plan)
    seats.find_equilibrium_arrangement(unoccupy_threshold=5, occupied_seats_counter=count_visible_occupied_seats)
    
    print('Part 2 Solution: {}\n'.format(
        seats.number_of_occupied_seats()
    ))
