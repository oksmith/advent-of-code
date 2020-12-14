import copy
import math

INITIALIZATION_PROGRAM = 'inputs/14_input.txt'

NUMBER_OF_BITS = 36


def binary_string(x, n=NUMBER_OF_BITS):
    return format(x, 'b').zfill(n)


def bit_mask(mem, mask, mem_loc, val):
    
    binary_val = binary_string(val)
    
    for i, char in enumerate(mask):
        if char != 'X':
            binary_val = binary_val[:i] + char + binary_val[i+1:]
            
    new_val = int(binary_val, 2)

    mem[mem_loc] = new_val
    
    
def bit_mask_v2(mem, mask, mem_loc, val):
    
    binary_mem_loc = binary_string(mem_loc)
    
    for i, char in enumerate(mask):
        if char == '0':
            pass
        elif char in ('1', 'X'):
            binary_mem_loc = binary_mem_loc[:i] + char + binary_mem_loc[i+1:]
        else:
            raise ValueError('Unrecognised mask character: {}, '.format(char) + 
                            'must be in ("0", "1", "X")!')
    
    floating_points = [pos for pos, char in enumerate(binary_mem_loc) if char == 'X']  
    
    # There are 2^(len(floating_points)) possibilities. Loop through them all 
    mem_loc_possibilities = []
    for i in range(int(math.pow(2, len(floating_points)))):
        i_bin = binary_string(i, n=len(floating_points))
        possible_loc = copy.deepcopy(binary_mem_loc)
        for j, pos in enumerate(floating_points):
            possible_loc = possible_loc[:pos] + i_bin[j] + possible_loc[pos+1:]
        mem_loc_possibilities.append(possible_loc)
            
    for mem_loc in mem_loc_possibilities:
        mem[mem_loc] = val
    
    
def get_memory_after_initialization(lines, bit_mask_func):
    mem = {}
    for line in lines:
        if line.split(' = ')[0] == 'mask':
            mask = line.split(' = ')[1]
        else:
            mem_loc = int(line.split(' = ')[0].replace('mem[', '').replace(']', ''))
            val = int(line.split(' = ')[1])
            
            bit_mask_func(mem, mask, mem_loc, val)
            
    return mem


if __name__ == '__main__':

    with open(INITIALIZATION_PROGRAM, 'r') as f:
        lines = f.read().strip().split('\n')
        
    mem = get_memory_after_initialization(lines, bit_mask_func=bit_mask)
     
    print('Part 1 Solution: {}'.format(
        sum(mem.values())
    ))
    
    mem = get_memory_after_initialization(lines, bit_mask_func=bit_mask_v2)
    
    print('Part 2 Solution: {}\n'.format(
        sum(mem.values())
    ))
