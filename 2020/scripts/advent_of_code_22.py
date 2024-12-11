import copy


CARDS = 'inputs/22_input.txt'


class CombatCards(object):
    def __init__(self, p1_cards, p2_cards):
        self.p1_cards = copy.deepcopy(p1_cards)
        self.p2_cards = copy.deepcopy(p2_cards)
        self.rounds_completed = 0
        
    def do_round(self):
        p1 = self.p1_cards.pop(0)
        p2 = self.p2_cards.pop(0)
        
        if p1 > p2:
            self.p1_cards = self.p1_cards + [p1, p2]
        elif p2 > p1:
            self.p2_cards = self.p2_cards + [p2, p1]
        else:
            raise ValueError('Encountered a draw! {}, {}, {}'.format(p1, p2, self.rounds_completed+1))
            
    def play_game(self):
        while len(self.p1_cards) > 0 and len(self.p2_cards) > 0:
            self.do_round()
            
        final_deck_order = self.p1_cards + self.p2_cards
        return final_deck_order
        
        
    def calculate_winning_score(self, final_deck_order):
        n = len(final_deck_order)
        ans = 0
        for i, val in enumerate(final_deck_order):
            ans += (n-i)*val
    
        return ans
    
    
class RecursiveCombat(CombatCards):
    def __init__(self, p1_cards, p2_cards):
        super().__init__(p1_cards, p2_cards)
        self.winner = None
        self.decks_seen = list((copy.deepcopy(p1_cards), copy.deepcopy(p2_cards)))
        
    def do_round(self):
        p1 = self.p1_cards.pop(0)
        p2 = self.p2_cards.pop(0)
        if len(self.p1_cards) >= p1 and len(self.p2_cards) >= p2:
            # Begin sub-game
            game = RecursiveCombat(self.p1_cards[:p1], self.p2_cards[:p2])
            game.play_game()
            if game.winner == 'p1':
                self.p1_cards = self.p1_cards + [p1, p2]
            else:
                self.p2_cards = self.p2_cards + [p2, p1]

        else:
            # Continue with game
            if p1 > p2:
                self.p1_cards = self.p1_cards + [p1, p2]
            elif p2 > p1:
                self.p2_cards = self.p2_cards + [p2, p1]
            else:
                raise ValueError('Encountered a draw! {}, {}, {}'.format(p1, p2, self.rounds_completed+1))
                
        if (self.p1_cards, self.p2_cards) in self.decks_seen:
            self.winner = 'p1'
        else:
            self.decks_seen.append((copy.deepcopy(self.p1_cards), copy.deepcopy(self.p2_cards)))
            
    def play_game(self):
        i = 1
        while len(self.p1_cards) > 0 and len(self.p2_cards) > 0 and not self.winner:
            self.do_round()
            i += 1
            
        final_deck_order = self.p1_cards + self.p2_cards
        if len(self.p1_cards) == 0:
            self.winner = 'p2'
        else:
            self.winner = 'p1'
            
        return final_deck_order



if __name__ == '__main__':

    with open(CARDS, 'r') as f:
        p1_cards, p2_cards = f.read().strip().split('\n\n')
        p1_cards = [int(x) for x in p1_cards.split('\n')[1:]]
        p2_cards = [int(x) for x in p2_cards.split('\n')[1:]]
        
        
    game = CombatCards(p1_cards, p2_cards)
    final_deck_order = game.play_game()

    print('Part 1 Solution: {}'.format(
        game.calculate_winning_score(final_deck_order)
    ))
    
    game2 = RecursiveCombat(p1_cards, p2_cards)
    final_deck_order = game2.play_game()

    print('Part 2 Solution: {}\n'.format(
        game2.calculate_winning_score(final_deck_order)
    ))
