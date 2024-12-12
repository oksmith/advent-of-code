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
	fmt.Printf("Part 1 result: %d\n", partone())
	// fmt.Printf("Part 2 result: %d\n", parttwo())
}

func partone() int {
	data := parseInput()

	blocks := getBlocks(data)
	shuffled := shuffleBlocks(blocks)
	checksum := checksum(shuffled)
	return checksum
}

// func parttwo() int {
// 	data := parseInput()

// 	blocks := getBlocks(data)
// 	shuffled := shuffleBlocksByFile(blocks)
// 	fmt.Println(shuffled)
// 	checksum := checksum(shuffled)
// 	return checksum
// }

func checksum(blocks []int) int {
	var sum int
	for i, block := range blocks {
		sum += block * i
	}
	return sum
}

func shuffleBlocks(blocks []int) []int {
	sorted := []int{}
	leftIndex := 0
	rightIndex := len(blocks) - 1

	var leftBlock, rightBlock int

	for leftIndex < rightIndex {
		leftBlock = blocks[leftIndex]
		rightBlock = blocks[rightIndex]

		// keep searching for an empty block, starting from the left
		for leftBlock != -1 {
			sorted = append(sorted, leftBlock)
			leftIndex++
			leftBlock = blocks[leftIndex]
		}

		// now we have an empty block, we need to find a non-empty block
		// starting from the right
		for rightBlock == -1 {
			rightIndex--
			rightBlock = blocks[rightIndex]
		}

		// now move the rightmost block onto the empty leftIndex position
		// and continue
		sorted = append(sorted, rightBlock)
		leftIndex++
		rightIndex--
		continue
	}
	// finally, catch this last right block (if it's not empty)
	if blocks[rightIndex] != -1 {
		sorted = append(sorted, blocks[rightIndex])
	}
	return sorted
}

func getBlocks(data []int) []int {
	id := 0
	blocks := []int{}
	for i, num := range data {
		if i%2 == 0 {
			for i = 0; i < num; i++ {
				blocks = append(blocks, id)
			}
			id++
		} else {
			for i = 0; i < num; i++ {
				blocks = append(blocks, -1)
			}
		}
	}
	return blocks
}

func parseInput() []int {
	_, goFilename, _, _ := runtime.Caller(1)
	dataFilename := path.Join(path.Dir(goFilename), "09_input.txt")
	input, _ := os.ReadFile(dataFilename)
	nums := strings.Split(string(input), "")

	var parsedInput []int
	for _, num := range nums {
		numInt, _ := strconv.Atoi(num)
		parsedInput = append(parsedInput, numInt)
	}
	return parsedInput
}
