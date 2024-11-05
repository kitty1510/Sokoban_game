import os
import pygame
import threading
import time




from Util.Environment import Environment
from Util.Level import Level

from algo.dfs import main as dfs_main 
from algo.bfs import main as bfs_main,read_input_file
from algo.ucs import main as ucs_main
from algo.astar import main as a_star_main

# Đường dẫn đến thư mục main.py
main_path = os.path.dirname(__file__)

# Đường dẫn đến các thư mục và tệp tin
font_path = os.path.join(main_path, 'font/font.ttf')
level_path = os.path.join(main_path, 'input')
output_path = os.path.join(main_path, 'output_game')
theme_path = os.path.join(main_path, 'themes')


# Khởi tạo Pygame
pygame.init()

# Các thiết lập màn hình
WHITE = (255, 255, 255)
GREEN = (102, 102, 0)
BLACK = (0, 0, 0)
BROWN = (51, 51, 10)
GRAY = (222, 222, 222)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Cutie Kitty')

bg = pygame.image.load(theme_path+'/background.png').convert()
bg = pygame.transform.scale(bg, (800, 600))


game_level = 1
Algorithm = "Depth First Search"

current_scr="Menu"

stop_event = threading.Event()



myEnvironment = Environment()



def game_level_control(value):
    global game_level
    game_level += value
    if game_level < 1:
        game_level = 1
    elif game_level > 10:
        game_level = 10

def algorithm_control():
    global Algorithm
    if Algorithm == "Depth First Search":
        Algorithm = "Breadth First Search"
    elif Algorithm == "Breadth First Search":
        Algorithm = "Uniform Cost Search"
    elif Algorithm == "Uniform Cost Search":
        Algorithm = "A*"
    elif Algorithm == "A*":
        Algorithm = "Depth First Search"
    
def screen_control(new_screen):
    global current_scr
    current_scr = new_screen

def initMenu():

    # Hiển thị hình nền
    screen.blit(bg, (0, 0))
    # Khởi tạo phông chữ và hiển thị tiêu đề
    titleSize = pygame.font.Font(font_path, 60)
    titleText = titleSize.render('SOKOBAN', True, GRAY)
    titleRect = titleText.get_rect(center=(400, 80))
    screen.blit(titleText, titleRect)

    # Hiển thị mô tả
    desSize = pygame.font.Font(font_path, 20)
    desText = desSize.render('Select your level!!!', True, GRAY)
    desRect = desText.get_rect(center=(400, 140))
    screen.blit(desText, desRect)

    # Hiển thị level
    levelSize = pygame.font.Font(font_path, 40)
    levelText = levelSize.render(f'Level {game_level}', True, GRAY)
    levelRect = levelText.get_rect(center=(400, 320))
    
    # Tạo nền cho nhãn (Label) - hình chữ nhật với các góc bo tròn
    label_background = pygame.Rect(levelRect.left - 10, levelRect.top - 10, levelRect.width + 20, levelRect.height + 20)
    

   
    # Vẽ viền cho nhãn
    border_rect = label_background.inflate(10, 10)  # Tạo một hình chữ nhật lớn hơn cho viền
    pygame.draw.rect(screen, GRAY, border_rect, 5)  # Vẽ viền màu đen với độ dày 5
    
    # Vẽ văn bản lên nhãn
    screen.blit(levelText, levelRect)

    # algorithm:DFS, BFS, A*
    # Hiển thị thuật toán
    algoSize = pygame.font.Font(font_path, 40)
    algoText = algoSize.render(f'{Algorithm}', True, GRAY)
    algoRect = algoText.get_rect(center=(400, 420))
    screen.blit(algoText, algoRect)


    # Cập nhật màn hình để hiển thị các thay đổi
    pygame.display.flip()

def waitScreen():
    # Hiển thị hình nền
    screen.blit(bg, (0, 0))

    # Khởi tạo phông chữ
    titleSize = pygame.font.Font(font_path, 60)
    desSize = pygame.font.Font(font_path, 30)

    # Kiểm tra trạng thái của luồng A*
    if newThread.is_alive():
        # Hiển thị tiêu đề "GAME ARE IN PROCESS"
        titleText = titleSize.render('GAME ARE IN PROCESS', True, GRAY)
        titleRect = titleText.get_rect(center=(400, 80))
        screen.blit(titleText, titleRect)

        # Hiển thị mô tả "Processing..."
        desText = desSize.render('Processing...', True, GRAY)
        desRect = desText.get_rect(center=(400, 140))
        screen.blit(desText, desRect)
    elif not newThread.is_alive():
        # Nếu luồng đã hoàn tất, hiển thị thông báo "GAME ARE DONE"
        if not isNoSolution():
            titleText = titleSize.render('GAME ARE DONE !', True, GRAY)
            titleRect = titleText.get_rect(center=(400, 150))

            # Hiển thị mô tả "Press SPACE to see the result"
            desText = desSize.render('Press SPACE to see the result', True, GRAY)
            desRect = desText.get_rect(center=(400, 400))
            screen.blit(desText, desRect)
            screen.blit(titleText, titleRect)
        else:
            # Nếu không có lời giải, hiển thị thông báo "NO SOLUTION FOUND"
            titleText = titleSize.render('NO SOLUTION FOUND', True, GRAY)
            titleRect = titleText.get_rect(center=(400, 150))

            # Hiển thị mô tả "Press SPACE to go back to menu"
            desText = desSize.render('Press SPACE to go back to menu', True, GRAY)
            desRect = desText.get_rect(center=(400, 360))
            screen.blit(desText, desRect)
            screen.blit(titleText, titleRect)

    # Cập nhật màn hình để hiển thị các thay đổi
    pygame.display.flip()

    #
    
def isNoSolution():
    # Kiểm tra nếu luồng A* đã hoàn thành
    if not newThread.is_alive():
        algorithm, info_line, path = read_output_file(output_path + f'/output-{game_level:02}.txt')
        
        # Kiểm tra nếu không có lời giải
        if info_line == "No Solution Found":
            return True
    return False
       
#game
def drawLevel(matrix_to_draw):
    # Load level images
    wall = pygame.image.load(theme_path + '/images/wall.png').convert()
    box = pygame.image.load(theme_path + '/images/box.png').convert()
    box_on_target = pygame.image.load(theme_path + '/images/box_on_target.png').convert()
    space = pygame.image.load(theme_path + '/images/space.png').convert()
    target = pygame.image.load(theme_path + '/images/target.png').convert()
    player = pygame.image.load(theme_path + '/images/player.png').convert()

    # Resize images if necessary
    if myLevel.getSize()[0] > myEnvironment.size[0] / 36 or myLevel.getSize()[1] > myEnvironment.size[1] / 36:
        if myLevel.getSize()[0] / myLevel.getSize()[1] >= 1:
            new_image_size = myEnvironment.size[0] / myLevel.getSize()[0]
        else:
            new_image_size = myEnvironment.size[1] / myLevel.getSize()[1]

        # Resize images
        wall = pygame.transform.scale(wall, (new_image_size, new_image_size))
        box = pygame.transform.scale(box, (new_image_size, new_image_size))
        box_on_target = pygame.transform.scale(box_on_target, (new_image_size, new_image_size))
        space = pygame.transform.scale(space, (new_image_size, new_image_size))
        target = pygame.transform.scale(target, (new_image_size, new_image_size))
        player = pygame.transform.scale(player, (new_image_size, new_image_size))

    # Map characters in the level to images
    images = {'#': wall, ' ': space, '$': box, '.': target, '@': player, '*': box_on_target}

    # Get the box size
    box_size = wall.get_width()

    # Calculate the size of the map in pixels
    level_width = len(matrix_to_draw[0]) * box_size
    level_height = len(matrix_to_draw) * box_size

    # Calculate the top-left position to start drawing the level in the center of the screen
    start_x = (myEnvironment.size[0] - level_width) // 2
    start_y = (myEnvironment.size[1] - level_height) // 2

    # Iterate through each row
    for i in range(len(matrix_to_draw)):
        # Iterate through each column
        for c in range(len(matrix_to_draw[i])):
            # Draw each tile in its calculated position
            myEnvironment.screen.blit(images[matrix_to_draw[i][c]], (start_x + c * box_size, start_y + i * box_size))

    pygame.display.update()

				
def movePlayer(direction,myLevel):
	
	matrix = myLevel.getMatrix()
	
	myLevel.addToHistory(matrix)
	
	x = myLevel.getPlayerPosition()[0]
	y = myLevel.getPlayerPosition()[1]
	
	global target_found
	
	#print boxes
	
	if direction == "L":
		
		# if is_space
		if matrix[y][x-1] == " ":
			
			matrix[y][x-1] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y][x-1] == "$":
			
			if matrix[y][x-2] == " ":
				matrix[y][x-2] = "$"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
			elif matrix[y][x-2] == ".":
				matrix[y][x-2] = "*"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
				
				
		# if is_box_on_target
		elif matrix[y][x-1] == "*":
			
			if matrix[y][x-2] == " ":
				matrix[y][x-2] = "$"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y][x-2] == ".":
				matrix[y][x-2] = "*"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
		# if is_target
		elif matrix[y][x-1] == ".":
			
			matrix[y][x-1] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
		
		# else
		else:
			print ("There is a wall here")
	
	elif direction == "R":
		

		# if is_space
		if matrix[y][x+1] == " ":
			
			matrix[y][x+1] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y][x+1] == "$":
			
			if matrix[y][x+2] == " ":
				matrix[y][x+2] = "$"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
			
			elif matrix[y][x+2] == ".":
				matrix[y][x+2] = "*"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "				
		
		# if is_box_on_target
		elif matrix[y][x+1] == "*":
			
			if matrix[y][x+2] == " ":
				matrix[y][x+2] = "$"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y][x+2] == ".":
				matrix[y][x+2] = "*"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
			
		# if is_target
		elif matrix[y][x+1] == ".":
			
			matrix[y][x+1] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
			
		# else
		else:
			print ("There is a wall here")		

	elif direction == "D":
		

		# if is_space
		if matrix[y+1][x] == " ":
			
			matrix[y+1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y+1][x] == "$":
			
			if matrix[y+2][x] == " ":
				matrix[y+2][x] = "$"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
			
			elif matrix[y+2][x] == ".":
				matrix[y+2][x] = "*"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
		
		# if is_box_on_target
		elif matrix[y+1][x] == "*":
			
			if matrix[y+2][x] == " ":
				matrix[y+2][x] = "$"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y+2][x] == ".":
				matrix[y+2][x] = "*"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
		
		# if is_target
		elif matrix[y+1][x] == ".":
			
			matrix[y+1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
			
		# else
		else:
			print ("There is a wall here")

	elif direction == "U":
		

		# if is_space
		if matrix[y-1][x] == " ":
			
			matrix[y-1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y-1][x] == "$":
			
			if matrix[y-2][x] == " ":
				matrix[y-2][x] = "$"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "

			elif matrix[y-2][x] == ".":
				matrix[y-2][x] = "*"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "					
					
		# if is_box_on_target
		elif matrix[y-1][x] == "*":
			
			if matrix[y-2][x] == " ":
				matrix[y-2][x] = "$"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y-2][x] == ".":
				matrix[y-2][x] = "*"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
					
		# if is_target
		elif matrix[y-1][x] == ".":
			
			matrix[y-1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
			
		# else
		else:
			print ("There is a wall here")
	
	drawLevel(matrix)
	
	

	#when all boxes are on targets game is completed
	if len(myLevel.getBoxes()) == 0:
		screen_control("Menu")
		
def initLevel(level):
	# Create an instance of this Level
	global myLevel
	myLevel = Level(level)

	# Draw this level
	drawLevel(myLevel.getMatrix())
	
	global target_found
	target_found = False






# read output file
def read_output_file(filename):
    try:
        with open(filename, 'r') as file:
            # Đọc toàn bộ các dòng
            algorithm = file.readline().strip()  # Dòng đầu tiên: Tên thuật toán
            info_line = file.readline().strip()  # Dòng thứ hai: Thông số
            path = file.readline().strip()  # Dòng thứ ba: Mảng bước đi

            return algorithm, info_line, path

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
	


def gameStart():
    global current_scr
    current_scr = "Game"
    
    # Clear the screen
    myEnvironment.screen.fill((0, 0, 0))
    initLevel(game_level)
    pygame.display.update()
    
    # Đọc dữ liệu từ file output
    algorithm, info_line, path = read_output_file(output_path + f'/output-{game_level:02}.txt')

    info_font = pygame.font.Font(font_path, 20)
    info_text = info_font.render(info_line, True, (255, 255, 255))
    info_rect = info_text.get_rect(center=(400, 550))
    myEnvironment.screen.blit(info_text, info_rect)
    
    # Duyệt qua từng bước trong đường đi
    for i in path:
        # Thực hiện kiểm tra sự kiện thoát trong mỗi lần lặp
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # Thoát hoàn toàn khỏi game nếu người dùng muốn thoát
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                gameStart()  # Khởi động lại trò chơi nếu nhấn "Backspace"
                return  # Thoát khỏi vòng lặp path để khởi động lại

        # Thực hiện bước di chuyển
        if i == 'U' or i == 'u':
            movePlayer("U", myLevel)
        elif i == 'D' or i == 'd':
            movePlayer("D", myLevel)
        elif i == 'L' or i == 'l':
            movePlayer("L", myLevel)
        elif i == 'R' or i == 'r':
            movePlayer("R", myLevel)
        time.sleep(0.5)
    
    # Hiển thị thông báo khi hoàn thành

    pygame.display.update()


    # Chuyển về màn hình Menu
    screen_control("Menu")






if __name__ == "__main__":
    running = True
    while running:
        if current_scr == "Menu":
            initMenu()
        elif current_scr == "Wait":
            waitScreen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if current_scr == "Menu":
                    if event.key == pygame.K_RIGHT:
                        game_level_control(1)
                    elif event.key == pygame.K_LEFT:
                        game_level_control(-1)
                    elif event.key == pygame.K_RETURN:
                        # Khởi tạo một luồng mới để xử lý thuật toán
                        levelFile = level_path + f'\\input-{game_level:02}.txt'
                        outputFile = output_path + f'\\output-{game_level:02}.txt'
						
                        if Algorithm == "Depth First Search":
                            newThread = threading.Thread(target=dfs_main, args=(levelFile,outputFile))
                        elif Algorithm == "Breadth First Search":
                            newThread = threading.Thread(target=bfs_main, args=(levelFile,outputFile))
                        elif Algorithm == "Uniform Cost Search":
                            newThread = threading.Thread(target=ucs_main, args=(levelFile,outputFile))
                        elif Algorithm == "A*":
                            newThread = threading.Thread(target=a_star_main, args=(levelFile,outputFile)) 
                        newThread.start()
						
                        screen_control("Wait")
                    elif event.key == pygame.K_SPACE:
                        algorithm_control()  # Thay đổi thuật toán khi nhấn SPACE
                    elif event.key == pygame.K_ESCAPE:
                        stop_event.set()
                        running = False
						
						

                elif current_scr == "Game":
                    if event.key ==pygame.K_ESCAPE:
						
                        screen_control("Menu")
                    elif event.key == pygame.K_r:
                        gameStart()


                elif current_scr == "Wait":
                    if event.key == pygame.K_SPACE and not newThread.is_alive():
                        gameStart()
                    elif event.key == pygame.K_ESCAPE:
                        running = False  # Thoát trò chơi trên ESCAPE

    pygame.quit()

