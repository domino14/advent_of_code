package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strconv"
	"strings"
)

const FountainX = 500

var RecursedMap map[int]bool

func parseRange(r string) (int, int) {
	rs := strings.Split(r, "..")
	rstart, _ := strconv.Atoi(rs[0])
	rend, _ := strconv.Atoi(rs[1])
	return rstart, rend
}

func addToMap(watertable map[int]map[int]rune, x int, y int, ch rune) {
	if watertable[y] == nil {
		watertable[y] = make(map[int]rune)
	}
	if ch == '~' && watertable[y][x] == '~' {
		panic("Bad")
	}
	watertable[y][x] = ch
}

func createMap() (map[int]map[int]rune, int, int, int, int) {
	cacheFilename := "/tmp/adventofcode_2018_17"
	// cacheFilename = "./example17.txt"
	dat, _ := ioutil.ReadFile(cacheFilename)
	var minx, maxx, miny, maxy int
	minx = 1000000
	maxx = -1000000
	miny = 1000000
	maxy = -1000000

	watertable := make(map[int]map[int]rune)

	for _, line := range strings.Split(string(dat), "\n") {
		var x, y, xstart, xend, ystart, yend int
		coords := strings.Split(line, ", ")
		vein := [][]string{}
		for _, coord := range coords {
			desc := strings.Split(coord, "=")
			vein = append(vein, desc)
		}
		if vein[0][0] == "x" {
			ystart, yend = parseRange(vein[1][1])
			x, _ = strconv.Atoi(vein[0][1])
			if x < minx {
				minx = x
			}
			if x > maxx {
				maxx = x
			}
			if ystart < miny {
				miny = ystart
			}
			if yend > maxy {
				maxy = yend
			}
			for y := ystart; y <= yend; y++ {
				addToMap(watertable, x, y, '#')
			}
		}
		if vein[0][0] == "y" {
			xstart, xend = parseRange(vein[1][1])
			y, _ = strconv.Atoi(vein[0][1])
			if y < miny {
				miny = y
			}
			if y > maxy {
				maxy = y
			}
			if xstart < minx {
				minx = xstart
			}
			if xend > maxx {
				maxx = xend
			}
			for x := xstart; x <= xend; x++ {
				addToMap(watertable, x, y, '#')
			}
		}
	}
	return watertable, minx, maxx, miny, maxy
}

func passable(wtable map[int]map[int]rune, x, y int) bool {
	return wtable[y] == nil || wtable[y][x] == '|' || wtable[y][x] == 0
}

func moveSideways(wtable map[int]map[int]rune, miny, maxy, x, y, dir, dropsGen int) (int, int) {
	seenMap := make(map[int]int)

	for {
		x += dir
		idx := y*100000 + x

		if passable(wtable, x, y) {
			addToMap(wtable, x, y, '|')

			if passable(wtable, x, y+1) {
				if _, ok := RecursedMap[idx]; !ok {
					traceDropPath(wtable, miny, maxy, x, y, dropsGen)
				}
				RecursedMap[idx] = true
				return -1, -1
			}

		} else {
			x -= dir
			dir *= -1
			idx = y*100000 + x
		}
		seenMap[idx]++
		if seenMap[idx] == 2 {
			return x, y
		}
		if y > maxy {
			break
		}
	}
	return -1, -1
}

func traceDropPath(wtable map[int]map[int]rune, miny, maxy, x, y, dropsGen int) {
	for y < maxy {
		y = y + 1
		if passable(wtable, x, y) {
			// drop thru
			addToMap(wtable, x, y, '|')
		} else {
			// Travel left and right and bounce back.
			s1x, s1y := moveSideways(wtable, miny, maxy, x, y-1, -1, dropsGen)
			s2x, s2y := moveSideways(wtable, miny, maxy, x, y-1, 1, dropsGen)

			if s1x != -1 && s2x != -1 && s1y == s2y {
				ysettle := s1y
				var xsettle int
				// sort s1x, s2x, FountainX
				i := []int{s1x, s2x, FountainX}
				sort.Ints(i)
				if i[0] == FountainX {
					xsettle = i[2]
				} else if i[2] == FountainX {
					xsettle = i[0]
				} else {
					xsettle = i[0]
				}
				addToMap(wtable, xsettle, ysettle, '~')
			}
			break
		}
	}
}

func countWater(wtable map[int]map[int]rune, miny, maxy int) (int, int) {
	var settled, sand int
	for y, xs := range wtable {
		if y < miny || y > maxy {
			continue
		}
		for _, tileval := range xs {
			if tileval == '~' {
				settled++
			}
			if tileval == '|' {
				sand++
			}
		}
	}
	return settled, sand
}

func printMap(wtable map[int]map[int]rune) {
	lines := []string{}
	for y := 1; y <= 13; y++ {
		line := ""
		for x := 494; x <= 507; x++ {
			rn, ok := wtable[y][x]
			if !ok {
				line = line + "."
			} else {
				line = line + string(rn)
			}
		}
		lines = append(lines, line)
	}
	fmt.Println()
	for _, line := range lines {
		fmt.Println(line)
	}
	fmt.Println()
}

func main() {
	wtable, minx, maxx, miny, maxy := createMap()
	fmt.Printf("miny=%v, maxy=%v, minx=%v, maxx=%v, map=%v",
		miny, maxy, minx, maxx, wtable)
	lastSettled := -1
	lastSand := -1
	dropsGen := 0
	RecursedMap = make(map[int]bool)

	for {
		RecursedMap = map[int]bool{}
		fmt.Println("----------")
		x, y := FountainX, 0
		traceDropPath(wtable, miny, maxy, x, y, dropsGen)

		settled, sand := countWater(wtable, miny, maxy)
		if settled == lastSettled && sand == lastSand {
			break
		}
		lastSettled, lastSand = settled, sand
		dropsGen++
		fmt.Printf("%v (%v, %v)\n", dropsGen, lastSettled, lastSand)
		// printMap(wtable)

	}
	fmt.Printf("Part 1: %v (part2: %v + %v) (%v)", lastSettled+lastSand,
		lastSettled, lastSand, dropsGen)
}
