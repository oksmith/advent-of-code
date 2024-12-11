import copy

# Load data
with open("day1/data.txt", "r") as f:
    data = f.read().split("\n")

### Part 1

# create array to store numbers in
numbers = []
for line in data:
    first_num = None
    last_num = None

    # find first numeric character in line
    for char in line:
        if char.isnumeric():
            first_num = char
            break

    # find last numeric character in line
    for char in line[::-1]:
        if char.isnumeric():
            last_num = char
            break

    if first_num and last_num:
        numbers.append(int(first_num + last_num))

print(sum(numbers))


### Part 2

numbers_dict = {
    "one": 1, 
    "two": 2, 
    "three": 3, 
    "four": 4, 
    "five": 5, 
    "six": 6, 
    "seven": 7, 
    "eight": 8, 
    "nine": 9
}

# create array to store numbers in
numbers = []
for line in data:
    first_num = None
    last_num = None

    line_copy = copy.deepcopy(line)
    while first_num is None and len(line_copy) > 0:
        for k, v in numbers_dict.items():
            if line_copy.startswith(k):
                first_num = int(v)
        
        if line_copy[0].isnumeric():
            first_num = int(line_copy[0])

        line_copy = line_copy[1:]

    line_copy = copy.deepcopy(line)
    while last_num is None and len(line_copy) > 0:
        for k, v in numbers_dict.items():
            if line_copy.endswith(k):
                last_num = int(v)

        if line_copy[-1].isnumeric():
            last_num = int(line_copy[-1])

        line_copy = line_copy[:-1]

    if first_num and last_num:
        numbers.append(first_num + last_num)

print(sum(numbers))
