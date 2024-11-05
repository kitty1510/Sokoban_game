import tracemalloc
import time

'''
Y tuong chung:
B1: Tim duong tu da den cong tac
B2: Voi moi vi tri tren duong di tu da den cong tac, tim duong di tu nhan vat Ares den vi tri day da
B3: Day da
'''

# Cau truc du lieu chung de luu cac doi tuong trong me cung
class Object:
    def __init__(self, object_type, x, y, weight = 0):
        self.__object_type = object_type;
        self.__x = x;
        self.__y = y;
        self.__weight = weight
    
    # Hanh dong di chuyen
    def go(self, direction):
        dx, dy = Direction_Map.get_direction(direction)
        self.__x += dx
        self.__y += dy
        
    def get_object_type(self):
        return self.__object_type
    
    def set_object_type(self, object_type):
        self.__object_type = object_type
        
    def get_x(self):
        return self.__x
    
    def set_x(self, x):
        self.__x = x
    
    def get_y(self):
        return self.__y
    
    def set_y(self, y):
        self.__y = y
        
    def get_weight(self):
        return self.__weight
    
    def set_weight(self, weight):
        self.__weight = weight
    # def generate_actions(self):
    #     actions = {}
    #     actions['l'] = Object(self.object_type, self.x - 1, self.y)
    #     actions['r'] = Object(self.object_type, self.x + 1, self.y)
    #     actions['u'] = Object(self.object_type, self.x, self.y - 1)
    #     actions['d'] = Object(self.object_type, self.x, self.y + 1)
    #     return actions
        
# Anh xa huong di chuyen voi su thay doi toa do cua doi tuong
class Direction_Map:
    direction_map = {
        'l': (-1, 0),
        'u': (0, -1),
        'r': (1, 0),
        'd': (0, 1)
    }
    def __init__(self):
        pass
    
    @classmethod
    def get_direction(cls, direction):
        if direction not in cls.direction_map.keys():
            return (0, 0)
        else:
            return cls.direction_map[direction]

# Anh xa ky hieu tren tep input voi loai doi tuong
class Notation:
    notation = {
            '#': 'Wall',
            '$': 'Stone',
            ' ': 'Cell',
            '@': 'Ares',
            '.': 'Switch',
            '*': 'Stone_on_Switch',
            '+': 'Ares_on_Switch'
        }
    
    def __init__(self):
        pass
    
    @classmethod
    def get_object(cls, char, x, y):
        if char in cls.notation.keys():
            return Object(cls.notation[char], x, y)
        else:
            return None

# Lop chinh lam moi thu
class Maze:
    def __init__(self):
        self.Objects = []
        self.stone_num = 0
        self.width, self.height = 0, 0
    
    def read_input(self, file_name):
        # Read the input file and create a 2D maze as a graph
        with open(file_name, "rt") as file_object:
            # This is where to read the input
            str_stone_weighs = file_object.readline().strip()
            stone_weighs = str_stone_weighs.split(' ')
            x, y = 0, 0
            while (True):
                object_char = file_object.read(1)
                if not object_char: # doc that bai hoac da doc het tep
                    break   
                if object_char == '\n':
                    y += 1
                    self.width = max(x, self.width)
                    x = 0
                    continue
                object = Notation.get_object(object_char, x, y)
                self.Objects.append(object)
                if object.get_object_type() in ('Stone', 'Stone_on_Switch'):
                    object.set_weight(int(stone_weighs[self.stone_num]))
                    self.stone_num += 1
                x += 1
            self.height = y
            
    def find_object_by_type(self, type):
        return [obj for obj in self.Objects if obj.get_object_type() == type]
            
    # Kiem tra tinh hoan thien cua chuong trinh
    def is_complete(self):
        count = 0
        for obj in self.Objects:
            if obj.get_object_type() == 'Stone_on_Switch':
                count += 1
        return count == self.stone_num
    
    def find_object_by_pos(self, x, y):
        objects = []
        for obj in self.Objects:
            if obj.get_x() == x and obj.get_y() == y:
                if obj.get_object_type() != 'Cell' and len(objects) > 0:
                    objects.clear()
                objects.append(obj)
        return objects[0]

    
    # Kiem tra mot nuoc di thuong cua nhan vat Ares co hop le khong
    def is_valid_move(self, ares, direction):
        dx, dy = Direction_Map.get_direction(direction)
        if dx == 0 and dy == 0:
            return False
        obj_temp = self.find_object_by_pos(ares.get_x() + dx, ares.get_y() + dy)
        if obj_temp is None:
            return False
        if obj_temp.get_object_type() == 'Wall':
            return False
        else: return True
        
    # Kiem tra mot nuoc di cua nhan vat Ares co phai la nuoc day da
    def is_push_stone_move(self, ares, direction):
        dx, dy = Direction_Map.get_direction(direction)
        if dx == 0 and dy == 0:
            return False
        obj_temp = self.find_object_by_pos(ares.get_x() + dx, ares.get_y() + dy)
        if obj_temp.get_object_type() in ['Stone', 'Stone_on_Switch']:
            return True
        else: return False      
        
    # Kiem tra mot vien da co the duoc day theo huong nhat dinh khong
    def is_able_to_push(self, stone, direction):
        dx, dy = Direction_Map.get_direction(direction)
        if dx == 0 and dy == 0:
            return False
        # Xem xet kha nang di chuyen cua da (bi ket boi da khac hay boi tuong)
        obj_temp = self.find_object_by_pos(stone.get_x() + dx, stone.get_y() + dy)
        if obj_temp is None:
            return False
        if obj_temp.get_object_type() in ('Wall', 'Stone', 'Stone_on_Switch'):
            return False
        # Xem xet kha nang tiep can den vi tri day da
        obj_temp = self.find_object_by_pos(stone.get_x() - dx, stone.get_y() - dy)
        if obj_temp is None:
            return False
        if obj_temp.get_object_type() in ('Wall', 'Stone_on_Switch') or (obj_temp.get_object_type() == 'Stone' and obj_temp.get_weight() != -1):
            return False
        else: return True
    
    # Kiem tra mot vien da da duoc dat tren mot cong tac bat ky nao    
    def is_on_switch(self, stone):
        switches = self.find_object_by_type('Switch')
        for switch in switches:
            if switch.get_x() == stone.get_x() and switch.get_y() == stone.get_y():
                return switch
            else:
                return False
    
    # Kiem tra mot cuc da da vao ngo cut, khong the day theo bat ky huong nao nua        
    def is_no_longer_able_to_push(self, stone):
        for dir in Direction_Map.direction_map.keys():
            if self.is_able_to_push(stone, dir):
                return False
        return True
    
    # Tim duong di tu da den cong tac bang dfs 
    def dfs_for_stone_to_switch(self, stone):
        stone_temp = Object('Stone', stone.get_x(), stone.get_y(), stone.get_weight())
        stone.set_weight(-1) # Danh dau rang day la da dang duyet
        generated_nodes = 0
        if self.is_on_switch(stone):
            return [(stone.get_x(), stone.get_y(), '')], generated_nodes
        frontier = [(stone.get_x(), stone.get_y())]
        explored = []
        expansion_order = [(stone.get_x(), stone.get_y(), '')]
        while True:
            if len(frontier) == 0:
                stone.set_weight(stone_temp.get_weight())
                return [], generated_nodes
            stone_temp_x, stone_temp_y = frontier.pop(len(frontier) - 1)
            stone_temp.set_x(stone_temp_x)
            stone_temp.set_y(stone_temp_y)
            explored.append((stone_temp.get_x(), stone_temp.get_y()))
            for dir in Direction_Map.direction_map.keys():
                if self.is_able_to_push(stone_temp, dir):
                    dx, dy = Direction_Map.get_direction(dir)
                    child = Object(stone_temp.get_object_type(), stone_temp.get_x() + dx, stone_temp.get_y() + dy, stone_temp.get_weight())
                    generated_nodes += 1
                    
                    if (child.get_x(), child.get_y()) not in explored and (child.get_x(), child.get_y()) not in frontier:
                        if self.is_on_switch(child):
                            expansion_order.append((child.get_x(), child.get_y(), dir))
                            stone.set_weight(stone_temp.get_weight())
                            return expansion_order, generated_nodes
                        frontier.append((child.get_x(), child.get_y()))
                        expansion_order.append((child.get_x(), child.get_y(), dir)) 
        
    # Tim duong di tu nhan vat Ares den vi tri day da
    def dfs_for_Ares_to_pos(self, ares, x, y):
        ares_temp = Object('Ares', ares.get_x(), ares.get_y())
        generated_nodes = 0
        if ares_temp.get_x() == x and ares_temp.get_y() == y:
            return [(ares_temp.get_x(), ares_temp.get_y(), '')], generated_nodes
        frontier = [(ares_temp.get_x(), ares_temp.get_y())]
        explored = set()
        expansion_order = [(ares_temp.get_x(), ares_temp.get_y(), '')]
        while True:
            if len(frontier) == 0:
                return [], generated_nodes
            ares_temp_x , ares_temp_y = frontier.pop(len(frontier) - 1) 
            ares_temp.set_x(ares_temp_x)
            ares_temp.set_y(ares_temp_y)
            explored.add((ares_temp.get_x(), ares_temp.get_y()))
            for dir in Direction_Map.direction_map.keys():
                if self.is_valid_move(ares_temp, dir) and not self.is_push_stone_move(ares_temp, dir):
                    dx, dy = Direction_Map.get_direction(dir)
                    child = Object('Ares', ares_temp.get_x() + dx, ares_temp.get_y() + dy)
                    generated_nodes += 1
                    
                    if (child.get_x(), child.get_y()) not in explored and (child.get_x(), child.get_y()) not in frontier:
                        if child.get_x() == x and child.get_y() == y:
                            expansion_order.append((child.get_x(), child.get_y(), dir))
                            return expansion_order, generated_nodes
                        frontier.append((child.get_x(), child.get_y()))
                        expansion_order.append((child.get_x(), child.get_y(), dir))
                        
    # Loai bo cac nhanh thua, cut trong duong di, trich xuat duong di duy nhat
    def extract_real_path(self, expansion_order):
        real_path = []
        if len(expansion_order) == 0: 
            return real_path
        real_path.insert(0, expansion_order[len(expansion_order) - 1]) # Dich cua duong di
        if real_path[0][2] == '': # neu no cung la diem dau
            return real_path
        while True:
            dx, dy = Direction_Map.get_direction(real_path[0][2])
            parent = (real_path[0][0] - dx, real_path[0][1] - dy) # Truy nguoc den diem truoc do
            for i in expansion_order:
                if i[0] == parent[0] and i[1] == parent[1]: # Tim kiem
                    real_path.insert(0, i)
                    break
            if real_path[0][0] == expansion_order[0][0] and real_path[0][1] == expansion_order[0][1]: # Neu da truy nguoc ve diem xuat phat
                break
        return real_path
    
    # setup them vai thu truoc khi giai
    def pre_setup(self):
        ares = self.find_object_by_type('Ares')[0]
        self.Objects.append(Object('Cell', ares.get_x(), ares.get_y())) # bien o ma ares roi di khi xuat phat thanh o trong
        stones = self.find_object_by_type('Stone')
        for stone in stones:
            self.Objects.append(Object('Cell', stone.get_x(), stone.get_y())) # bien o ma da roi di khi xuat phat thanh o trong
        ares_on_switch = self.find_object_by_type('Ares_on_Switch')
        if len(ares_on_switch) > 0:
            for aos in ares_on_switch:
                self.Objects.append(Object('Ares', aos.get_x(), aos.get_y()))
                self.Objects.append(Object('Switch', aos.get_x(), aos.get_y()))
        
    def final_solution(self):
        # This is where to solve the whole asshole
        self.pre_setup()
        main_char = self.find_object_by_type('Ares')[0]
        path_cost = 0
        path = ''
        generated_nodes = 0
        if (self.is_complete()): # Kiem tra su hoan thien san
            return path, path_cost, generated_nodes
        stones = self.find_object_by_type('Stone')
        for stone in stones: # voi moi vien da trong me cung
            if self.is_no_longer_able_to_push(stone):
                continue
            expansion_order_stone, generated_nodes_stone = self.dfs_for_stone_to_switch(stone)
            real_path_stone = self.extract_real_path(expansion_order_stone) # tim duong di cua da
            generated_nodes += generated_nodes_stone
            if len(real_path_stone) == 0:
                return '', 0, generated_nodes
            iter1 = iter(real_path_stone)
            iter2 = iter(real_path_stone)
            next(iter2)
            # voi moi buoc di cua da tren duong di
            for cell1, cell2 in zip(iter1, iter2): # for (int i = 0, j = 1; i < n & j < n; i++, j++)
                di, dj = Direction_Map.get_direction(cell2[2])
                i = cell1[0] - di
                j = cell1[1] - dj
                expansion_order_ares, generated_nodes_ares = self.dfs_for_Ares_to_pos(main_char, i, j)
                real_path_ares = self.extract_real_path(expansion_order_ares) # tim duong di cua ares
                generated_nodes += generated_nodes_ares
                if len(real_path_ares) == 0:
                    return '', 0, generated_nodes
                for step in real_path_ares[1:]: # Bo qua phan tu dau tien
                    # Cho ares di chuyen
                    main_char.go(step[2])
                    path += step[2]
                # cho ares day da
                stone.go(cell2[2])
                main_char.go(cell2[2])
                path += cell2[2].upper()
                path_cost += stone.get_weight() # tinh chi phi
                # kiem tra da da den cong tac chua
                switch = self.is_on_switch(stone)
                if switch != False:
                    switch.set_object_type('Stone_on_Switch')
                    stone.set_object_type('Stone_on_Switch')
                    self.Objects.remove(stone)
                    
        # kiem tra su hoan thien
        if self.is_complete():
            return path, path_cost, generated_nodes
        else:
            return '', 0, 0
        
    def write_output(self, file_name, result):
        with open(file_name, 'wt') as file_object:
            if result['Path'] == '':
                file_object.write(str(result['Algorithm']) + '\n')
                file_object.write('No Solution Found\n')
            else:
                # Ghi dòng đầu tiên
                file_object.write(str(result['Algorithm']) + '\n')
                
                # Ghi các cặp key-value (trừ 'Algorithm' và 'Path')
                result_str = ', '.join(f"{key}: {value}" for key, value in list(result.items())[1:-1])
                file_object.write(result_str)
                
                # Xuống dòng cuối
                file_object.write('\n' + str(result['Path']) + '\n')
            
def main(input_file_name, output_file_name):
    maze = Maze()
    maze.read_input(input_file_name)
    tracemalloc.start()
    start_time = time.time()
    path, path_cost, generated_nodes = maze.final_solution()
    end_time = time.time()
    current, peek = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory = peek/(1024 * 1024)
    time_used = (end_time - start_time) * 1000
    result = {
        'Algorithm': 'DFS',
        'Steps': len(path),
        'Weight': path_cost,
        'Node': generated_nodes,
        'Time (ms)': round(time_used, 2),
        'Memory (MB)': round(memory, 2),
        'Path': path
    }
    maze.write_output(output_file_name, result)

# input_file_name = 'D:\HK1 2024-2025\CSTTNT\project01\input\input-04.txt'
# output_file_name = 'output.txt'
# main(input_file_name, output_file_name)