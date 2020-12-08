GAMEBOY_CODE = 'inputs/08_input.txt'


class GameBoy:
    def __init__(self, startup_commands):
        self.accumulator = 0
        self.loop_number = 0
        self.line_number = 0
        self.startup_commands = startup_commands
        self.lines_run = []
        self.started = False
        
    def reset(self):
        self.accumulator = 0
        self.loop_number = 0
        self.line_number = 0
        self.lines_run = []
        
    def run_next_command(self):
        
        command = self.startup_commands[self.line_number]
        command_type = command.split(' ')[0]
        command_num = int(command.split(' ')[1])
        
        self.lines_run.append(self.line_number)
        
        if command_type == 'jmp':
            self.line_number += command_num
        elif command_type == 'acc':
            self.accumulator += command_num
            self.line_number += 1
        elif command_type == 'nop':
            self.line_number += 1
            pass
        else:
            raise ValueError(
                'Encountered command type {} (expected ' + 
                '`jmp`, `acc` or `nop`)!'.format(command_type)
            )   
        
        if self.line_number in self.lines_run:
            self.loop_number += 1
        elif self.line_number > len(self.startup_commands) - 1:
            self.started = True
        
    def get_accumulator_value_after_first_loop_or_startup(self):
        while self.loop_number == 0 and not self.started:
            self.run_next_command()
            
        return self.accumulator
    
    

def debug_gameboy(commands, command_type, replacement_type):
    
    for i, command in enumerate(commands):
        if command.split(' ')[0] == command_type:
            new_commands = [
                commands[j] if j != i else commands[j].replace(command_type, replacement_type) 
                for j in range(len(commands))
            ]
            game = GameBoy(new_commands)
            value = game.get_accumulator_value_after_first_loop_or_startup()
            if game.started:
                # Successfully booted up the gameboy
                print('Debugged! Replaced {} with {} in position {}'.format(
                    command_type, replacement_type, i
                ))
                return value
            else:
                pass
            
        else:
            pass


if __name__ == '__main__':

    with open(GAMEBOY_CODE, 'r') as f:
        commands = [line for line in f.read().strip().split("\n")]

    game = GameBoy(commands)

    print('Part 1 Solution: {}'.format(
        game.get_accumulator_value_after_first_loop_or_startup()
    ))
    
    debugged_gameboy_accumulator = debug_gameboy(commands, 'jmp', 'nop')
    
    print('Part 2 Solution: {}\n'.format(
        debugged_gameboy_accumulator
    ))
