package main

import (
	"fmt"
	"os"
	"path"
	"runtime"
	"strconv"
	"strings"

	"github.com/mowshon/iterium"
)

func main() {
	fmt.Printf("Part 1 result: %d\n", solve([]string{"+", "*"}))
	fmt.Printf("Part 2 result: %d\n", solve([]string{"+", "*", "||"}))
}

func solve(operators []string) int {
	data := parseInput()
	result := 0
	for _, line := range data {
		key := line[0]
		vals := line[1:]
		if isSolveable(key, vals, operators) {
			result += key
		}
	}
	return result
}

func isSolveable(key int, vals []int, operators []string) bool {
	n := len(vals)
	product := iterium.Product(operators, n-1)
	combinations, _ := product.Slice()
	for _, combination := range combinations {
		// now calculate the result of the operator combination
		result := vals[0]
		for i, operator := range combination {
			if operator == "+" {
				result += vals[i+1]
			} else if operator == "*" {
				result *= vals[i+1]
			} else {
				// concatenate together
				result, _ = strconv.Atoi(strconv.Itoa(result) + strconv.Itoa(vals[i+1]))
			}
		}
		if result == key {
			// fmt.Println("Found:", key, vals, combination)
			return true
		}
	}
	// fmt.Println("Not found:", key, vals)
	return false
}

func parseInput() [][]int {
	_, goFilename, _, _ := runtime.Caller(1)
	dataFilename := path.Join(path.Dir(goFilename), "07_input.txt")
	input, _ := os.ReadFile(dataFilename)
	lines := strings.Split(string(input), "\n")

	parsedInput := [][]int{}
	for _, line := range lines {
		if line != "" {
			parsedLine := strings.Split(line, ": ")
			key, _ := strconv.Atoi(parsedLine[0])
			val := []int{key}
			for _, value := range strings.Split(parsedLine[1], " ") {
				intVal, _ := strconv.Atoi(value)
				val = append(val, intVal)
			}
			parsedInput = append(parsedInput, val)
		}
	}

	return parsedInput
}
