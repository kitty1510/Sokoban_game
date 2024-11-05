from collections import deque
import tracemalloc
import time
import os
DIRECTION_MAP = {
    'u': (-1, 0),
    'd': (1, 0),
    'l': (0, -1),
    'r': (0, 1)
}

def move(x, y, direction):
    dx, dy = DIRECTION_MAP[direction]
    return x + dx, y + dy

class SokobanBFS:
    def __init__(self, grid, start, stones, switches):
        self.grid = grid
        self.start = start
        self.stones = stones  
        self.switches = switches
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.generated_nodes = 0
        

    def is_valid_move(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] != '#'

    def bfs(self):
        queue = deque([(self.start, frozenset(self.stones), "", 0, 0)])  # (vị trí người chơi, vị trí đá, đường đi, tổng trọng lượng, số bước)
        visited = set()
        visited.add((self.start, frozenset(self.stones)))
        self.generated_nodes = 0

        while queue:
            (x, y), stones, path, total_weight, steps = queue.popleft()

            # Kiểm tra nếu tất cả viên đá đã ở vị trí công tắc
            if all(stone[0] in self.switches for stone in stones):
                return path, total_weight, steps, self.generated_nodes

            for direction in DIRECTION_MAP.keys():
                new_x, new_y = move(x, y, direction)

                # Kiểm tra xem người chơi có thể di chuyển đến vị trí mới không
                if self.is_valid_move(new_x, new_y):
                    # Trường hợp đẩy đá
                    stone_positions = {stone[0]: stone[1] for stone in stones}
                    if (new_x, new_y) in stone_positions:
                        stone_new_x, stone_new_y = move(new_x, new_y, direction)

                        # Kiểm tra xem viên đá có thể được đẩy đến vị trí tiếp theo không
                        if self.is_valid_move(stone_new_x, stone_new_y) and (stone_new_x, stone_new_y) not in stone_positions:
                            new_stones = set(stones)
                            new_stones.remove(((new_x, new_y), stone_positions[(new_x, new_y)]))
                            new_stones.add(((stone_new_x, stone_new_y), stone_positions[(new_x, new_y)]))

                            # Lấy trọng lượng của viên đá đang đẩy
                            stone_weight = stone_positions[(new_x, new_y)]

                            # Cộng trọng lượng viên đá vào ngay khi đẩy đá thành công
                            current_weight = total_weight + stone_weight

                            # Thêm trạng thái mới vào hàng đợi nếu không phải deadlock
                            new_state = ((new_x, new_y), frozenset(new_stones))
                            if new_state not in visited:
                                queue.append((new_state[0], new_state[1], path + direction.upper(), current_weight, steps + 1))
                                self.generated_nodes += 1
                                visited.add(new_state)
                    else:
                        # Kiểm tra trạng thái mới trước khi thêm vào hàng đợi
                        new_state = ((new_x, new_y), frozenset(stones))
                        if new_state not in visited:
                            queue.append((new_state[0], new_state[1], path + direction, total_weight, steps + 1))
                            self.generated_nodes += 1
                            visited.add(new_state)

        return None  # Nếu không tìm thấy lời giải

# Các hàm đọc và ghi file như đã có ở trên
# Hàm đọc dữ liệu từ file đầu vào
def read_input_file(filename):
    with open(filename, 'r') as f:
        weights = list(map(int, f.readline().strip().split()))
        grid = [list(line.rstrip()) for line in f if line.strip()]

    start = None
    stones = set()
    switches = set()

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                start = (i, j)
            elif cell == '$':
                stones.add(((i, j), weights[len(stones)]))  # Thêm vị trí và trọng lượng của viên đá
            elif cell == '.':
                switches.add((i, j))
            elif cell == '*':
                # Viên đá đã ở vị trí công tắc, thêm cả vào danh sách công tắc và viên đá
                switches.add((i, j))
                stones.add(((i, j), weights[len(stones)]))
            elif cell == '+':
                start = (i, j)
                switches.add((i, j))

    return grid, start, stones, switches

# Hàm ghi dữ liệu ra file đầu ra
def write_output_file(filename, algorithm_name, path, steps, weight, nodes, time_taken, memory):
    with open(filename, 'w') as f:
        f.write(f"{algorithm_name}\n")
        f.write(f"Steps: {steps}, Weight: {weight}, Node: {nodes}, Time (ms): {time_taken:.2f}, Memory (MB): {memory:.2f}\n")
        f.write("".join(path) + "\n")

# Hàm chính để chạy BFS và ghi kết quả ra file

def main(input_file, output_file):
    tracemalloc.start()
    start_time = time.time()

    # Đọc input
    grid, start, stones, switches = read_input_file(input_file)

    # Chạy BFS
    solver = SokobanBFS(grid, start, stones, switches)
    result = solver.bfs()

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if result:
        path, total_weight, steps, generated_nodes = result
        time_taken = (end_time - start_time) * 1000  # ms
        memory_used = peak / (1024 * 1024)  # MB

        # Ghi kết quả ra file
        write_output_file(output_file, "BFS", path, steps, total_weight, generated_nodes, time_taken, memory_used)
    else:
        with open(output_file, 'w') as f:
            f.write("BFS\nNo Solution Found")

# input_file_name = 'D:\HK1 2024-2025\CSTTNT\project01\input\input-04.txt'
# output_file_name = 'output.txt'
# main(input_file_name, output_file_name)
