import pandas as pd

PASSWORDS_AND_POLICIES = 'inputs/02_input.txt'

def validate_password(string, contain_substr, not_contain_substr):
    return contain_substr in string and not_contain_substr not in string


def validate_password_new_policy(string, character, position_1, position_2):
    return (string[position_1] == character or string[position_2] == character) and string[position_1] != string[position_2]


if __name__ == '__main__':

    with open(PASSWORDS_AND_POLICIES, 'r') as f:

        df = pd.DataFrame(
            [
                # String formatting 
                [
                    line.split(" ")[1].strip(":"),
                    int(line.split(" ")[0].split('-')[0]), 
                    int(line.split(" ")[0].split('-')[1]), 
                    line.split(" ")[2].strip('\n')
                ] for line in f.readlines()
            ], 
            columns=['character', 'min', 'max', 'password']
        )
        
    df['sorted_password'] = df['password'].apply(lambda x: ''.join(sorted(x)))
    df['must_contain'] = df['character']*df['min']
    df['must_not_contain'] = df['character']*(df['max']+1)

    df['valid'] = df.apply(lambda x: validate_password(x.sorted_password, x.must_contain, x.must_not_contain), axis=1)
    
    print('Part 1 Solution: {}'.format(df['valid'].sum()))
    
    
    # Now we find out the password policy is different
    df = df[['character', 'min', 'max', 'password']].rename(columns={'min': 'position_1', 'max': 'position_2'})
    
    df['valid'] = df.apply(lambda x: validate_password_new_policy(x.password, x.character, x.position_1-1, x.position_2-1), axis=1)
    
    print('Part 2 Solution: {}'.format(df['valid'].sum()))
