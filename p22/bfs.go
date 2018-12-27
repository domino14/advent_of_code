package main

import (
	"fmt"
)

type Point struct {
	x, y, tool int
}

type QueueMember struct {
	pt   Point
	cost int
}

func (qm *QueueMember) String() string {
	return fmt.Sprintf("<pt: (%v, %v -- %v), tool: %v, cost: %v>",
		qm.pt.x, qm.pt.y, regionTypeText(regionTypeFromCache(qm.pt.x, qm.pt.y)),
		toolText(qm.pt.tool), qm.cost)
}

func toCode(pt Point) int {
	return pt.tool*10000*10000 + pt.y*10000 + pt.x
}

func equipmentPermitted(regionType int) []int {
	if regionType == RegionRocky {
		return []int{Torch, Climbing}
	} else if regionType == RegionNarrow {
		return []int{Torch, NoEquip}
	} else if regionType == RegionWet {
		return []int{Climbing, NoEquip}
	}
	return []int{}
}

func isPermittedIn(equipment, regionType int) bool {
	permitted := false
	for _, eq := range equipmentPermitted(regionType) {
		if equipment == eq {
			permitted = true
			break
		}
	}
	return permitted
}

func queueAddition(oqm *QueueMember, ex, ey int, cave caveMap) []*QueueMember {
	myRegion := regionTypeFromCache(oqm.pt.x, oqm.pt.y)
	myEquipped := oqm.pt.tool
	toAdd := []*QueueMember{}

	// Move spatially, with no equipment changes.
	for _, cell := range [][2]int{
		{oqm.pt.x + 1, oqm.pt.y},
		{oqm.pt.x, oqm.pt.y + 1},
		{oqm.pt.x - 1, oqm.pt.y},
		{oqm.pt.x, oqm.pt.y - 1}} {

		if cell[0] < 0 || cell[1] < 0 || cell[0] > int(float64(ex)*BFSXmul) ||
			cell[1] > int(float64(ey)*BFSYmul) {
			continue
		}
		cellRegion := cave[cell[1]][cell[0]]

		if !isPermittedIn(myEquipped, cellRegion) {
			continue
		}

		qm := &QueueMember{
			Point{cell[0], cell[1], myEquipped},
			1 + oqm.cost,
		}
		toAdd = append(toAdd, qm)
	}

	// Move only in "equipment change" space
	permitted := equipmentPermitted(myRegion)
	for _, eq := range permitted {
		if eq == myEquipped {
			continue
		}
		qm := &QueueMember{
			Point{oqm.pt.x, oqm.pt.y, eq},
			7 + oqm.cost,
		}
		toAdd = append(toAdd, qm)
	}

	return toAdd
}

func bfs(bx, by, ex, ey int, cave caveMap) int {
	fastQueueLookup := map[int]int{}

	startpt := Point{bx, by, Torch}
	endpt := Point{ex, ey, Torch}
	cost := 0

	queue := []*QueueMember{&QueueMember{endpt, cost}}
	fastQueueLookup[toCode(endpt)] = cost

	elIdx := -1
	for elIdx < len(queue)-1 {
		elIdx++
		qm := queue[elIdx]
		toAdd := queueAddition(qm, ex, ey, cave)
		toAddCopy := []*QueueMember{}

		for _, nqm := range toAdd {
			existingCost, ok := fastQueueLookup[toCode(nqm.pt)]
			if !(ok && existingCost <= nqm.cost) {
				toAddCopy = append(toAddCopy, nqm)
			}
		}
		queue = append(queue, toAddCopy...)
		for _, qm := range toAddCopy {
			fastQueueLookup[toCode(qm.pt)] = qm.cost
		}
		if elIdx%100000 == 0 {
			// log.Printf("Processed %v cells... (sample %v, len %v)\n", elIdx, qm, len(toAddCopy))
		}
	}
	printSteps(fastQueueLookup, startpt, endpt, fastQueueLookup[toCode(startpt)])
	return fastQueueLookup[toCode(startpt)]
}

func toolText(tool int) string {
	if tool == Torch {
		return "a torch"
	}
	if tool == Climbing {
		return "climbing gear"
	}
	if tool == NoEquip {
		return "nothing"
	}
	return "---"
}

func regionTypeText(rt int) string {
	if rt == 0 {
		return "rocky"
	} else if rt == 1 {
		return "wet"
	} else {
		return "narrow"
	}
}

func printSteps(lookup map[int]int, startpt Point, endpt Point, finalCost int) {
	fmt.Printf("Begin at (%v, %v -- %v) holding %v, t=%v\n", startpt.x, startpt.y,
		regionTypeText(regionTypeFromCache(startpt.x, startpt.y)), toolText(startpt.tool),
		0)

	pt := startpt
	for true {
		lowest, lowestCost := findLowestNeighbor(pt, lookup)

		if lowest.x == pt.x && lowest.y == pt.y {
			fmt.Printf("Switched to holding %v (%v minutes)\n", toolText(lowest.tool),
				finalCost-lowestCost)
		} else {
			fmt.Printf("Walked to (%v, %v -- %v), holding %v (%v minutes)\n", lowest.x, lowest.y,
				regionTypeText(regionTypeFromCache(lowest.x, lowest.y)),
				toolText(lowest.tool), finalCost-lowestCost)
		}

		pt = lowest
		if pt.x == endpt.x && pt.y == endpt.y && pt.tool == endpt.tool {
			break
		}

	}
	fmt.Printf("End at (%v, %v -- %v) holding %v (%v minutes)\n", endpt.x, endpt.y,
		regionTypeText(regionTypeFromCache(endpt.x, endpt.y)),
		toolText(endpt.tool), finalCost)
}

func findLowestNeighbor(pt Point, lookup map[int]int) (Point, int) {
	var lowestPt Point

	lowest := 100000000
	myCode := toCode(pt)
	myCost := lookup[myCode]
	neighbors := []*QueueMember{}
	for _, cell := range [][2]int{
		{pt.x + 1, pt.y},
		{pt.x, pt.y + 1},
		{pt.x - 1, pt.y},
		{pt.x, pt.y - 1}} {

		newPt := Point{cell[0], cell[1], pt.tool}

		code := toCode(newPt)
		if cost, ok := lookup[code]; ok {

			if cost < lowest {
				lowest = cost
				lowestPt = newPt
			}
			neighbors = append(neighbors, &QueueMember{newPt, cost})
		}
	}

	for tool := range [3]int{Torch, Climbing, NoEquip} {
		if tool == pt.tool {
			continue
		}
		newPt := Point{pt.x, pt.y, tool}
		code := toCode(newPt)
		if cost, ok := lookup[code]; ok {
			if cost < lowest {
				lowest = cost
				lowestPt = newPt
			}
			neighbors = append(neighbors, &QueueMember{newPt, cost})
		}
	}

	if lowest >= myCost {
		panic(fmt.Sprintf("NO %v (%v) > %v (%v)", lowest, lowestPt, myCost, pt))
	}

	// fmt.Printf("  Neighbors for %v: %v\n", pt, neighbors)

	return lowestPt, lowest
}
