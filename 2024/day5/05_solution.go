package main

import (
	"fmt"
	"os"
	"path"
	"runtime"
	"strconv"
	"strings"
)

type Rules [100][100]bool

func main() {
	p1, p2 := solution()
	fmt.Printf("Part 1 result: %d\n", p1)
	fmt.Printf("Part 2 result: %d\n", p2)
}

func solution() (int, int) {
	rules, updates := parseInput()
	ruleTable := ruleTable(rules)

	part1 := 0
	part2 := 0
	for _, update := range updates {
		valid := isCorrectlyOrdered(update, ruleTable)
		if valid {
			middleNumber := update[len(update)/2]
			part1 += middleNumber
		} else {
			orderedUpdate := correctlyOrder(update, ruleTable)
			middleNumber := orderedUpdate[len(orderedUpdate)/2]
			part2 += middleNumber
		}
	}

	return part1, part2
}

func correctlyOrder(update []int, ruleTable Rules) []int {
	var orderedUpdate []int
	for i, num := range update {
		// if there are no elements in orderedUpdate, then we can just append
		if i == 0 {
			orderedUpdate = append(orderedUpdate, num)
			continue
		}

		toInsert := len(orderedUpdate)
		for j := 0; j < i; j++ {
			if ruleTable[orderedUpdate[j]][num] {
				// this means that num must come after element j
				// we keep going with the for loop in case there's another element
				// we need to insert after
				toInsert = j + 1
			}
		}

		if toInsert == len(orderedUpdate) {
			// in this case, we didn't find any element that num should come after
			// however... are there any elements num should come before?
			for j := 0; j < i; j++ {
				if ruleTable[num][orderedUpdate[j]] {
					// then num must come before element j
					toInsert = j
					break
				}
			}
		}

		// We've found the correct toInsert index. Now let's insert it.
		if toInsert == len(orderedUpdate) {
			orderedUpdate = append(orderedUpdate, num)
		} else {
			// create space at position toInsert
			orderedUpdate = append(orderedUpdate[:toInsert+1], orderedUpdate[toInsert:]...)
			orderedUpdate[toInsert] = num
		}
	}
	return orderedUpdate
}

func isCorrectlyOrdered(update []int, ruleTable Rules) bool {
	valid := true

	for i, num := range update {
		if i == 0 {
			continue
		}
		for j := 0; j < i; j++ {
			if !ruleTable[update[j]][num] {
				return false
			}
		}
	}
	return valid
}

func ruleTable(rules [][]int) Rules {
	// I think it would be more efficient to first create a dictionary that's very quick
	// to index, rather than looping through all rules for each update and checking the first
	// element
	var ruleTable Rules
	for _, rule := range rules {
		ruleTable[rule[0]][rule[1]] = true
	}
	return ruleTable
}

func parseInput() ([][]int, [][]int) {
	_, goFilename, _, _ := runtime.Caller(1)
	dataFilename := path.Join(path.Dir(goFilename), "05_input.txt")
	input, _ := os.ReadFile(dataFilename)
	blocks := strings.Split(string(input), "\n\n")
	if len(blocks) != 2 {
		fmt.Println("Invalid input format")
		os.Exit(1)
	}
	rules := strings.Split(blocks[0], "\n")
	updates := strings.Split(blocks[1], "\n")

	var parsedRules [][]int
	for _, rule := range rules {
		parsedRule := strings.Split(rule, "|")
		var parsedRuleIntegers []int
		for _, element := range parsedRule {
			elementInt, _ := strconv.Atoi(element)
			parsedRuleIntegers = append(parsedRuleIntegers, elementInt)
		}
		parsedRules = append(parsedRules, parsedRuleIntegers)
	}

	var parsedUpdates [][]int
	for _, update := range updates {
		parsedUpdate := strings.Split(update, ",")
		var parsedUpdateIntegers []int
		for _, element := range parsedUpdate {
			elementInt, _ := strconv.Atoi(element)
			parsedUpdateIntegers = append(parsedUpdateIntegers, elementInt)
		}
		parsedUpdates = append(parsedUpdates, parsedUpdateIntegers)
	}
	return parsedRules, parsedUpdates
}
