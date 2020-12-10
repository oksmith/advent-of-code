ADAPTERS = 'inputs/10_input.txt'

CHARGING_OUTLET_JOLTAGE = 0

FINAL_ADAPTER_DIFFERENCE = 3


def get_differences(adapters):
    joltage = 0
    differences = {1: 0, 3: 0}

    for x, y in zip(adapters[1:], adapters[:-1]):
        if x - y == 1:
            differences[1] += 1
        elif x - y == 3:
            differences[3] += 1
        else:
            raise ValueError('Consecutive adapters {} and {} are not '.format(x, y) + 
                             '1 or 3 apart!')
    
    return differences


def get_combinations(adapters):
    
    combinations_per_adapter = [0]*len(adapters)
    
    # Initialise a list containing the number of ways to reach the each adapter in the list
    # It will be a function of the number of ways of reaching earlier adapters, starting with 1 
    combinations_per_adapter[0] = 1

    for i, adapter in enumerate(adapters):
        for k in range(max(i-3, 0), i):
            if (adapter - adapters[k] <= 3):
                combinations_per_adapter[i] += combinations_per_adapter[k]

    print(combinations_per_adapter)
    
    # `combinations_per_adapter` now contains, for each adapter in the list, the number of ways of
    # reaching that adapter from the starting point 0.
    # To select the number of ways to reach the final device select the last element in the list
    return combinations_per_adapter[-1]


if __name__ == '__main__':

    with open(ADAPTERS, 'r') as f:
        adapters = sorted([int(line) for line in f.read().strip().split("\n")])
        
    # Starting point is always the charging outlet
    adapters.insert(0, CHARGING_OUTLET_JOLTAGE)
    adapters.append(max(adapters)+FINAL_ADAPTER_DIFFERENCE)

    differences = get_differences(adapters)

    print('Part 1 Solution: {}'.format(
        differences[1]*differences[3]
    ))
    
    n_combinations = get_combinations(adapters)
    
    print('Part 2 Solution: {}\n'.format(
        n_combinations
    ))
