from copy import deepcopy

# Direction matrix
directions = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
# Target matrix
end = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


# Node class representing a state of the puzzle
class Node:
    def __init__(self, current_node, previous_node, g, h, direction):
        self.current_node = current_node  # Current state of the puzzle
        self.previous_node = previous_node  # Previous state
        self.g = g  # Cost to reach this node (steps taken so far)
        self.h = h  # Heuristic cost (estimated cost to goal)
        self.direction = direction  # Direction taken to reach this node

    def f(self):
        return self.g + self.h  # Total cost (g + h)


def get_pos(current_state, element):
    """Find the position of a given element in the puzzle."""
    for row in range(len(current_state)):
        if element in current_state[row]:
            return row, current_state[row].index(element)


def manhattan_cost(current_state):
    """Calculate the Manhattan distance heuristic cost."""
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(end, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost


def get_adjacent_nodes(node):
    """Generate adjacent nodes by moving the empty tile."""
    adjacent_nodes = []
    empty_pos = get_pos(node.current_node, 0)

    for dir_key in directions.keys():
        new_pos = (empty_pos[0] + directions[dir_key][0], empty_pos[1] + directions[dir_key][1])
        if 0 <= new_pos[0] < len(node.current_node) and 0 <= new_pos[1] < len(node.current_node[0]):
            new_state = deepcopy(node.current_node)
            new_state[empty_pos[0]][empty_pos[1]] = node.current_node[new_pos[0]][new_pos[1]]
            new_state[new_pos[0]][new_pos[1]] = 0
            adjacent_nodes.append(Node(new_state, node.current_node, node.g + 1, manhattan_cost(new_state), dir_key))

    return adjacent_nodes


def get_best_node(open_set):
    """Select the node with the lowest f() value from the open set."""
    best_node = min(open_set.values(), key=lambda node: node.f())
    return best_node


def build_path(closed_set):
    """Reconstruct the path from the start state to the goal state."""
    node = closed_set[str(end)]
    path = []

    while node.direction:
        path.append({'direction': node.direction, 'node': node.current_node, 'g': node.g, 'h': node.h})
        node = closed_set[str(node.previous_node)]
    path.append({'direction': '', 'node': node.current_node, 'g': node.g, 'h': node.h})
    path.reverse()

    return path


def solve_puzzle(start_state):
    """Solve the puzzle using the A* search algorithm."""
    open_set = {str(start_state): Node(start_state, start_state, 0, manhattan_cost(start_state), "")}
    closed_set = {}

    while open_set:
        current_node = get_best_node(open_set)
        closed_set[str(current_node.current_node)] = current_node

        if current_node.current_node == end:
            return build_path(closed_set)

        for adj_node in get_adjacent_nodes(current_node):
            if str(adj_node.current_node) in closed_set:
                continue
            if str(adj_node.current_node) not in open_set or open_set[str(adj_node.current_node)].f() > adj_node.f():
                open_set[str(adj_node.current_node)] = adj_node

        del open_set[str(current_node.current_node)]


if __name__ == '__main__':
    # Example start state
    start = [[6, 2, 8],
             [4, 7, 1],
             [0, 3, 5]]

    solution_path = solve_puzzle(start)

    print(f'Total steps: {len(solution_path) - 1}')
    for step in solution_path:
        if step['direction']:
            print(f"Move: {step['direction']}, g: {step['g']}, h: {step['h']}, f: {step['g'] + step['h']}")
        for row in step['node']:
            print(row)
        print()
