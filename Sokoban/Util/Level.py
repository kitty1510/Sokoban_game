import os
import copy

class Level:

    def __init__(self, level_num):
        self.matrix = []
        self.matrix_history = []

        # Create level
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../', 'input', f'input-{level_num:02}.txt'), 'r') as f:
                # Bỏ qua dòng đầu tiên và chỉ đọc từ dòng thứ hai trở đi
                for i, row in enumerate(f.read().splitlines()):
                    if i == 0:  # Bỏ qua dòng đầu tiên
                        continue
                    self.matrix.append(list(row))
        except FileNotFoundError:
            print(os.path.dirname(os.path.abspath(__file__)), 'input', f'input-{level_num:02}.txt')
        except Exception as e:
            print(f"An error occurred: {e}")

    def getMatrix(self):
        return self.matrix

    def addToHistory(self, matrix):
        self.matrix_history.append(copy.deepcopy(matrix))

    def getLastMatrix(self):
        if self.matrix_history:
            lastMatrix = self.matrix_history.pop()
            self.matrix = lastMatrix
            return lastMatrix
        return self.matrix

    def getPlayerPosition(self):
        for i in range(len(self.matrix)):
            for k in range(len(self.matrix[i])):
                if self.matrix[i][k] == "@":
                    return [k, i]
        return None  # Return None if player not found

    def getBoxes(self):
        boxes = []
        for i in range(len(self.matrix)):
            for k in range(len(self.matrix[i])):
                if self.matrix[i][k] == "$":
                    boxes.append([k, i])
        return boxes

    def getSize(self):
        max_row_length = max(len(row) for row in self.matrix) if self.matrix else 0
        return [max_row_length, len(self.matrix)]
