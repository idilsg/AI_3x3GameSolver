from copy import deepcopy


directions = {
    "U": (-1, 0), #up
    "D": (1, 0), #down
    "L": (0, -1), #left
    "R": (0, 1) #right
}


def print_matrix(matrix):
    """puzzle'ı matris formunda yazdırmak için"""
    for row in matrix:
        print(" ".join(str(num) if num != 0 else "_" for num in row))
    print("-" * 10)


def manhattan_distance(state, goal):
    distance = 0
    flat_goal = [num for row in goal for num in row]
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                try:
                    target_i, target_j = divmod(flat_goal.index(state[i][j]), 3)
                    distance += abs(target_i - i) + abs(target_j - j)
                except ValueError:
                    raise ValueError(f"Error: {state[i][j]}")
    return distance


def move_blank(state, direction):
    """boş karenin hareketi için"""
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
    """kullanıcı girişleri için kontroller"""
    err = 1
    try:
        numbers = list(map(int, flat_input.split()))
    except ValueError:
        raise ValueError("Invalid entry: Please enter numbers only.")

    while err == 1:

        if len(numbers) != 9:
            print("Invalid entry: Please enter 9 numbers.")
        else:
            err = 0

        unique_numbers = set(numbers)
        if len(unique_numbers - {0}) != len(numbers) - numbers.count(0):
            print("Invalid entry: There should not be more than one of the same number except for empty boxes (0).")
        else:
            err = 0

        if numbers.count(0) < 1:
            print("Invalid entry: There must be at least one empty box (0).")
        else:
            err = 0

        non_zero_numbers = sorted(num for num in numbers if num != 0)
        if non_zero_numbers != list(range(1, len(non_zero_numbers) + 1)):
            print("Invalid entry: Numbers entered must be consecutive, except for empty boxes.")
        else:
            err = 0

    return [numbers[:3], numbers[3:6], numbers[6:]]


def validate_goal(start, goal):
    """initial ve goal'da aynı sayılar olup olmadığını kontrol etmek için"""
    if sorted(num for row in start for num in row) != sorted(num for row in goal for num in row):
        raise ValueError("Invalid input: Initial and goal states must have the same set of numbers.")


def find_blank(state):
    """boş kutular için"""
    for i, row in enumerate(state):
        if 0 in row:
            return i, row.index(0)
    return None


def get_tile_position(state, tile):
    """dolu olanlar için"""
    for i, row in enumerate(state):
        if tile in row:
            return i, row.index(tile)
    return None


def solve_puzzle_step_by_step(initial_state, goal_state):
    """çözümü"""
    current_state = [row[:] for row in initial_state]  # başlangıç durumunun kopyası
    visited_states = set()  # daha önce ziyaret edilen durumları kaydetmek için
    visited_states.add(tuple(tuple(row) for row in current_state))  # başlangıç durumu eklenir

    print("\nInitial state:")
    print_matrix(current_state)

    tile_to_move = 1
    total_cost = 0
    total_move = 0

    while current_state != goal_state:
        best_move = None
        best_priority = float('inf')  # en düşük önceliği arıyoruz

        for tile in range(tile_to_move, 9):
            current_pos = get_tile_position(current_state, tile)
            goal_pos = get_tile_position(goal_state, tile)

            if current_pos != goal_pos:  # sayı doğru pozisyonda değilse
                # eğer aynı satırda değilse önce satırda değişiklik yapılacak
                if current_pos[1] == goal_pos[1]:
                    for direction in ['U', 'D']:
                        new_state = move_blank(current_state, direction)
                        if new_state:
                            total_misplaced_distance = manhattan_distance(new_state, goal_state)
                            if total_misplaced_distance < best_priority:
                                best_priority = total_misplaced_distance
                                best_move = (new_state, direction)
                                total_cost = total_cost + 1 # cost hesaplama için
                                total_move = total_move + 1
                # eğer aynı satırda ise sadece sütunda değişiklik yapılacak
                elif current_pos[0] == goal_pos[0]:
                    for direction in ['L', 'R']:
                        new_state = move_blank(current_state, direction)
                        if new_state:
                            total_misplaced_distance = manhattan_distance(new_state, goal_state)
                            if total_misplaced_distance < best_priority:
                                best_priority = total_misplaced_distance
                                best_move = (new_state, direction)
                                total_cost = total_cost + 2  # cost hesaplama için
                                total_move = total_move + 1


        if best_move is None:
            raise ValueError("Error: No valid move found, puzzle cannot be solved.")

        # hareketi uygulamak için
        current_state, move = best_move
        visited_states.add(tuple(tuple(row) for row in current_state))

        print(f"\nMove: {move}")
        print_matrix(current_state)

        # toplam maliyeti artır
        # total_cost += best_priority

        # sıradaki sayıya geç
        tile_to_move = tile_to_move + 1 if tile_to_move < 8 else 1

        if total_move == 10:
            print('Solution cannot found.')
            break

    print("Solution completed!")
    print(f"Total cost: {total_cost}")  # toplam maliyet


def main():
    try:
        initial_input = input("Enter the initial state (exp: 1 2 3 0 0 0 0 0 0): ")
        initial_state = validate_input(initial_input)

        goal_input = input("Enter the goal state (exp: 0 0 0 1 2 3 0 0 0): ")
        goal_state = validate_input(goal_input)

        validate_goal(initial_state, goal_state)
        print("Valid initial and goal state.")

        solve_puzzle_step_by_step(initial_state, goal_state)

    except ValueError as e:
        print(f"Hata: {e}")


if __name__ == "__main__":
    main()
