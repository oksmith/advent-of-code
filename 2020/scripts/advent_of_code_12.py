import math


INSTRUCTIONS = 'inputs/12_input.txt'


def apply_rule(position, rule):
    if rule[0] == 'N':
        position.update({'y': position['y']+rule[1]})
    elif rule[0] == 'E':
        position.update({'x': position['x']+rule[1]})
    elif rule[0] == 'S':
        position.update({'y': position['y']-rule[1]})
    elif rule[0] == 'W':
        position.update({'x': position['x']-rule[1]})
    elif rule[0] == 'R':
        position.update({'rot': (position['rot']+rule[1]) % 360})
    elif rule[0] == 'L':
        position.update({'rot': (position['rot']-rule[1]) % 360})
    elif rule[0] == 'F':
        if position['rot'] not in [0, 90, 180, 270]:
            raise ValueError('`rot` encountered an invalid value: {}'.format(position['rot']))
            
        direction = 'E' if position['rot'] == 0 else (
            'S' if position['rot'] == 90 else (
                'W' if position['rot'] == 180 else 'N'
            )
        )
        
        apply_rule(position, (direction, rule[1]))
    else:
        raise ValueError('Invalud rule type: {}'.format(rule[0]))
    
    return position


def rotate(point, angle):
    """
    Rotate a point counterclockwise by a given angle around an origin of (0, 0).
    """
    px, py = point

    qx = math.cos(math.radians(angle)) * px + math.sin(math.radians(angle)) * py
    qy = -math.sin(math.radians(angle)) * px + math.cos(math.radians(angle)) * py
    return qx, qy

def apply_rule_v2(position, waypoint_position, rule):
    if rule[0] == 'N':
        waypoint_position.update({'y': waypoint_position['y']+rule[1]})
    elif rule[0] == 'E':
        waypoint_position.update({'x': waypoint_position['x']+rule[1]})
    elif rule[0] == 'S':
        waypoint_position.update({'y': waypoint_position['y']-rule[1]})
    elif rule[0] == 'W':
        waypoint_position.update({'x': waypoint_position['x']-rule[1]})
    elif rule[0] == 'R':
        waypoint_position['x'], waypoint_position['y'] = \
            rotate((waypoint_position['x'], waypoint_position['y']), rule[1])
    elif rule[0] == 'L':
        waypoint_position['x'], waypoint_position['y'] = \
            rotate((waypoint_position['x'], waypoint_position['y']), -rule[1])
    elif rule[0] == 'F':
        position.update({
            'x': position['x'] + rule[1]*waypoint_position['x'],
            'y': position['y'] + rule[1]*waypoint_position['y']
        })
    else:
        raise ValueError('Invalud rule type: {}'.format(rule[0]))
    
    return position


if __name__ == '__main__':

    with open(INSTRUCTIONS, 'r') as f:
        instructions = {i: (line[0], int(line[1:])) for i, line in enumerate(f.read().strip().split("\n"))}
       
    n_rules = len(instructions.keys())
    position = {'x': 0, 'y': 0, 'rot': 0}
    
    for i in range(n_rules):
        apply_rule(position, instructions[i])

    print('Part 1 Solution: {}'.format(
        abs(position['x']) + abs(position['y'])
    ))
    
    position = {'x': 0, 'y': 0}
    waypoint_position = {'x': 10, 'y': 1}
    
    for i in range(n_rules):
        apply_rule_v2(position, waypoint_position, instructions[i])

    print('Part 2 Solution: {}\n'.format(
        round(abs(position['x']) + abs(position['y']))
    ))
