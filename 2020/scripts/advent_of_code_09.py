import itertools


NUMBERS = 'inputs/09_input.txt'

N_CONSECUTIVE = 25


def check(num, seq, n_terms=2):
    """
    Checks if `num` can be the sum of `n_terms` numbers in `seq`.
    """
    for x in itertools.product(*[seq]*n_terms):
        if sum(x) == num:
            return x
        
    return None


def check_consecutive(num, seq, n_terms=2):
    """
    Checks if `num` can be the sum of `n_terms` consecutive numbers in `seq`.
    """
    for i in range(len(seq)-n_terms+1):
        if sum(seq[i:i+n_terms]) == num:
            return seq[i:i+n_terms]
    
    return None
    

def find_encryption_weakness_list(num, seq):
    """
    Finds a list of numbers in `seq` which sum to make `num`.
    """
    for n_terms in range(2,len(seq)+1,1):
        can_be_made_list = check_consecutive(num, seq, n_terms=n_terms)
        if can_be_made_list:
            return can_be_made_list
        
    return None


if __name__ == '__main__':

    with open(NUMBERS, 'r') as f:
        numbers = [int(line) for line in f.read().strip().split("\n")]
        
        
    i = 0
    cannot_be_made = []

    while len(cannot_be_made) == 0:

        test_seq = numbers[i:i+N_CONSECUTIVE]
        test_num = numbers[i+N_CONSECUTIVE]

        can_be_made_list = check(test_num, test_seq)

        if can_be_made_list:
            i += 1
            if i >= len(numbers)-N_CONSECUTIVE:
                print('Cannot form another sequence of numbers! All can be made into a sum.')
                break
        else:
            cannot_be_made.append({'position': i+N_CONSECUTIVE, 'number': numbers[i+N_CONSECUTIVE]})
            break
    

    print('Part 1 Solution: {}'.format(
        cannot_be_made[0]['number']
    ))
    
    encryption_weakness_list = find_encryption_weakness_list(cannot_be_made[0]['number'], numbers[:cannot_be_made[0]['position']])
    
    print('Part 2 Solution: {}\n'.format(
        min(encryption_weakness_list) + 
        max(encryption_weakness_list)
    ))
