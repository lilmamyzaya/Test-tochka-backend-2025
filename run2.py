import sys
from collections import deque
import heapq

def get_input():
    return [list(line.strip()) for line in sys.stdin if line.strip()]

def neighbors(x, y):
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        yield x + dx, y + dy

def bfs(data, start, collected_keys):
    rows, cols = len(data), len(data[0])
    q = deque([(start[0], start[1], 0)])
    visited = set()
    results = {}

    while q:
        x, y, dist = q.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        cell = data[x][y]
        if 'A' <= cell <= 'Z' and cell.lower() not in collected_keys:
            continue  
        if 'a' <= cell <= 'z' and cell not in collected_keys:
            results[cell] = (dist, (x, y))
            continue

        for nx, ny in neighbors(x, y):
            if 0 <= nx < rows and 0 <= ny < cols and data[nx][ny] != '#':
                q.append((nx, ny, dist + 1))

    return results

def min_steps_to_collect_all_keys(data):
    rows, cols = len(data), len(data[0])
    key_locations = {}
    robots = []

    for i in range(rows):
        for j in range(cols):
            c = data[i][j]
            if c == '@':
                robots.append((i, j))
            elif 'a' <= c <= 'z':
                key_locations[c] = (i, j)

    total_keys = len(key_locations)
    all_keys_mask = (1 << total_keys) - 1
    key_to_bit = {k: 1 << i for i, k in enumerate(sorted(key_locations))}

    heap = [(0, tuple(robots), 0)]  # (steps, robot positions, collected_keys_mask)
    visited = set()

    while heap:
        steps, positions, keys_mask = heapq.heappop(heap)
        state = (positions, keys_mask)
        if state in visited:
            continue
        visited.add(state)

        if keys_mask == all_keys_mask:
            return steps

        collected_keys = set(k for k, b in key_to_bit.items() if keys_mask & b)

        for i, (x, y) in enumerate(positions):
            reachable = bfs(data, (x, y), collected_keys)
            for key, (dist, new_pos) in reachable.items():
                bit = key_to_bit[key]
                if keys_mask & bit:
                    continue  

                new_positions = list(positions)
                new_positions[i] = new_pos
                new_keys_mask = keys_mask | bit
                heapq.heappush(heap, (steps + dist, tuple(new_positions), new_keys_mask))

    return -1

def main():
    data = get_input()
    result = min_steps_to_collect_all_keys(data)
    print(result)

if __name__ == '__main__':
    main()
