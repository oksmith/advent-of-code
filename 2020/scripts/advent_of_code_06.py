QUESTIONNAIRES = 'inputs/06_input.txt'


def calculate_questionnaire_results(answers, set_operation):
    overlapping_characters = set_operation(*[set(line) for line in answers])
    return len(overlapping_characters)


if __name__ == '__main__':

    with open(QUESTIONNAIRES, 'r') as f:
        groups = [line for line in f.read().strip().split("\n\n")]

    questionnaires = [group.split('\n') for group in groups]

    n_answers_any = [
        calculate_questionnaire_results(answers, set_operation=set.union) 
        for answers in questionnaires
    ]

    n_answers_all = [
        calculate_questionnaire_results(answers, set_operation=set.intersection) 
        for answers in questionnaires
    ]
    
    print('Part 1 Solution: {}'.format(
        sum(n_answers_any)
    ))
    
    print('Part 2 Solution: {}\n'.format(
        sum(n_answers_all)
    ))
