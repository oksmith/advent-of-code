package main

import (
	"fmt"
	"os"
	"path"
	"regexp"
	"runtime"
	"strconv"
	"strings"
)

func main() {
	fmt.Printf("Part 1 result: %d\n", partone())
	fmt.Printf("Part 2 result: %d\n", parttwo())
}

func partone() int {
	data := readInput()

	r := regexp.MustCompile(`mul\(\d{1,3},\d{1,3}\)`) // must be a 1-3 digit number?
	matches := r.FindAllString(data, -1)

	result := 0
	for _, match := range matches {
		product := mul(match)
		result += product
	}
	return result
}

func parttwo() int {
	data := readInput()

	// look for all `mul` and `do` and `undo` operations
	r := regexp.MustCompile(`mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)`)
	matches := r.FindAllString(data, -1)

	result := 0
	do := true
	for _, match := range matches {
		if match == "do()" {
			do = true
		} else if match == "don't()" {
			do = false
		} else {
			if do {
				product := mul(match)
				result += product
			}
		}
	}
	return result
}

func mul(matchString string) int {
	// take the firstNumber,secondNumber substring
	subStr := matchString[4 : len(matchString)-1]

	digitsStr := strings.Split(subStr, ",")
	firstNumber, _ := strconv.Atoi(digitsStr[0])
	secondNumber, _ := strconv.Atoi(digitsStr[1])
	return firstNumber * secondNumber
}

func readInput() string {
	_, goFilename, _, _ := runtime.Caller(1)
	dataFilename := path.Join(path.Dir(goFilename), "03_input.txt")
	input, _ := os.ReadFile(dataFilename)
	return string(input)
}
