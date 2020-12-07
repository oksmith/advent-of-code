import re

BAGGAGE_RULES = 'inputs/07_input.txt'


def get_containing_bags(bag, bag_rules_parsed):
        
    bag_set = set([bag])
    checked = set()

    while bag_set != checked:
        for b in bag_set - checked:
            bag_set = bag_set.union(
                set([
                    bigbag for bigbag in bag_rules_parsed.keys() 
                    if b in [val['type'] for val in bag_rules_parsed[bigbag]]
                ]
            ))
            checked.add(b)
        
    return bag_set - set([bag])


def get_number_of_bags_inside(bag, bag_rules_parsed):
    n_bags = 0
    if len(bag_rules_parsed[bag]) == 1 and bag_rules_parsed[bag][0]['num'] == 0:
        # reached one of the endpoints where no other bags are contained 
        print('   get_number_of_bags_inside: Reached endpoint: {}'.format(bag))
        return 0

    for smallbag in bag_rules_parsed[bag]:
        n_bags += smallbag['num'] * (1 + get_number_of_bags_inside(smallbag['type'], bag_rules_parsed))
        
    return n_bags


if __name__ == '__main__':

    with open(BAGGAGE_RULES, 'r') as f:
        rules = [line for line in f.read().strip().split("\n")]

    bag_rules = {
        line.split('bags contain')[0].strip(): line.split('bags contain')[1]\
            .replace(' bags', '')\
            .replace(' bag', '')\
            .replace('no other', '0 other')\
            .strip(' .')\
            .split(', ')
        for line in rules
    }

    bag_rules_parsed = {
        key: [{'num': int(re.match('\d+', v)[0]), 'type': re.sub('\d+ ', '', v)} for v in val] 
        for key, val in bag_rules.items()
    }

    print('Part 1 Solution: {}'.format(
        len(get_containing_bags('shiny gold', bag_rules_parsed))
    ))
    
    print('Part 2 Solution: {}\n'.format(
        get_number_of_bags_inside('shiny gold', bag_rules_parsed)
    ))
