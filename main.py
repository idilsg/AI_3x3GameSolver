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


def solve_puzzle_step_by_step(initial_state, goal_state):
    current_state = [row[:] for row in initial_state]  # Başlangıç durumunun bir kopyasını oluştur
    total_cost = 0  # Toplam maliyet

    def find_position(matrix, value):
        """Bir matris içinde bir değerin pozisyonunu bul."""
        for i, row in enumerate(matrix):
            if value in row:
                return i, row.index(value)
        return None

    def calculate_cost(current_pos, goal_pos):
        """Pozisyonlar arasındaki maliyeti hesapla."""
        return abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])

    moves_log = []  # Hareketleri kaydetmek için bir liste

    while True:
        all_at_goal = True  # Tüm sayıların hedefte olup olmadığını kontrol etmek için bir bayrak

        for number in range(1, 10):  # 1'den 9'a kadar sırayla sayılar
            current_pos = find_position(current_state, number)
            goal_pos = find_position(goal_state, number)

            # Eğer sayı hedefteyse atla
            if current_pos == goal_pos:
                moves_log.append(f"{number} zaten hedef konumda.")
                continue

            # Hedefte olmayan bir sayı varsa tüm sayıların hedefte olmadığını işaretle
            all_at_goal = False

            # Öncelikle sütun farkını gider
            if current_pos[1] != goal_pos[1]:
                direction = "sağa" if goal_pos[1] > current_pos[1] else "sola"
                new_pos = (current_pos[0], current_pos[1] + (1 if direction == "sağa" else -1))
                current_state[current_pos[0]][current_pos[1]], current_state[new_pos[0]][new_pos[1]] = (
                    current_state[new_pos[0]][new_pos[1]],
                    current_state[current_pos[0]][current_pos[1]],
                )
                total_cost += 1
                moves_log.append(
                    f"{number} {direction} hareket etti. Yeni durum:\n{format_puzzle(current_state)}\nO adımdaki toplam maliyet: {total_cost}"
                )
                break  # Bir adım yapıldıktan sonra diğer sayılara geçmek için döngüden çık

            # Daha sonra satır farkını gider
            if current_pos[0] != goal_pos[0]:
                direction = "aşağı" if goal_pos[0] > current_pos[0] else "yukarı"
                new_pos = (current_pos[0] + (1 if direction == "aşağı" else -1), current_pos[1])
                current_state[current_pos[0]][current_pos[1]], current_state[new_pos[0]][new_pos[1]] = (
                    current_state[new_pos[0]][new_pos[1]],
                    current_state[current_pos[0]][current_pos[1]],
                )
                total_cost += 1
                moves_log.append(
                    f"{number} {direction} hareket etti. Yeni durum:\n{format_puzzle(current_state)}\nO adımdaki toplam maliyet: {total_cost}"
                )
                break  # Bir adım yapıldıktan sonra diğer sayılara geçmek için döngüden çık

        # Eğer tüm sayılar hedef konumdaysa döngüyü kır
        if all_at_goal:
            moves_log.append("Tüm sayılar hedef konumda!")
            break

    # Çözüm bilgilerini döndür
    moves_log.append(f"Toplam maliyet: {total_cost}")
    return moves_log


def format_puzzle(puzzle):
    """Puzzle durumunu formatlayarak yazdır."""
    return "\n".join([" ".join(map(str, row)) for row in puzzle])


def main():
    # Kullanıcıdan başlangıç ve hedef durumlarını al
    initial_input = input("Lütfen başlangıç durumunu girin (örnek: 1 0 2 0 3 0 0 0 0): ")
    initial_state = [list(map(int, initial_input.split()))[i:i+3] for i in range(0, 9, 3)]

    goal_input = input("Lütfen hedef durumunu girin (örnek: 0 0 0 0 1 2 0 0 3): ")
    goal_state = [list(map(int, goal_input.split()))[i:i+3] for i in range(0, 9, 3)]

    # Çözümü bul ve adımları yazdır
    moves_log = solve_puzzle_step_by_step(initial_state, goal_state)
    for log in moves_log:
        print(log)


if __name__ == "__main__":
    main()
