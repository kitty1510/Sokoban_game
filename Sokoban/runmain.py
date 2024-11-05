import os
from algo.bfs import main as bfs_main
from algo.astar import main as astar_main
from algo.dfs import main as dfs_main
from algo.ucs import main as ucs_main

# Lấy đường dẫn của thư mục hiện tại
current_directory = os.path.dirname(os.path.abspath(__file__))
input_directory = os.path.join(current_directory, 'input')
output_directory = os.path.join(current_directory, 'output')
output_test_directory = os.path.join(current_directory, 'outputTest')

# Tạo thư mục output nếu chưa tồn tại
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Tạo thư mục outputTest nếu chưa tồn tại
if not os.path.exists(output_test_directory):
    os.makedirs(output_test_directory)

def process_file(input_file_name, output_summary_file_name):
    # Các file tạm để lưu kết quả của từng thuật toán
    output_file_name_bfs = os.path.join(output_test_directory, 'output_bfs.txt')
    output_file_name_astar = os.path.join(output_test_directory, 'output_astar.txt')
    output_file_name_dfs = os.path.join(output_test_directory, 'output_dfs.txt')
    output_file_name_ucs = os.path.join(output_test_directory, 'output_ucs.txt')

    # Chạy các thuật toán và lưu kết quả vào file tạm
    bfs_main(input_file_name, output_file_name_bfs)
    astar_main(input_file_name, output_file_name_astar)
    dfs_main(input_file_name, output_file_name_dfs)
    ucs_main(input_file_name, output_file_name_ucs)

    # Tổng hợp kết quả từ các file tạm và ghi vào outputSummary
    with open(output_summary_file_name, 'w') as summary_file:
        #summary_file.write("=== BFS Result ===\n")
        with open(output_file_name_bfs, 'r') as bfs_file:
            summary_file.write(bfs_file.read())
            summary_file.write("\n")

        #summary_file.write("=== DFS Result ===\n")
        with open(output_file_name_dfs, 'r') as dfs_file:
            summary_file.write(dfs_file.read())
            summary_file.write("\n")

        with open(output_file_name_ucs, 'r') as ucs_file:
            summary_file.write(ucs_file.read())
            summary_file.write("\n")
        
        #summary_file.write("=== A* Result ===\n")
        with open(output_file_name_astar, 'r') as astar_file:
            summary_file.write(astar_file.read())
            summary_file.write("\n")

        # Thông báo ghi file thành công
        print(f"Đã ghi thành công file: {os.path.basename(output_summary_file_name)}")
       

def main():
    # Lặp qua tất cả các file trong thư mục input
    for file_name in os.listdir(input_directory):
        if file_name.startswith('input-') and file_name.endswith('.txt'):
            # Tạo đường dẫn file input và file output tương ứng
            input_file_name = os.path.join(input_directory, file_name)
            output_summary_file_name = os.path.join(output_directory, file_name.replace('input', 'output'))

            # Xử lý từng file input
            process_file(input_file_name, output_summary_file_name)

if __name__ == "__main__":
    main()
