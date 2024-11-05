from collections import deque
import heapq
import tracemalloc
import time


DIRECTION_MAP = {
    'u': (-1, 0),
    'd': (1, 0),
    'l': (0, -1),
    'r': (0, 1)
}

def move(x, y, direction):
    dx, dy = DIRECTION_MAP[direction]
    return x + dx, y + dy

class SokobanAStar:
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

    def heuristic(self, stones):
        # Hàm heuristic cải tiến: tính khoảng cách Manhattan từ mỗi viên đá đến công tắc gần nhất
        total_distance = 0
        for stone in stones:
            min_distance = float('inf')
            for switch in self.switches:
                distance = abs(stone[0][0] - switch[0]) + abs(stone[0][1] - switch[1])
                min_distance = min(min_distance, distance)
            total_distance += min_distance

        return total_distance


    def is_valid_push(self, stone_new_x, stone_new_y, stone_positions):
        # Kiểm tra xem viên đá có thể được đẩy đến vị trí tiếp theo không (không phải tường và không phải vị trí của viên đá khác)
        return self.is_valid_move(stone_new_x, stone_new_y) and (stone_new_x, stone_new_y) not in stone_positions

    def a_star(self):
        priority_queue = []
        # (vị trí của người chơi, vị trí các viên đá, đường đi, tổng trọng lượng, số bước) khởi tạo ban đầu
        start_state = (self.start, frozenset(self.stones), "", 0, 0)  
        heapq.heappush(priority_queue, (0, start_state))  # (priority, state)
        
        visited = set()
        generated_states = {}  # Để lưu trữ các trạng thái đã được sinh ra

        visited.add((self.start, frozenset(self.stones)))
        generated_states[(self.start, frozenset(self.stones))] = 0  # Lưu chi phí trạng thái ban đầu

        self.generated_nodes = 0

        while priority_queue:
            _, current_state = heapq.heappop(priority_queue)
            (x, y), stones, path, total_weight, steps = current_state

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

                        # Sử dụng hàm is_valid_push để kiểm tra viên đá có thể đẩy đến vị trí tiếp theo không
                        if self.is_valid_push(stone_new_x, stone_new_y, stone_positions):
                            new_stones = set(stones)
                            new_stones.remove(((new_x, new_y), stone_positions[(new_x, new_y)]))
                            new_stones.add(((stone_new_x, stone_new_y), stone_positions[(new_x, new_y)]))

                            

                            # Lấy trọng lượng của viên đá đang đẩy
                            stone_weight = stone_positions[(new_x, new_y)]
                            current_weight = total_weight + stone_weight
                            cost = steps + 1 + current_weight + self.heuristic(new_stones)  # f(n) = g(n) + h(n)

                            new_state = ((new_x, new_y), frozenset(new_stones), path + direction.upper(), current_weight, steps + 1)

                            # Kiểm tra nếu trạng thái này đã có với chi phí thấp hơn
                            new_state_key = ((new_x, new_y), frozenset(new_stones))
                            if new_state_key not in visited or generated_states[new_state_key] > cost:
                                heapq.heappush(priority_queue, (cost, new_state))
                                self.generated_nodes += 1
                                generated_states[new_state_key] = cost
                                visited.add(new_state_key)
                    else:
                        # Trường hợp di chuyển không đẩy
                        new_state_key = ((new_x, new_y), stones)
                        if new_state_key not in visited or generated_states[new_state_key] > steps + 1:
                            cost = steps + 1 + self.heuristic(stones)  # f(n) = g(n) + h(n)
                            new_state = ((new_x, new_y), stones, path + direction, total_weight, steps + 1)
                            heapq.heappush(priority_queue, (cost, new_state))
                            self.generated_nodes += 1
                            generated_states[new_state_key] = steps + 1
                            visited.add(new_state_key)
                        
        return None  # Nếu không tìm thấy lời giả

#hàm xử lí đầu vào
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

def write_output_file(filename, algorithm_name, path, steps, weight, nodes, time_taken, memory):
    with open(filename, 'w') as f:
        f.write(f"{algorithm_name}\n")
        f.write(f"Steps: {steps}, Weight: {weight}, Node: {nodes}, Time (ms): {time_taken:.2f}, Memory (MB): {memory:.2f}\n")
        f.write("".join(path) + "\n")

#hàm này kiểm tra đọc input đúng hay không
def write_grid_to_file(filename, grid):
    with open(filename, 'w') as f:
        for row in grid:
            f.write("".join(row) + "\n")

def main(input_file, output_file):
    tracemalloc.start()
    start_time = time.time()

    # Đọc input
    grid, start, stones, switches = read_input_file(input_file)

    # Chạy A*
    solver = SokobanAStar(grid, start, stones, switches)
    result = solver.a_star()

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if result:
        path, total_weight, steps, generated_nodes = result
        time_taken = (end_time - start_time) * 1000  # ms
        memory_used = peak / (1024 * 1024)  # MB

        # In kết quả ra màn hình
        # print(f"{'A-Star'}")
        # print(f"Steps: {steps}, Weight: {total_weight}, Node: {generated_nodes}, Time (ms): {time_taken:.2f}, Memory (MB): {memory_used:.2f}")
        # print("".join(path))

        # Ghi kết quả ra file
        write_output_file(output_file, "A-Star", path, steps, total_weight, generated_nodes, time_taken, memory_used)
    else:
        with open(output_file, 'w') as f:
            f.write("A-Star\nNo Solution Found")
        
#chạy hàm main

# input_file_name = 'D:\HK1 2024-2025\CSTTNT\project01\input\input-05.txt'
# output_file_name = 'output.txt'
# main(input_file_name, output_file_name)
