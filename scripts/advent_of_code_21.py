import itertools
from collections import Counter

INGREDIENTS = 'inputs/21_input.txt'


def get_allergen_mapping(lines):
    unique_ingredients = list(set(itertools.chain.from_iterable([line[0] for line in lines])))
    unique_allergens = list(set(itertools.chain.from_iterable([line[1] for line in lines])))
    
    allergens_dict = {}
    
    counter_dict = {allergen: Counter() for allergen in unique_allergens}
    appearance_dict = {allergen: 0 for allergen in unique_allergens}
    ingredient_counter = {ingredient: 0 for ingredient in unique_ingredients}
    
    for line in lines:
        for allergen in line[1]:
            counter_dict[allergen].update(line[0])
            appearance_dict[allergen] += 1
        for ingredient in line[0]:
            ingredient_counter[ingredient] += 1
            
    while len(unique_allergens) > 0:
        for allergen in unique_allergens:
            present_every_time = [
                x for x in counter_dict[allergen].keys() 
                if counter_dict[allergen][x] == appearance_dict[allergen]
            ]
            if len(present_every_time) == 1:
                ingredient = present_every_time[0]
                allergens_dict[allergen] = ingredient
                unique_allergens = [x for x in unique_allergens if x != allergen]
                for allergen in unique_allergens:
                    del counter_dict[allergen][ingredient]
                    
    ingredients_without_allergens = [x for x in unique_ingredients if x not in allergens_dict.values()]
    non_allergen_ingredient_count = sum([
        ingredient_counter[ingredient] for ingredient in ingredients_without_allergens
    ])
            
    return allergens_dict, non_allergen_ingredient_count


if __name__ == '__main__':

    with open(INGREDIENTS, 'r') as f:
        lines = [
            (line.split('contains')[0].strip('() ').split(), line.split('contains')[1].strip('() ').split(', '))  
            for line in f.read().strip().split("\n")
        ]
    
        
    allergens_dict, non_allergen_ingredient_count = get_allergen_mapping(lines)
    
    print('Part 1 Solution: {}'.format(
        non_allergen_ingredient_count
    ))

    print('Part 2 Solution: {}\n'.format(
        ','.join([allergens_dict[k] for k in sorted(allergens_dict.keys())])
    ))
