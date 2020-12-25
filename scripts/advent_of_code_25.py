PUBLIC_KEYS = 'inputs/25_input.txt'


def transform_subject_number(subject_number, loop_size, init_value=1):
    value = init_value
    for _ in range(loop_size):
        value *= subject_number
        value = value % 20201227
        
    return value


def determine_loop_size(public_key):
    trial_loop_size = 1
    trial_key = transform_subject_number(7, 1, init_value=1)
    
    while trial_key != public_key:
        trial_key = transform_subject_number(7, 1, init_value=trial_key)
        trial_loop_size += 1
    
    return trial_loop_size 


if __name__ == '__main__':

    with open(PUBLIC_KEYS, 'r') as f:
        door_public_key, card_public_key = [int(x) for x in f.read().strip().split('\n')]
        
    card_loop_size = determine_loop_size(card_public_key)
    door_loop_size = determine_loop_size(door_public_key)
    
    encryption_key = transform_subject_number(door_public_key, card_loop_size)

    print('Part 1 Solution: {}'.format(
        encryption_key
    ))
   
    print('Part 2 Solution: {}\n'.format(
        None
    ))
