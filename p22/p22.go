package main

import (
	"fmt"
	"strings"
)

type caveMap map[int]map[int]int

const (
	NoEquip = iota
	Torch
	Climbing
)

const (
	RegionRocky  = 0
	RegionWet    = 1
	RegionNarrow = 2
)

const (
	BFSYmul = 2.5
	BFSXmul = 10
)

var erosionLevelCache map[int]map[int]int

func geoIdx(x, y, depth, tx, ty int) int {
	if x == 0 && y == 0 {
		return 0
	}
	if x == tx && y == ty {
		return 0
	}
	if y == 0 {
		return x * 16807
	}
	if x == 0 {
		return y * 48271
	}
	return erosionLevel(x-1, y, tx, ty, depth) * erosionLevel(x, y-1, tx, ty, depth)
}

func erosionLevel(x, y, tx, ty, depth int) int {
	if erosionLevelCache == nil {
		erosionLevelCache = make(map[int]map[int]int)
	}
	if ymap, ok := erosionLevelCache[y]; ok {
		if xval, ok := ymap[x]; ok {
			return xval
		}
	} else {
		erosionLevelCache[y] = make(map[int]int)
	}
	el := (geoIdx(x, y, depth, tx, ty) + depth) % 20183
	erosionLevelCache[y][x] = el
	return el
}

func regionType(x, y, tx, ty, depth int) int {
	el := erosionLevel(x, y, tx, ty, depth)
	return el % 3
}

func regionTypeFromCache(x, y int) int {
	el := erosionLevelCache[y][x]
	return el % 3
}

func createMap(tx, ty, depth int) caveMap {
	cm := make(map[int]map[int]int)
	for y := 0; y < int(float64(ty)*BFSYmul+1); y++ {
		if _, ok := cm[y]; !ok {
			cm[y] = make(map[int]int)
		}
		for x := 0; x < int(float64(tx)*BFSXmul+1); x++ {
			cm[y][x] = regionType(x, y, tx, ty, depth)
		}
	}
	return caveMap(cm)
}

func calculateRisk(tlx, tly, brx, bry int, cave caveMap) int {
	risk := 0
	for y := tly; y < bry+1; y++ {
		for x := tlx; x < brx+1; x++ {
			risk += cave[y][x]
		}
	}
	return risk
}

func regionToChar(region int) string {
	if region == 0 {
		return "."
	} else if region == 1 {
		return "="
	}
	return "|"
}

func drawMap(cave caveMap) string {
	cells := []string{}
	for y := 0; y < len(cave); y++ {
		row := []string{}
		for x := 0; x < len(cave[y]); x++ {
			row = append(row, regionToChar(regionTypeFromCache(x, y)))
		}
		rowStr := strings.Join(row[:], "")
		cells = append(cells, rowStr)
	}
	return strings.Join(cells[:], "\n")
}

func main() {
	// tx, ty, depth := 3, 3, 6969
	tx, ty, depth := 16, 2, 6084
	// tx, ty, depth := 14, 709, 6084
	cave := createMap(tx, ty, depth)
	fmt.Println(drawMap(cave))
	risk := calculateRisk(0, 0, tx, ty, cave)
	fmt.Printf("Risk: %v\n", risk)
	fmt.Printf("Walking to: (%v, %v)\n", tx, ty)
	cost := bfs(0, 0, tx, ty, cave)
	fmt.Printf("Cost: %v\n", cost)
}
