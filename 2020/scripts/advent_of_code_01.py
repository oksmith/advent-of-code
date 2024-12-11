import itertools

EXPENSE_REPORT_INPUT = 'inputs/01_input.txt'


if __name__ == '__main__':
    with open(EXPENSE_REPORT_INPUT, 'r') as f:
        entries = [int(line) for line in f.readlines()]
        
    solutions_1 = [entry*(2020-entry) for entry in entries if 2020-entry in entries and entry >= 2020-entry]
    
    print('Part 1 Solution: {}'.format(solutions_1[0]))
    if len(solutions_1) > 1:
        print('WARNING! More than 1 solution: {}.'.format(solutions_1))
    
    
    solutions_2 = [
        entry1*entry2*(2020-entry1-entry2) for entry1, entry2 in itertools.product(entries, entries) 
        if 2020-entry1-entry2 in entries and entry1 >= entry2 and entry2 >= (2020-entry1-entry2)
    ]
    
    print('Part 2 Solution: {}\n'.format(solutions_2[0]))
    if len(solutions_2) > 1:
        print('WARNING! More than 1 solution: {}.'.format(solutions_2))
