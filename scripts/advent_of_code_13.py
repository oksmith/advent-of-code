"""
Implementation of Chinese Remainder Theorem uses code snippet from this blog (code slightly 
amended due to a bug fix): 
https://fangya.medium.com/chinese-remainder-theorem-with-python-a483de81fbb8
"""

from functools import reduce


BUS_TIMES = 'inputs/13_input.txt'


def chinese_remainder(n, a):
    sum=0
    prod=reduce(lambda a, b: a*b, n)
    
    for n_i, a_i in zip(n,a):
        p=prod//n_i
        sum += a_i* mul_inv(p, n_i)*p
        
    return sum % prod


def mul_inv(a, b):
    b0= b
    x0, x1= 0,1
    if b== 1: 
        return 1
    
    while a>1:
        q=a// b
        a, b= b, a%b
        x0, x1=x1 -q *x0, x0
        
    if x1<0: 
        x1+= b0
        
    return x1


if __name__ == '__main__':

    with open(BUS_TIMES, 'r') as f:
        data = f.read().strip().split("\n")
        current_timestamp = int(data[0])
        bus_frequencies = data[1]
        
    available_buses = sorted([int(x) for x in bus_frequencies.replace(',x', '').split(',')])
    
    next_bus_time = {}
    for bus in available_buses:
        next_bus_time[bus] = current_timestamp + bus - (current_timestamp % bus)
        
    wait_time = min(next_bus_time.values()) - current_timestamp
    bus_id = [x for x in next_bus_time.keys() if next_bus_time[x] == min(next_bus_time.values())][0]

    print('Part 1 Solution: {}'.format(
        wait_time * bus_id
    ))
    
    
    """
    Part 2:
    
    Solve for x: 
    x = 0 mod 23
    x + 13 = 0 mod 41
    x + 23 = 0 mod 733 
    x + 36 = 0 mod 13
    ...
    
    equivalently
    x = 0 mod 23
    x = 41-13 mod 41
    x = 733-23 mod 733
    ...
    
    This is a system of equations similar to what's seen in the Chinese Remainder Theorem.
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    which can be solved using Euclid's algorithm.
    """
    minute_of_departure = {int(bus_id): time for time, bus_id in enumerate(bus_frequencies.split(',')) if bus_id != 'x'}
    bus_ids = list(minute_of_departure.keys())
    minutes = [x - minute_of_departure[x] % x for x in bus_ids]
    
    print('Part 2 Solution: {}\n'.format(
        chinese_remainder(bus_ids, minutes)
    ))
