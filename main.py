from copy import deepcopy
from queue import PriorityQueue

# Yön matrisleri: Yukarı, Aşağı, Sol, Sağ
directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}

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
    """Mevcut durumun Manhattan mesafesini hesaplar."""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def get_blank_position(state):
    """Boş karenin (0) konumunu döndürür."""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def move_blank(state, direction):
    """Boş kareyi belirtilen yöne hareket ettirir."""
    x, y = get_blank_position(state)
    dx, dy = directions[direction]
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < 3 and 0 <= new_y < 3:
        new_state = deepcopy(state)
        new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
        return new_state
    return None

def get_tile_order(initial_state):
    """Taş sırasını belirler."""
    tile_order = [tile for row in initial_state for tile in row if tile != 0]
    return tile_order

def validate_input(flat_input):
    """Kullanıcı girişini kontrol eder ve geçerli bir 3x3 matris döndürür."""
    try:
        numbers = list(map(int, flat_input.split()))
    except ValueError:
        raise ValueError("Hatalı giriş: Lütfen sadece sayılar girin.")

    if len(numbers) != 9:
        raise ValueError("Hatalı giriş: Lütfen 9 adet sayı girin.")

    if sorted(numbers) != list(range(9)):
        raise ValueError("Hatalı giriş: Sayılar 0'dan 8'e kadar ve birbirinden farklı olmalıdır.")

    return [numbers[:3], numbers[3:6], numbers[6:]]

def expand_node(node, tile_order):
    """Mevcut düğümden belirtilen taş sırasına göre hareketleri genişletir."""
    expanded_nodes = []
    for tile in tile_order:  # Taş sırasını takip et
        tile_pos = [(i, j) for i in range(3) for j in range(3) if node.state[i][j] == tile]
        if not tile_pos:
            continue
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

def a_star_search(initial_state, goal_state):
    """A* algoritmasını kullanarak bulmaca çözümü arar."""
    root = Node(state=initial_state, cost=manhattan_distance(initial_state))
    frontier = PriorityQueue()
    frontier.put(root)
    explored = set()
    expansions = 0

    tile_order = get_tile_order(initial_state)  # Taş sırasını al

    while not frontier.empty() and expansions < 10:
        node = frontier.get()
        explored.add(tuple(map(tuple, node.state)))

        print(f"\nExpanded Node {expansions + 1}:")
        for row in node.state:
            print(row)
        print(f"Move: {node.move}, g(n): {node.depth}, h(n): {node.cost}, f(n): {node.priority}\n")

        if node.state == goal_state:
            return node

        for child in expand_node(node, tile_order):
            if tuple(map(tuple, child.state)) not in explored:
                frontier.put(child)

        expansions += 1

    return None

def print_solution(solution_node):
    """Çözüm yolunu ve her adımda düğüm genişlemelerini yazdırır."""
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
    while True:
        try:
            print("Başlangıç durumunu düz bir şekilde (9 sayı) girin (örnek: 6 2 8 4 7 1 0 3 5):")
            start_input = input()
            start = validate_input(start_input)
            break
        except ValueError as e:
            print(e)

    while True:
        try:
            print("Hedef durumunu düz bir şekilde (9 sayı) girin (örnek: 1 2 3 4 5 6 7 8 0):")
            goal_input = input()
            goal = validate_input(goal_input)
            break
        except ValueError as e:
            print(e)

    solution = a_star_search(start, goal)
    if solution:
        print_solution(solution)
    else:
        print("\nÇözüm bulunamadı veya 10 düğüm genişletildi.")
