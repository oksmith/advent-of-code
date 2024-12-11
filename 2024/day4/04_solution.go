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
	return xmasSearch(data)
}

func parttwo() int {
	data := parseInput()
	return masCrossSearch(data)
}

func xmasSearch(data [][]string) int {
	n := len(data) // column and row length
	directions := [][]int{{1, 0}, {1, -1}, {0, -1}, {-1, -1}, {-1, 0}, {-1, 1}, {0, 1}, {1, 1}}

	// search for the word "XMAS" in all directions
	xmasCount := 0
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			if data[i][j] == "X" {
				for _, dir := range directions {
					match := searchLine(data, i, j, dir)
					if match {
						xmasCount += 1
					}
				}
			}
		}
	}

	return xmasCount
}

func masCrossSearch(data [][]string) int {
	n := len(data) // column and row length

	// search for the word "MAS" in a cross pattern
	masCount := 0
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			if data[i][j] == "A" {
				match := searchCross(data, i, j)
				if match {
					masCount += 1
				}
			}
		}
	}

	return masCount

}

func searchCross(data [][]string, i int, j int) bool {
	// search for the word "MAS" in a cross pattern
	// we know that position (i,j) contains an A

	// first, check if we've run out of space
	if i-1 < 0 || i+1 >= len(data) || j-1 < 0 || j+1 >= len(data) {
		// coordinate of 'M' or 'S' will be out of bounds so we return match=false
		return false
	}

	// check if the word "MAS" is in the cross pattern, starting from (i, j)
	if ((data[i-1][j-1] == "M" && data[i+1][j+1] == "S") ||
		(data[i-1][j-1] == "S" && data[i+1][j+1] == "M")) &&
		((data[i-1][j+1] == "M" && data[i+1][j-1] == "S") ||
			(data[i-1][j+1] == "S" && data[i+1][j-1] == "M")) {
		return true
	}
	return false

}

func searchLine(data [][]string, i int, j int, dir []int) bool {
	// search for the word "XMAS" in a particular directions
	// we know that position (i,j) contains an X

	// first, check if we've run out of space
	if i+dir[0]*3 < 0 || i+dir[0]*3 >= len(data) || j+dir[1]*3 < 0 || j+dir[1]*3 >= len(data) {
		// coordinate of 'S' will be out of bounds so we return match=false
		return false
	}

	// check if the word "XMAS" is in the direction, starting from (i, j)
	if data[i+dir[0]][j+dir[1]] == "M" && data[i+dir[0]*2][j+dir[1]*2] == "A" && data[i+dir[0]*3][j+dir[1]*3] == "S" {
		return true
	}
	return false
}

func parseInput() [][]string {
	_, goFilename, _, _ := runtime.Caller(1)
	dataFilename := path.Join(path.Dir(goFilename), "04_input.txt")
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
