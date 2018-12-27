package main

type Point struct {
	x, y, tool int
}

type QueueMember struct {
	pt   Point
	cost int
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

func queueAddition(oqm *QueueMember, ex, ey int, cave caveMap) []*QueueMember {
	myRegion := regionTypeFromCache(oqm.pt.x, oqm.pt.y)
	myEquipped := oqm.pt.tool
	toAdd := []*QueueMember{}

	for _, cell := range [][2]int{
		{oqm.pt.x + 1, oqm.pt.y},
		{oqm.pt.x, oqm.pt.y + 1},
		{oqm.pt.x - 1, oqm.pt.y},
		{oqm.pt.x, oqm.pt.y - 1}} {

		if cell[0] < 0 || cell[1] < 0 || cell[0] > int(float64(ex)*BFSXmul) ||
			cell[1] > int(float64(ey)*BFSYmul) {
			continue
		}

		cellRegion := caveMap[cell[1]][cell[0]]

	}
}

func bfs(bx, by, ex, ey int, cave caveMap) int {
	fastQueueLookup := map[int]int{}

	startpt := Point{bx, by, Torch}
	endpt := Point{ex, ey, Torch}
	cost := 0

	queue := []*QueueMember{&QueueMember{endpt, cost}}

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
		queue = append(queue, toAdd...)
		for _, qm := range toAddCopy {
			fastQueueLookup[toCode(qm.pt)] = qm.cost
		}
	}
	return fastQueueLookup[toCode(startpt)]
}
