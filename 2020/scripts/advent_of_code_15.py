STARTING_NUMBERS = [2,20,0,4,1,17]

def get_last_number_spoken(numbers, target_round_number):
    last_round_spoken = {}

    for round_num in range(1, target_round_number+1, 1):
        if round_num - 1 < len(numbers):
            last_number_spoken = numbers[round_num-1]
            last_round_spoken[numbers[round_num-1]] = {'last': round_num, 'previous': None}
        else:
            if last_number_spoken not in last_round_spoken.keys():
                last_round_spoken[last_number_spoken] = {'last': round_num, 'previous': None}
                last_number_spoken = 0
            elif last_round_spoken[last_number_spoken]['previous'] is None:
                last_number_spoken = 0
                last_round_spoken[last_number_spoken]['previous'] = last_round_spoken[last_number_spoken]['last']
                last_round_spoken[last_number_spoken]['last'] = round_num

            else:
                diff = last_round_spoken[last_number_spoken]['last'] - last_round_spoken[last_number_spoken]['previous']
                last_number_spoken = diff

                if last_number_spoken not in last_round_spoken.keys():
                    last_round_spoken[last_number_spoken] = {'last': round_num, 'previous': None}
                else:
                    last_round_spoken[last_number_spoken]['previous'] = last_round_spoken[last_number_spoken]['last']
                    last_round_spoken[last_number_spoken]['last'] = round_num

        round_num += 1
        
        
    return last_number_spoken


if __name__ == '__main__':
     
    print('Part 1 Solution: {}'.format(
        get_last_number_spoken(STARTING_NUMBERS, 2020)
    ))
    
    
    
    print('Part 2 Solution: {}\n'.format(
        get_last_number_spoken(STARTING_NUMBERS, 30000000)
    ))
