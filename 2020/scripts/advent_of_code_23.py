import copy
from collections import deque


INITIAL_CUP_ORDER = 598162734
    
"""
Understanding what linked lists are and how to implement custom ones:
https://www.tutorialspoint.com/python_data_structure/python_linked_lists.htm
"""   
    
class Node(object):
    def __init__(self, parent, value, prev, next_):
        assert isinstance(parent, LinkedList)
        self.parent = parent
        self.value = value
        self.prev = prev
        self.next = next_
        
    def insert(self, x):
        node = Node(self.parent, x, self, self.next)
        self.parent.dict[x] = node
        self.next = node
        node.next.prev = node
        return node
    
    def erase(self):
        self.next.prev = self.prev
        self.prev.next = self.next
        del self.parent.dict[self.value]
        

class LinkedList(object):
    def __init__(self, initial_list=None):
        self.dict = {}
        if initial_list:
            X = LinkedList()
            prev = None
            for x in initial_list:
                prev = X.append(prev, x)
            self.dict = X.dict
        
    def append(self, prev, x):
        if prev is None:
            node = Node(self, x, None, None)
            node.next = node
            node.prev = node
            self.dict[x] = node
            return node
        else:
            node = Node(self, x, prev, prev.next)
            prev.next = node
            node.next.prev = node
            self.dict[x] = node
            return node

    def find(self, x):
        return self.dict[x]

    def to_list(self, start):
        node = self.dict[start]
        ret = [node.value]
        node = node.next
        while node.value != start:
            ret.append(node.value)
            node = node.next
        return ret
    

class CrabCups(object):
    def __init__(self, inital_cup_order, number_of_cups=None):
        inital_cup_order = str(inital_cup_order)
        
        if number_of_cups and len(inital_cup_order) < number_of_cups:
            inital_cup_order = list(map(int, inital_cup_order)) + [x for x in range(len(inital_cup_order)+1, number_of_cups+1)]
            assert len(inital_cup_order) == number_of_cups
        else:
            inital_cup_order = list(map(int, inital_cup_order))
            
        self.cups = LinkedList(inital_cup_order)
        self.current_node = self.cups.find(inital_cup_order[0])

        # Class attributes which do not change 
        self.num_cups = len(inital_cup_order)
        self.lowest_cup_value = min(inital_cup_order)
        self.highest_cup_value = max(inital_cup_order)

    def do_round(self):
#         print('cups: ', self.cups.to_list(self.current_node.value))
#         print('current cup: ', self.current_node.value)
        pickup_cups = []
        pickup_node = self.current_node.next
        for _ in range(3):
            pickup_cups.append(pickup_node.value)
            next_ = pickup_node.next
            pickup_node.erase()
            pickup_node = next_
        
#         print('pickup: ', pickup_cups)
        
        destination_node = self.get_destination_node(pickup_cups)
#         print('destination: ', destination_node.value)
        
        for pickup_node in pickup_cups:
            destination_node = destination_node.insert(pickup_node)

        self.current_node = self.current_node.next
        
    def get_destination_node(self, pickup_cups):
        
        destination_cup_value = self.current_node.value-1 if self.current_node.value > 1 else self.num_cups
        
        while destination_cup_value in pickup_cups:
            destination_cup_value = destination_cup_value-1 if destination_cup_value > 1 else self.num_cups

        return self.cups.find(destination_cup_value)
    
    def play_game(self, n_rounds):
        for _ in range(n_rounds):
            self.do_round()
            
        return self.cups.to_list(1)


if __name__ == '__main__':

   
    game = CrabCups(INITIAL_CUP_ORDER)
    order = game.play_game(100)

    print('Part 1 Solution: {}'.format(
        ''.join([str(x) for x in order[1:]])
    ))
    
    game = CrabCups(INITIAL_CUP_ORDER, number_of_cups=1000000)
    order = game.play_game(10000000)

    print('Part 2 Solution: {}\n'.format(
        int(order[1]) * int(order[2])
    ))
