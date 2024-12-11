package main

import (
	"fmt"
	"os"
	"path"
	"runtime"
	"strconv"
	"strings"
)

func main() {
	partOne, partTwo := solution()
	fmt.Printf("Part 1 result: %d\n", partOne)
	fmt.Printf("Part 2 result: %d\n", partTwo)
}

func solution() (int, int) {
	data := parseInput()

	directions := map[int][2]int{
		0: {-1, 0}, // up
		1: {0, 1},  // right
		2: {1, 0},  // down
		3: {0, -1}, // left
	}
	direction := 0 // first element of directions i.e. up

	// find starting position
	x, y := findStartPos(data)

	// initialise visitedLocations with the starting position
	visitedLocations := map[string]bool{
		fmt.Sprintf("%d,%d", x, y): true,
	}
	for x > 0 && x < len(data)-1 && y > 0 && y < len(data)-1 {
		x, y, direction = move(data, x, y, direction, directions)
		visitedLocations[fmt.Sprintf("%d,%d", x, y)] = true
	}

	// we can use the visitedLocations from part 1 to find the
	// potential loops in part 2. Only consider visited locations
	// when choosing potential obstructions
	// loop over all possible obstruction options
	x, y = findStartPos(data)
	direction = 0
	loops := 0
	for loc := range visitedLocations {
		locSplit := strings.Split(loc, ",")
		i, _ := strconv.Atoi(locSplit[0])
		j, _ := strconv.Atoi(locSplit[1])
		if i != x || j != y {
			// create a new map with the obstruction
			var newData [][]string
			for k, row := range data {
				newRow := make([]string, len(row))
				copy(newRow, row)
				if k == i {
					newRow[j] = "#"
				}
				newData = append(newData, newRow)
			}

			isLoop := isLoop(newData, x, y, direction, directions)
			if isLoop {
				loops++
			}
		}
	}
	return len(visitedLocations), loops
}

func isLoop(data [][]string, x, y, direction int, directions map[int][2]int) bool {
	// initialise visitedLocationDirections with the starting position and direction
	visitedLocationDirections := map[string]bool{
		fmt.Sprintf("%d,%d,%d", x, y, direction): true,
	}
	for x > 0 && x < len(data)-1 && y > 0 && y < len(data)-1 {
		x, y, direction = move(data, x, y, direction, directions)
		if visitedLocationDirections[fmt.Sprintf("%d,%d,%d", x, y, direction)] {
			return true
		} else {
			visitedLocationDirections[fmt.Sprintf("%d,%d,%d", x, y, direction)] = true
		}
	}
	return false

}

func move(data [][]string, x, y, direction int, directions map[int][2]int) (int, int, int) {
	if data[x+directions[direction][0]][y+directions[direction][1]] == "#" {
		// if the next position in current direction is an obstruction
		// move direction 90 degrees and do nothing else
		direction = (direction + 1) % 4
	} else {
		// assume all other elements of the array are "." or "^" (starting position), then
		// we move in the current direction and append the new position to visitedLocations
		x += directions[direction][0]
		y += directions[direction][1]
	}
	return x, y, direction
}

func findStartPos(data [][]string) (int, int) {
	for i, row := range data {
		for j, col := range row {
			if col == "^" {
				return i, j
			}
		}
	}
	return -1, -1
}

func parseInput() [][]string {
	_, goFilename, _, _ := runtime.Caller(1)
	dataFilename := path.Join(path.Dir(goFilename), "06_input.txt")
	input, _ := os.ReadFile(dataFilename)
	lines := strings.Split(string(input), "\n")

	var parsedInput [][]string
	for _, line := range lines {
		if line != "" {
			parsedLine := strings.Split(line, "")
			parsedInput = append(parsedInput, parsedLine)
		}
	}

	return parsedInput
}
