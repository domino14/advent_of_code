package main

import "fmt"

func fishes(days int, repr int, delay int) int {
	day := 0
	nums := []int8{1}

	for day < days {
		fmt.Println("day:", day, "fish", len(nums))
		newFishes := []int8{}
		for idx := range nums {
			nums[idx] -= 1

			if nums[idx] == -1 {
				newFishes = append(newFishes, int8(repr+delay-1))
				nums[idx] = int8(repr - 1)
			}
		}
		nums = append(nums, newFishes...)
		day += 1
	}
	return len(nums)
}

func main() {
	repr := 7
	delay := 2
	fmt.Println("fishes:", fishes(256, repr, delay))
}
