import itertools
from collections import Counter


MESSAGES = 'inputs/19_input.txt'

REPLACE_DICT = {
    '8: 42': '8: 42 | 42 8',
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

def message_match(message, matcher_list, rules, rule_num=0):
    if len(matcher_list) == 0 or len(message) == 0:
        # No more characters in the message to match, or no more rules in the matcher list 
        return len(matcher_list) == len(message)
    
    else:
        char = matcher_list.pop()
        if char in ['a', 'b']:
            if message[0] == char:
                return message_match(message[1:], matcher_list.copy(), rules)
        else:
            # char is an integer representing a rule 
            for rule in rules[char]:
                if message_match(message, matcher_list + list(reversed(rule)), rules):
                    return True
        return False


if __name__ == '__main__':

    with open(MESSAGES, 'r') as f:
        data = f.read().strip().split("\n\n")
        rules = {x.split(': ')[0]: x.split(': ')[1] for x in data[0].split('\n')}
        rules = {int(k): v.strip('"') if v in ['"a"', '"b"'] 
                     else [[int(u) for u in t.strip().split(' ')] for t in v.split('|')]
                 for k, v in rules.items()}
        messages = data[1].split('\n')

    print('Part 1 Solution: {}'.format(
        Counter([message_match(x, list(reversed(rules[0][0])), rules, rule_num=0) for x in messages])[True]
    ))
    
    rules = data[0]
    for k, v in REPLACE_DICT.items():
        rules = rules.replace(k, v)
    
    rules = rules.split('\n')
    rules = {x.split(': ')[0]: x.split(': ')[1] for x in rules}
    rules = {int(k): v.strip('"') if v in ['"a"', '"b"'] 
                     else [[int(u) for u in t.strip().split(' ')] for t in v.split('|')]
                 for k, v in rules.items()}
    
    print('Part 2 Solution: {}\n'.format(
        Counter([message_match(x, list(reversed(rules[0][0])), rules, rule_num=0) for x in messages])[True]
    ))
