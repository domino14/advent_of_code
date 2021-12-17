from copy import deepcopy
import heapq

input = open("./15/input.txt", "r").readlines()

mat = {}

for ridx, row in enumerate(input):
    for cidx, c in enumerate(row.strip()):
        mat[(ridx, cidx)] = int(c)

p1mat = deepcopy(mat)

dimr, dimc = ridx + 1, cidx + 1
end1 = (ridx, cidx)

new_mat = {}
for pt, cost in mat.items():
    for dr in range(0, 5):
        for dc in range(0, 5):
            r = pt[0] + (dr * dimr)
            c = pt[1] + (dc * dimc)
            newcost = (cost + dr + dc) % 9
            if newcost == 0:
                newcost = 9
            new_mat[(r, c)] = newcost


mat.update(new_mat)
# damn dijkstra

start = (0, 0)
end = (((ridx + 1) * 5) - 1, ((cidx + 1) * 5) - 1)

print(start, end)

inf = 1000000000


def dijkstra(start, end, mat):
    prev = {}
    dist = {}
    Q = []
    nonheap = set()
    for v in mat:
        dist[v] = inf
        prev[v] = None

    dist[start] = 0
    heapq.heappush(Q, (dist[start], start))
    nonheap.add(start)

    while len(Q) > 0:
        m = heapq.heappop(Q)
        nonheap.remove(m[1])
        u = m[1]
        if u == end:
            return shortest_path(u, start, prev, mat)

        for v in (
            (u[0] + 1, u[1]),
            (u[0] - 1, u[1]),
            (u[0], u[1] + 1),
            (u[0], u[1] - 1),
        ):
            try:
                alt = dist[u] + mat[v]
            except KeyError:
                continue
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                if v not in nonheap:
                    heapq.heappush(Q, (alt, v))
                    nonheap.add(v)

    return dist, prev


def shortest_path(u, start, prev, mat):
    S = []
    sum = 0
    if prev.get(u) or u == start:
        while u:
            S.insert(0, u)
            if u != start:
                sum += mat[u]
            u = prev[u]

    print("Seq is", S)
    print("cost is", sum)
    return sum


print('p1:', dijkstra(start, end1, p1mat))
print('p2:', dijkstra(start, end, mat))