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
    flat_goal = [num for row in goal for num in row]  # Hedef durumu düz bir listeye dönüştür
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                try:
                    target_i, target_j = divmod(flat_goal.index(state[i][j]), 3)
                    distance += abs(target_i - i) + abs(target_j - j)
                except ValueError:
                    raise ValueError(f"Hata: {state[i][j]} hedef durumunda bulunamadı.")
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
    if sorted(num for row in start for num in row) != sorted(num for row in goal for num in row):
        raise ValueError("Hatalı giriş: Başlangıç ve hedef durumlar aynı sayı kümesine sahip olmalı.")


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
    frontier = PriorityQueue()
    # Başlangıç maliyeti 0 olarak ayarlandı
    root = Node(state=initial_state, cost=0)
    frontier.put(root)
    explored = set()
    step_count = 0  # Adım sayacı
    print_limit = 10  # Sadece ilk 10 adım yazdırılsın

    print("Çözüm aranmaya başlandı...\n")

    while not frontier.empty():
        node = frontier.get()
        explored.add(tuple(map(tuple, node.state)))

        # İlk 10 adımı yazdır
        if step_count < print_limit:
            print(f"Adım {step_count}:")
            print(f"Genişletilen düğüm:\n{node.state}")
            if node.move:
                print(f"Hareket: {node.move}")
            print(f"Toplam maliyet: {node.cost}")
            print("------")
        step_count += 1

        # Hedef duruma ulaşıldığında çözüm yolunu yazdır
        if node.state == goal_state:
            path = []
            while node:
                path.append(node)
                node = node.parent
            path.reverse()  # Çözüm yolunu doğru sıraya sok

            print("\nÇözüm Bulundu! Adımlar:")
            total_cost = 0
            for step, step_node in enumerate(path):
                if step_node.move:
                    move_cost = 2 if step_node.move in ["L", "R"] else 1
                    total_cost += move_cost
                    print(f"Adım {step}: Hareket {step_node.move}")
                    print(f"Maliyet: {move_cost}, Toplam Maliyet: {total_cost}")
                for row in step_node.state:
                    print(f"{' '.join(map(str, row))}")

                print()
            return

        # Çocuk düğümleri genişlet
        for child in expand_node(node, goal_state):
            if tuple(map(tuple, child.state)) not in explored:
                frontier.put(child)

    # Eğer bu noktaya ulaşılırsa çözüm bulunamamış demektir
    print("\nÇözüm bulunamadı.")
    print(f"Toplam 10 adım genişletildi.")


if __name__ == "__main__":
    print("Lütfen başlangıç durumunu girin (örnek: 1 0 2 0 3 0 0 0 0):")
    try:
        start_input = input()
        start_state = validate_input(start_input)

        print("Lütfen hedef durumunu girin (örnek: 0 0 0 0 1 2 0 0 3):")
        goal_input = input()
        goal_state = validate_input(goal_input)

        # Geçerli giriş kontrolü
        validate_goal(start_state, goal_state)

        # Bulmacayı çöz
        solve_puzzle_with_sequence(start_state, goal_state)
    except ValueError as e:
        print(f"Hata: {e}")
