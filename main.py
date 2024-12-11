from copy import deepcopy
from queue import PriorityQueue

# yön matrisleri: yukarı, aşağı, sol, sağ
directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}

# Hedef matris
end = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


class Node:
    def __init__(self, state, parent=None, move=None, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost  # Manhattan distance
        self.priority = self.depth + self.cost

    def __lt__(self, other):
        return self.priority < other.priority


def manhattan_distance(state):
    """current manhattan distance"""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance


def get_blank_position(state):
    """boş kısım"""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def move_blank(state, direction):
    """boş kısım hareket ettirilir"""
    x, y = get_blank_position(state)
    dx, dy = directions[direction]
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < 3 and 0 <= new_y < 3:
        new_state = deepcopy(state)
        new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
        return new_state
    return None


def expand_node(node):
    """ANLAMADIM"""
    expanded_nodes = []
    for direction in directions.keys():
        new_state = move_blank(node.state, direction)
        if new_state:
            cost = 1 if direction in ["U", "D"] else 2
            new_node = Node(
                state=new_state,
                parent=node,
                move=direction,
                depth=node.depth + cost,
                cost=manhattan_distance(new_state)
            )
            expanded_nodes.append(new_node)
    return expanded_nodes


def a_star_search(initial_state):
    """A* algoritamsı ile çözüm"""
    root = Node(state=initial_state, cost=manhattan_distance(initial_state))
    frontier = PriorityQueue()
    frontier.put(root)
    explored = set()
    expansions = 0

    while not frontier.empty() and expansions < 10:
        node = frontier.get()
        explored.add(tuple(map(tuple, node.state)))
        print(f"\nExpanded Node {expansions + 1}:")
        for row in node.state:
            print(row)
        print(f"Move: {node.move}, g(n): {node.depth}, h(n): {node.cost}, f(n): {node.priority}\n")
        if node.state == end:
            return node
        for child in expand_node(node):
            if tuple(map(tuple, child.state)) not in explored:
                frontier.put(child)
        expansions += 1
    return None


def print_solution(solution_node):
    """çözüm"""
    path = []
    node = solution_node
    while node:
        path.append(node)
        node = node.parent
    path.reverse()
    print("\nSolution Path:")
    for step in path:
        print(f"Move: {step.move}, g(n): {step.depth}, h(n): {step.cost}, f(n): {step.priority}")
        for row in step.state:
            print(row)
        print()


if __name__ == "__main__":
    # kullanıcıdan initial state alma
    start = [[1, 0, 2], [0, 3, 0], [0, 0, 0]]
    solution = a_star_search(start)
    if solution:
        print_solution(solution)
    else:
        print("\nÇözüm bulunamadı veya 10 düğüm genişletildi.")
