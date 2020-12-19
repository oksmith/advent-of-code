import itertools
from collections import Counter


MESSAGES = 'inputs/19_input.txt'

REPLACE_DICT = {
    '8: 42': '8: 42 | 42 8'
    '11: 42 31': '11: 42 31 | 42 11 31'  
}


def get_match_possibilities(rules, rule_num=0):
    match_possibilities = []
    matchstr = rules[str(rule_num)]
    
    if '|' in matchstr:
        for option in matchstr.split(' | '):
            poss_product = itertools.product(
                *[get_match_possibilities(rules, m) for m in option.split(' ')]
            )
            _ = [match_possibilities.append(''.join(x)) for x in poss_product]

    elif matchstr.replace(' ', '').isnumeric():
        # then the matchstr is something like '2 3'
        poss_product = itertools.product(
            *[get_match_possibilities(rules, m) for m in matchstr.split(' ')]
        )
        _ = [match_possibilities.append(''.join(x)) for x in poss_product]
        
    else:
        # then the matchstr is "a" or "b"
        match_possibilities.append(matchstr.strip('"'))
        
    return match_possibilities 


def message_match(message, rules, rule_num=0):
    match_possibilities = get_match_possibilities(rules, rule_num=rule_num)
    return message in match_possibilities


if __name__ == '__main__':

    with open(MESSAGES, 'r') as f:
        data = f.read().strip().split("\n\n")
        rules = {x.split(': ')[0]: x.split(': ')[1] for x in data[0].split('\n')}
        rules = {int(k): v.strip('"').split('|') for k, v in rules.items()}
        messages = data[1].split('\n')

    print('Part 1 Solution: {}'.format(
        Counter([message_match(x, rules, rule_num=0) for x in messages])[True]
    ))
    
    rules = data[0].split('\n').replace(REPLACE_DICT)
    rules = {x.split(': ')[0]: x.split(': ')[1] for x in rules}
    rules = {int(k): v.strip('"').split('|') for k, v in rules.items()}
    
    print('Part 2 Solution: {}\n'.format(
        None
    ))
