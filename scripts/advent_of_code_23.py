import copy
from collections import deque


INITIAL_CUP_ORDER = 598162734


class CrabCups(object):
    def __init__(self, inital_cup_order, number_of_cups=None):
        self.cups = deque(map(int, str(inital_cup_order)))
        self.current_cup = 0
        self.current_cup_value = self.cups[self.current_cup]
        
        if number_of_cups:
            if len(self.cups) < number_of_cups:
                self.cups = self.cups + deque([x for x in range(max(self.cups)+1, number_of_cups+1)])
                assert len(self.cups) == number_of_cups
        
        self.num_cups = len(self.cups)
        self.lowest_cup_value = min(self.cups)
        self.highest_cup_value = max(self.cups)

    def do_round(self):
#         print('cups: ', self.cups)
#         print('current cup: ', self.current_cup_value)
        
        pickup_index = [
            (self.current_cup+1) % self.num_cups,
            (self.current_cup+2) % self.num_cups,
            (self.current_cup+3) % self.num_cups
        ]

        pickup_cups = [self.cups[i] for i in pickup_index]
        for i in pickup_cups:
            del self.cups[self.cups.index(i)]
        
#         print('pickup: ', pickup_cups)
        
        destination_cup, destination_cup_value = self.get_destination_cup(pickup_cups)
#         print('destination: ', destination_cup_value)
        
        for i, p in enumerate(pickup_cups):
            self.cups.insert(destination_cup+1+i, p)
        
        # shuffle so that the current cup is in the same position as last time
        while self.cups[self.current_cup] != self.current_cup_value:
            self.cups.rotate(1)
        
        self.current_cup = (self.current_cup + 1) % self.num_cups
        self.current_cup_value = self.cups[self.current_cup]
        if self.current_cup == self.num_cups:
            self.current_cup = 0
    
    def get_destination_cup(self, pickup_cups):
        destination_cup_value = self.current_cup_value-1
        while destination_cup_value in pickup_cups or destination_cup_value == 0:
            destination_cup_value += -1
            if destination_cup_value < self.lowest_cup_value:
                destination_cup_value = self.highest_cup_value

        destination_cup = self.cups.index(destination_cup_value)
        return destination_cup, destination_cup_value
    
    def play_game(self, n_rounds):
        for _ in range(n_rounds):
            self.do_round()
            
        while self.cups[0] != 1:
            self.cups.rotate(1)
        
        self.cups.remove(1)
            
        return ''.join([
            str(x) for x in self.cups
        ])


if __name__ == '__main__':

   
    game = CrabCups(INITIAL_CUP_ORDER)
    order = game.play_game(100)

    print('Part 1 Solution: {}'.format(
        order
    ))
    
    
    """
    OS 2020-02-23: looks like `collections.deque` isn't good enough. Do I need to write my own `LinkedList` object?
    """
    game = CrabCups(INITIAL_CUP_ORDER, number_of_cups=1000000)
    order = game.play_game(10000000)

    print('Part 2 Solution: {}\n'.format(
        int(order[0]) * int(order[1])
    ))
