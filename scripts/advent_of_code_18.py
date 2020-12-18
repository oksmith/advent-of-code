import re
import numpy as np


ARITHMETIC_QUESTIONS = 'inputs/18_input.txt'


def simple_evaluation(expression):
    iterator = expression.split(' ')
    result = int(iterator.pop(0))
    while len(iterator) > 0:
        op = iterator.pop(0)
        num = int(iterator.pop(0))
        if op == '+':
            result = result + num
        elif op == '*':
            result = result * num
            
    return result


def weird_evaluation(expression):
    iterator = expression.split(' * ')
    iterator = [int(x) if len(x.split(' + ')) == 1 else sum([int(y) for y in x.split(' + ')]) for x in iterator]
    return np.prod(iterator)


def evaluate_expression(expression, inner_function=simple_evaluation):
    
    parentheses = find_parentheses(expression)
    
    while len(parentheses) > 0:
        for parenthesis in parentheses:
            expression = expression.replace(
                parenthesis, 
                str(evaluate_expression(parenthesis.strip('()'), inner_function=inner_function))
            )
            
        parentheses = find_parentheses(expression)
    
    
    return inner_function(expression)


def find_parentheses(expression):
    return re.findall('\([\d+* \d]*\)', expression)


if __name__ == '__main__':

    with open(ARITHMETIC_QUESTIONS, 'r') as f:
        questions = [line for line in f.read().strip().split("\n")]

    print('Part 1 Solution: {}'.format(
        sum([evaluate_expression(question, inner_function=simple_evaluation) for question in questions])
    ))
    
    print('Part 2 Solution: {}\n'.format(
        sum([evaluate_expression(question, inner_function=weird_evaluation) for question in questions])
    ))
