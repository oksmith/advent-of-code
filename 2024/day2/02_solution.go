package main

import (
	"fmt"
	"math"
	"os"
	"path"
	"runtime"
	"strconv"
	"strings"
)

func main() {
	fmt.Printf("Part 1 result: %d\n", partone())
	fmt.Printf("Part 2 result: %d\n", parttwo())
}

func partone() int {
	data := parseInput()
	isSafe := isSafeArray(data, false)
	safeCount := 0
	for _, safe := range isSafe {
		if safe {
			safeCount++
		}
	}
	return safeCount
}

func parttwo() int {
	data := parseInput()
	isSafe := isSafeArray(data, true)
	// // debugging
	// for i, report := range data {
	// 	fmt.Println(i, report, isSafe[i])
	// }
	safeCount := 0
	for _, safe := range isSafe {
		if safe {
			safeCount++
		}
	}
	return safeCount
}

func isSafeArray(data [][]int, removal bool) []bool {
	var safeArray []bool
	for _, report := range data {
		safe := isSafe(report, removal)
		safeArray = append(safeArray, safe)
	}
	return safeArray
}

func isSafe(report []int, removal bool) bool {
	isIncreasing := true
	isDecreasing := true
	maxDiff := 0.0

	for i := 1; i < len(report); i++ {
		if report[i] >= report[i-1] {
			isDecreasing = false
		}
		if report[i] <= report[i-1] {
			isIncreasing = false
		}
		diff := float64(report[i] - report[i-1])
		maxDiff = max(maxDiff, math.Abs(diff))
	}

	safe := (isIncreasing || isDecreasing) && maxDiff <= 3
	// check for safety at current level - Only relevant for Part 2
	if removal && !safe {
		// we remove an element from the report and try again.
		// Loop through all possible elements and try removing each
		// Note: I create a new slice here because I don't want to modify
		// the original array
		for i := 0; i < len(report); i++ {
			newReport := make([]int, 0, len(report)-1)
			newReport = append(newReport, report[:i]...)
			newReport = append(newReport, report[i+1:]...)
			if isSafe(newReport, false) {
				return true
			}
		}
	}
	return safe
}

func parseInput() [][]int {
	// Load data into array of lines
	_, goFilename, _, _ := runtime.Caller(1)
	dataFilename := path.Join(path.Dir(goFilename), "02_input.txt")
	input, _ := os.ReadFile(dataFilename)
	lines := strings.Split(string(input), "\n")

	var parsedInput [][]int
	for _, line := range lines {
		if line != "" {
			parsedLine := strings.Fields(line)
			var parsedLineIntegers []int
			for _, element := range parsedLine {
				elementInt, _ := strconv.Atoi(element)
				parsedLineIntegers = append(parsedLineIntegers, elementInt)
			}
			parsedInput = append(parsedInput, parsedLineIntegers)
		}
	}

	return parsedInput
}
