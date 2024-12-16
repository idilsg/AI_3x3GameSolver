from copy import deepcopy

# Yön matrisleri: Yukarı, Aşağı, Sol, Sağ
directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}


def print_matrix(matrix):
    """Puzzle durumunu matris formatında yazdırır."""
    for row in matrix:
        print(" ".join(str(num) if num != 0 else "_" for num in row))
    print("-" * 10)


def manhattan_distance(state, goal):
    """Mevcut durumun hedef duruma Manhattan mesafesini hesaplar."""
    distance = 0
    flat_goal = [num for row in goal for num in row]
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                try:
                    target_i, target_j = divmod(flat_goal.index(state[i][j]), 3)
                    distance += abs(target_i - i) + abs(target_j - j)
                except ValueError:
                    raise ValueError(f"Hata: {state[i][j]} hedef durumunda bulunamadı.")
    return distance


def move_blank(state, direction):
    """Boş kareyi belirtilen yöne hareket ettirir."""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                dx, dy = directions[direction]
                new_x, new_y = i + dx, j + dy
                if 0 <= new_x < 3 and 0 <= new_y < 3:
                    new_state = deepcopy(state)
                    new_state[i][j], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[i][j]
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

    return [numbers[:3], numbers[3:6], numbers[6:]]


def validate_goal(start, goal):
    """Başlangıç ve hedef durumların aynı sayı kümesini içerip içermediğini kontrol eder."""
    if sorted(num for row in start for num in row) != sorted(num for row in goal for num in row):
        raise ValueError("Başlangıç ve hedef durumlar aynı sayı kümesine sahip olmalı.")


def solve_puzzle_step_by_step(initial_state, goal_state):
    """Puzzle'ı adım adım çöz ve hareketleri ekrana yazdır."""
    current_state = [row[:] for row in initial_state]  # Başlangıç durumunun kopyası
    visited_states = set()  # Daha önce ziyaret edilen durumları kaydetmek için
    visited_states.add(tuple(tuple(row) for row in current_state))  # Başlangıç durumu eklenir

    print("Başlangıç durumu:")
    print_matrix(current_state)

    def get_tile_position(state, tile):
        """Bir taşın mevcut pozisyonunu bul."""
        for i, row in enumerate(state):
            if tile in row:
                return i, row.index(tile)
        return None

    def is_tile_in_correct_position(state, tile):
        """Bir taş doğru pozisyonda mı?"""
        current_pos = get_tile_position(state, tile)
        goal_pos = get_tile_position(goal_state, tile)
        return current_pos == goal_pos

    while current_state != goal_state:
        best_move = None
        best_priority = float('inf')  # En düşük önceliği arıyoruz

        for direction in directions.keys():
            new_state = move_blank(current_state, direction)

            if new_state and tuple(tuple(row) for row in new_state) not in visited_states:
                # Yanlış pozisyonda olan taşların toplam mesafesini hesapla
                total_misplaced_distance = sum(
                    manhattan_distance(new_state, goal_state)
                    for tile in range(1, 9)  # 1'den 8'e kadar olan taşlar için
                    if not is_tile_in_correct_position(new_state, tile)
                )
                if total_misplaced_distance < best_priority:
                    best_priority = total_misplaced_distance
                    best_move = (new_state, direction)

        if best_move is None:
            raise ValueError("Hata: Hareket bulunamadı, puzzle çözülemiyor.")

        # Hareketi uygula
        current_state, move = best_move
        visited_states.add(tuple(tuple(row) for row in current_state))  # Yeni durumu ziyaret edilenlere ekle

        print(f"Hareket: {move}")
        print_matrix(current_state)

    print("Çözüm tamamlandı!")
    return


def main():
    try:
        initial_input = input("Lütfen başlangıç durumunu girin (örnek: 1 0 2 0 3 0 0 0 0): ")
        initial_state = validate_input(initial_input)

        goal_input = input("Lütfen hedef durumunu girin (örnek: 0 0 0 0 1 2 0 0 3): ")
        goal_state = validate_input(goal_input)

        validate_goal(initial_state, goal_state)
        print("Başlangıç ve hedef durumlar doğrulandı.")

        # Puzzle'ı çöz
        solve_puzzle_step_by_step(initial_state, goal_state)

    except ValueError as e:
        print(f"Hata: {e}")


if __name__ == "__main__":
    main()
