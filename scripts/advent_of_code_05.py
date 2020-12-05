BOARDING_PASSES = 'inputs/05_input.txt'


def get_seat_id(boarding_pass_id):
    
    row_binary = boarding_pass_id[:7].replace('F', '0').replace('B', '1')
    col_binary = boarding_pass_id[7:].replace('L', '0').replace('R', '1')
    
    row_num = int(row_binary, 2)
    col_num = int(col_binary, 2)

    return {'row_num': row_num, 'col_num': col_num, 'seat_id': 8*row_num + col_num}


if __name__ == '__main__':

    with open(BOARDING_PASSES, 'r') as f:
        lines = [str(line).strip('\n').strip() for line in f.readlines()]

    seat_ids = [get_seat_id(boarding_pass_id)['seat_id'] for boarding_pass_id in lines]
    
    print('Part 1 Solution: {}'.format(
        max(seat_ids)
    ))
    
    missing_seat_ids = [x for x in range(min(seat_ids), max(seat_ids)+1) if x not in seat_ids]
    if len(missing_seat_ids) > 1:
        print('WARNING! More than 1 solution: {}.'.format(missing_seat_ids))
        
    print('Part 2 Solution: {}\n'.format(
        missing_seat_ids[0]
    ))
