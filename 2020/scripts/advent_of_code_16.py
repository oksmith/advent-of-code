import numpy as np


TICKET_DETAILS = 'inputs/16_input.txt'


def check_rule(field_num, ranges):
    return any([(int(field_num) <= int(max_v) and int(field_num) >= int(min_v)) for min_v, max_v in ranges])
        

def get_invalid_values(ticket, rules):
    invalid_values = []
    for field_num in ticket:
        if all([
            not check_rule(field_num, value) for value in rules.values()
        ]):
            invalid_values.append(int(field_num))
    
    return invalid_values



if __name__ == '__main__':
    
    with open(TICKET_DETAILS, 'r') as f:
        txt = f.read().strip().split('\n\n')
        rules_text, myticket_text, tickets_text = txt
        
    rules = {
        r.split(':')[0]: [tuple(x.split('-')) for x in r.split(':')[1].strip().split(' or ')] 
        for r in rules_text.split('\n')
    }
    myticket = myticket_text.split('\n')[1].split(',')
    tickets = [ticket.split(',') for ticket in tickets_text.split('\n')[1:]]
        
    invalid_values = []
    for ticket in tickets:
        invalid_values += get_invalid_values(ticket, rules)
     
    print('Part 1 Solution: {}'.format(
        sum(invalid_values)
    ))
    
    valid_tickets = [ticket for ticket in tickets if len(get_invalid_values(ticket, rules)) == 0]
    num_positions = len(valid_tickets[0])
    possible_positions = {key: [] for key in rules.keys()}
    decided_positions = {}

    for key, value in rules.items():
        for position in range(num_positions):
            if all([check_rule(ticket[position], value) for ticket in valid_tickets]):
                possible_positions[key].append(position)
    
    while len(decided_positions.keys()) != num_positions:
        for field in rules.keys():
            if len(possible_positions[field]) == 1:
                position = possible_positions[field][0]
                decided_positions[field] = position
                for field in rules.keys():
                    # Remove position from the other fields' possibilities 
                    possible_positions[field] = [
                        x for x in possible_positions[field] if x != position
                    ]
    
    print('Part 2 Solution: {}\n'.format(
        np.product([
            int(myticket[decided_positions[key]]) for key in decided_positions.keys() 
            if key.startswith('departure')
        ])
    ))
