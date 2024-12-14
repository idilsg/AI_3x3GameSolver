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
        self.cost = cost  # Hareket maliyeti
        self.priority = self.depth + self.cost

    def __lt__(self, other):
        return self.priority < other.priority


def manhattan_distance(state, goal):
    """Mevcut durumun hedef duruma Manhattan mesafesini hesaplar."""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                # Hedef durumdaki (i,j) konumunun hedef yerini bulalım
                x, y = [(x, y) for x in range(3) for y in range(3) if goal[x][y] == state[i][j]][0]
                distance += abs(x - i) + abs(y - j)
    return distance


def get_blank_positions(state):
    """Boş karelerin (0) konumlarını döndürür."""
    positions = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                positions.append((i, j))
    return positions


def move_blank(state, direction):
    """Boş kareyi belirtilen yöne hareket ettirir."""
    blank_positions = get_blank_positions(state)
    for x, y in blank_positions:
        dx, dy = directions[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = deepcopy(state)
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            return new_state
    return None


def validate_input(flat_input):
    """Kullanıcı girişini kontrol eder ve geçerli bir 3x3 matris döndürür."""
    try:
        numbers = list(map(int, flat_input.split()))
    except ValueError:
        raise ValueError("Hatalı giriş: Lütfen sadece sayılar girin.")
    if len(numbers) != 9:
        raise ValueError("Hatalı giriş: Lütfen 9 adet sayı girin.")
    unique_numbers = set(numbers)
    if len(unique_numbers - {0}) != len(numbers) - numbers.count(0):
        raise ValueError("Hatalı giriş: Boş kutular (0) hariç aynı sayıdan birden fazla olmamalı.")
    if numbers.count(0) < 1:
        raise ValueError("Hatalı giriş: En az bir adet boş kutu (0) olmalı.")
    non_zero_numbers = sorted(num for num in numbers if num != 0)
    if non_zero_numbers != list(range(1, len(non_zero_numbers) + 1)):
        raise ValueError("Hatalı giriş: Boş kutular hariç girilen sayılar ardışık olmalı.")
    return [numbers[:3], numbers[3:6], numbers[6:]]


def validate_goal(start, goal):
    """Başlangıç ve hedef durumların aynı sayı kümesini içerip içermediğini kontrol eder."""
    start_numbers = sorted(num for row in start for num in row)
    goal_numbers = sorted(num for row in goal for num in row)
    if start_numbers != goal_numbers:
        raise ValueError("Hatalı giriş: Başlangıç ve hedef durumlar aynı sayı kümesine sahip olmalı.")
    if start == goal:
        raise ValueError("Hatalı giriş: Hedef durum, başlangıç durumuyla aynı olmamalı. Yerler farklı olmalı.")


def expand_node(node, goal):
    """Mevcut düğümden hareketleri genişletir."""
    expanded_nodes = []
    for direction in directions.keys():
        new_state = move_blank(node.state, direction)
        if new_state:
            move_cost = 2 if direction in ["L", "R"] else 1
            new_node = Node(
                state=new_state,
                parent=node,
                move=direction,
                depth=node.depth + 1,
                cost=node.cost + move_cost
            )
            new_node.priority = new_node.cost + manhattan_distance(new_state, goal)
            expanded_nodes.append(new_node)
    return expanded_nodes


def solve_puzzle_with_sequence(initial_state, goal_state):
    """Bulmacayı ardışık sayı sırasıyla çözmeye çalışır."""
    current_state = deepcopy(initial_state)
    print("Başlangıç Durumu:")
    for row in current_state:
        print(row)
    print()

    frontier = PriorityQueue()
    root = Node(state=current_state, cost=manhattan_distance(current_state, goal_state))
    frontier.put(root)
    explored = set()

    while not frontier.empty():
        node = frontier.get()
        explored.add(tuple(map(tuple, node.state)))

        # Hedef duruma ulaşıldığında çözüm yolunu yazdır
        if node.state == goal_state:
            path = []
            while node:
                path.append(node)
                node = node.parent
            path.reverse()  # Çözüm yolunu doğru sıraya sok

            print("Çözüm Bulundu! Adımlar:")
            total_cost = 0
            for step, step_node in enumerate(path):
                if step_node.move:
                    move_cost = 2 if step_node.move in ["L", "R"] else 1
                    total_cost += move_cost
                    print(f"Adım {step}: Hareket {step_node.move}")
                    print(f"Maliyet: {move_cost}, Toplam Maliyet: {total_cost}")
                for row in step_node.state:
                    print(row)
                print()
            return

        # Çocuk düğümleri genişlet
        for child in expand_node(node, goal_state):
            if tuple(map(tuple, child.state)) not in explored:
                frontier.put(child)

    # Eğer bu noktaya ulaşılırsa çözüm bulunamamış demektir
    print("Çözüm bulunamadı.")


if __name__ == "__main__":
    while True:
        try:
            print("Başlangıç durumunu düz bir şekilde (9 sayı) girin (örnek: 1 2 3 0 0 0 0 0 0):")
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
            validate_goal(start, goal)
            break
        except ValueError as e:
            print(e)
    solve_puzzle_with_sequence(start, goal)
