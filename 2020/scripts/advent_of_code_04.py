import string
import re

PASSPORTS = 'inputs/04_input.txt'

REQUIRED_FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

OPTIONAL_FIELDS = ['cid']


def get_number_of_valid_passports(passport_dicts, validate_fields=False):
    valid_passports = 0

    for passport in passport_dicts:
        if all([field in passport.keys() for field in REQUIRED_FIELDS]):
            if not validate_fields:
                valid_passports += 1
            else:
                valid_passports += int(_validate_fields(passport))

    return valid_passports


def _validate_fields(passport):
    """
    There's almost definitely a more elegant way of doing this, eg. using lambda functions.
    """
    valid = True
    
    if len(passport['byr']) != 4 or int(passport['byr']) < 1920 or int(passport['byr']) > 2002:
        valid = False 
        
    elif len(passport['iyr']) != 4 or int(passport['iyr']) < 2010 or int(passport['iyr']) > 2020:
        valid = False 
        
    elif len(passport['eyr']) != 4 or int(passport['eyr']) < 2020 or int(passport['eyr']) > 2030:
        valid = False
        
    elif not (
        (
            passport['hgt'][-2:] == 'cm' and int(passport['hgt'][:-2]) >= 150 and int(passport['hgt'][:-2]) <= 193
        ) or (
            passport['hgt'][-2:] == 'in' and int(passport['hgt'][:-2]) >= 59 and int(passport['hgt'][:-2]) <= 76
        )
    ):
        valid = False 
        
    elif not re.fullmatch('^#[a-f0-9]{6}$', passport['hcl']):
        valid = False
        
    elif passport['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        valid = False
        
    elif len(passport['pid']) != 9 or not passport['pid'].isdigit():
        valid = False
        
    else:
        pass
    
    return valid


if __name__ == '__main__':

    with open(PASSPORTS, 'r') as f:
        lines = [str(line).strip('\n').strip() for line in f.readlines()]

    # Parse passports data until it consists of a list of dictionaries 
    passports_oneline = ' '.join([line if line != '' else '\n' for line in lines])
    passports = [line.strip().split(' ') for line in passports_oneline.split('\n')]
    passport_dicts = [
        {
            entry.split(':')[0]: entry.split(':')[1]
            for entry in passport
        } for passport in passports
    ]
    
    print('Part 1 Solution: {}'.format(
        get_number_of_valid_passports(passport_dicts)
    ))
    print('Part 2 Solution: {}\n'.format(
        get_number_of_valid_passports(passport_dicts, validate_fields=True)
    ))
