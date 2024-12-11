package main

import (
	"fmt"
	"os"
	"path"
	"runtime"
	"strings"
)

func main() {
	fmt.Printf("Part 1 result: %d\n", partone())
	fmt.Printf("Part 2 result: %d\n", parttwo())
}

func partone() int {
	data := parseInput()
	symbolLocations := getSymbolLocations(data)
	fullAntinodesSet := map[[2]int]bool{}
	for _, locations := range symbolLocations {
		getAntinodes(locations, data, true, fullAntinodesSet)
	}
	return len(fullAntinodesSet)
}

func parttwo() int {
	data := parseInput()
	symbolLocations := getSymbolLocations(data)
	fullAntinodesSet := map[[2]int]bool{}
	for _, locations := range symbolLocations {
		getAntinodes(locations, data, false, fullAntinodesSet)
	}
	return len(fullAntinodesSet)
}

func getAntinodes(locations [][2]int, data [][]string, pairwise bool, fullAntinodesSet map[[2]int]bool) {
	// for every pair of locations, there are 2 antinodes
	// get those locations, evaluate if they are valid locations on data, and
	// if they are, add them to fullAntinodesSet
	for i := 0; i < len(locations); i++ {
		for j := i + 1; j < len(locations); j++ {
			validAntinodes := getAntinodeGroup(locations[i], locations[j], pairwise, data)
			for _, antinode := range validAntinodes {
				fullAntinodesSet[antinode] = true
			}
		}
	}
}

func getAntinodeGroup(location1, location2 [2]int, pairwise bool, data [][]string) [][2]int {
	antinodes := [][2]int{}
	vector := [2]int{location2[0] - location1[0], location2[1] - location1[1]}
	n := len(data)
	m := len(data[0])

	if !pairwise {
		antinodes = append(antinodes, location1)
		antinodes = append(antinodes, location2)
	}

	for i := 0; location1[0] >= 0 && location1[0] < n && location1[1] >= 0 && location1[1] < m; i++ {
		location1[0] = location1[0] - vector[0]
		location1[1] = location1[1] - vector[1]
		if isValidLocation(location1, data) {
			antinodes = append(antinodes, location1)
		}
		if pairwise {
			break // exit for loop
		}
	}
	for j := 0; location2[0] >= 0 && location2[0] < n && location2[1] >= 0 && location2[1] < m; j++ {
		location2[0] = location2[0] + vector[0]
		location2[1] = location2[1] + vector[1]
		if isValidLocation(location2, data) {
			antinodes = append(antinodes, location2)
		}
		if pairwise {
			break // exit for loop
		}
	}
	return antinodes
}

func isValidLocation(location [2]int, data [][]string) bool {
	if location[0] < 0 || location[0] >= len(data) {
		return false
	}
	if location[1] < 0 || location[1] >= len(data[0]) {
		return false
	}
	return true
}

func getSymbolLocations(data [][]string) map[string][][2]int {
	symbolLocations := map[string][][2]int{}
	for i, row := range data {
		for j, symbol := range row {
			if symbol != "." {
				if _, ok := symbolLocations[symbol]; !ok {
					symbolLocations[symbol] = make([][2]int, 0)
				}
				symbolLocations[symbol] = append(symbolLocations[symbol], [2]int{i, j})
			}
		}
	}
	return symbolLocations
}

func parseInput() [][]string {
	_, goFilename, _, _ := runtime.Caller(1)
	dataFilename := path.Join(path.Dir(goFilename), "08_input.txt")
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
