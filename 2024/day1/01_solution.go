package main

import (
	"fmt"
	"os"
	"path"
	"runtime"
	"sort"
	"strconv"
	"strings"
)

func main() {
	fmt.Printf("Part 1 result: %d\n", partone())
	fmt.Printf("Part 2 result: %d\n", parttwo())
}

func partone() int {
	data := parseInput()
	leftList, rightList := getLeftRightLists(data)
	sortData(leftList, rightList)
	distances := getDistances(leftList, rightList)
	result := sumDistances(distances)
	return result
}

func parttwo() int {
	data := parseInput()
	leftList, rightList := getLeftRightLists(data)
	result := similarityScore(leftList, rightList)
	return result
}

func similarityScore(leftList, rightList []int) int {
	score := 0
	for _, left := range leftList {
		appearances := 0
		for _, right := range rightList {
			if left == right {
				appearances++
			}
		}
		score = score + left*appearances
	}
	return score
}

func getLeftRightLists(data [][]int) ([]int, []int) {
	var leftList, rightList []int

	for _, pair := range data {
		leftList = append(leftList, pair[0])
		rightList = append(rightList, pair[1])
	}
	return leftList, rightList
}

func sortData(leftList, rightList []int) {
	sort.Ints(leftList)
	sort.Ints(rightList)
}

func getDistances(firstLocs, secondLocs []int) []int {
	var distances []int
	for i, line := range firstLocs {
		distance := line - secondLocs[i]
		if distance >= 0 {
			distances = append(distances, distance)
		} else {
			distances = append(distances, -distance)
		}
	}
	return distances
}

func sumDistances(distances []int) int {
	sum := 0
	for _, distance := range distances {
		sum += distance
	}
	return sum
}

func parseInput() [][]int {
	// Load data into array of lines
	_, goFilename, _, _ := runtime.Caller(1)
	dataFilename := path.Join(path.Dir(goFilename), "01_input.txt")
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
