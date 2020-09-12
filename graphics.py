'''
    author: Pham Manh Tien
    created: 15.06.2020
'''
import pygame
from main import GameState
import os

class character_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rows = 4
        self.cols = 5
        self.totalCell = self.rows * self.cols

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = self.rect.width / self.cols
        h = self.cellHeight = self.rect.height / self.rows

        self.cells = list()
        for y in range(self.rows):
            for x in range(self.cols):
                self.cells.append([x * w, y * h, w, h])

    def draw(self, surface, x, y, cellIndex, direction):
        if direction == "UP":
            pass
        if direction == "RIGHT":
            cellIndex = cellIndex + 5
        if direction == "DOWN":
            cellIndex = cellIndex + 10
        if direction == "LEFT":
            cellIndex = cellIndex + 15
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class wall_spritesheet:
    def __init__(self, image_spritesheet_path, maze_size):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.left_wall = []
        self.right_wall =[]
        self.up_wall = []
        if maze_size == 6:
            self.left_wall = [0, 0, 12, 78]
            self.right_wall = [84, 0, 12, 78]
            self.up_wall = [12, 0, 72, 18]
            self.up_wall_no_shadow = [12, 0, 66, 18]
        elif maze_size == 8:
            self.left_wall = [0, 0, 12, 63]
            self.right_wall = [69, 0, 12, 63]
            self.up_wall = [12, 0, 57, 18]
            self.up_wall_no_shadow = [12, 0, 51, 18]
        elif maze_size == 10:
            self.left_wall = [0, 0, 8, 48]
            self.right_wall = [52, 0, 8, 48]
            self.up_wall = [8, 0, 44, 12]
            self.up_wall_no_shadow = [8, 0, 38, 12]

    def draw_left_wall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.left_wall)

    def draw_right_wall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.right_wall)

    def draw_up_wall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.up_wall)

    def draw_up_wall_no_shadow(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.up_wall_no_shadow)

class key_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        self.cell = [0, 0, self.rect.width, self.rect.height]

    def draw(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.cell)

class gate_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        # 8 is number of sheet in image
        w = self.rect.width / 8
        h = self.rect.height
        self.cells = []
        for x in range(8):
            self.cells.append([x * w, 0, w, h])

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class trap_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        self.cell = [0, 0, self.rect.width, self.rect.height]

    def draw(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.cell)

class stairs_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        self.cell_w = self.rect.width // 4
        self.cell_h = self.rect.height
        # Stair is UP, RIGHT, DOWN, LEFT = (0, 1, 2, 3) in list stairs
        self.stairs = []
        for x in range(4):
            self.stairs.append([x * self.cell_w, 0, self.cell_w, self.cell_h])

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.stairs[cellIndex])

def draw_screen(screen, input_maze, backdrop, floor, maze_size, cell_rect, stair, stair_position, trap, trap_position,
                key, key_position, gate_sheet, gate, wall, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red):
    coordinate_X = 67
    coordinate_Y = 80
    # DRAW BACKDROP AND FLOOR
    screen.blit(backdrop, (0, 0))
    screen.blit(floor, (coordinate_X, coordinate_Y))

    # DRAW STAIR
    stair_px = stair_position[1] // 2
    stair_py = stair_position[0] // 2
    stair_x = coordinate_X + cell_rect * (stair_px)
    stair_y = coordinate_Y + cell_rect * (stair_py)
    stair_index = 0
    # STAIR IS RIGHT
    if (stair_px == maze_size and stair_position[0] > 0 and stair_position[0] < 2 * maze_size):
        stair_index = 1
        # STAIR IS LEFT
    elif (stair_px == 0 and stair_position[0] > 0 and stair_position[0] < 2 * maze_size):
        stair_index = 3
        # STAIR IS DOWN
    elif (stair_py == maze_size and stair_position[1] > 0 and stair_position[1] < 2 * maze_size):
        stair_index = 2
    if (stair_index == 0):
        stair_y = coordinate_Y - stair.cell_h
    if (stair_index == 3):
        stair_x = coordinate_X - stair.cell_w
    stair.draw(screen, stair_x, stair_y, stair_index)
    # DRAW TRAP
    if trap_position:
        trap_x = coordinate_X + cell_rect * (trap_position[1] // 2)
        trap_y = coordinate_Y + cell_rect * (trap_position[0] // 2)
        trap.draw(screen, trap_x, trap_y)
    # DRAW KEY
    if key_position:
        key_x = coordinate_X + cell_rect * (key_position[1] // 2)
        key_y = coordinate_Y + cell_rect * (key_position[0] // 2)
        key.draw(screen, key_x, key_y)

    # DRAW EXPLORER
    if explorer["coordinates"]:
        explorer["sprite_sheet"].draw(screen, explorer["coordinates"][0], explorer["coordinates"][1], explorer["cellIndex"], explorer["direction"])

    # DRAW MUMMY WHITE
    if mummy_white:
        for i in range(len(mummy_white)):
            mummy_white[i]["sprite_sheet"].draw(screen, mummy_white[i]["coordinates"][0], mummy_white[i]["coordinates"][1],
                                                mummy_white[i]["cellIndex"], mummy_white[i]["direction"])

    # DRAW MUMMY RED
    if mummy_red:
        for i in range(len(mummy_red)):
            mummy_red[i]["sprite_sheet"].draw(screen, mummy_red[i]["coordinates"][0], mummy_red[i]["coordinates"][1],
                                                mummy_red[i]["cellIndex"], mummy_red[i]["direction"])

    # DRAW SCORPION WHITE
    if scorpion_white:
        for i in range(len(scorpion_white)):
            scorpion_white[i]["sprite_sheet"].draw(screen, scorpion_white[i]["coordinates"][0], scorpion_white[i]["coordinates"][1],
                                                scorpion_white[i]["cellIndex"], scorpion_white[i]["direction"])

    # DRAW SCORPION RED
    if scorpion_red:
        for i in range(len(scorpion_red)):
            scorpion_red[i]["sprite_sheet"].draw(screen, scorpion_red[i]["coordinates"][0], scorpion_red[i]["coordinates"][1],
                                                scorpion_red[i]["cellIndex"], scorpion_red[i]["direction"])

    # DRAW GATE
    if gate:
        gate_x = coordinate_X + cell_rect * (gate["gate_position"][1] // 2)
        gate_y = coordinate_Y + cell_rect * (gate["gate_position"][0] // 2)
        if maze_size == 6 or maze_size == 8:
            gate_x -= 6
            gate_y -= 12
        elif maze_size == 10:
            gate_x -= 3
            gate_y -= 9
        gate_sheet.draw(screen, gate_x, gate_y, gate["cellIndex"])
    # DRAW WALL
    # Horizontal Wall
    for i in range(2, len(input_maze)-1, 2):
        for j in range(1, len(input_maze[i]), 2):
            if input_maze[i][j] == "%":
                wall_x = coordinate_X + cell_rect * (j // 2)
                wall_y = coordinate_Y + cell_rect * (i // 2)
                if maze_size == 6 or maze_size == 8:
                    wall_x -= 6
                    wall_y -= 12
                if maze_size == 10:
                    wall_x -= 3
                    wall_y -= 9
                wall.draw_up_wall(screen, wall_x, wall_y)
    # Vertical Wall
    for j in range(2, len(input_maze)-1, 2):
        for i in range(1, len(input_maze[j]), 2):
            if input_maze[i][j] == "%":
                wall_x = coordinate_X + cell_rect * (j // 2)
                wall_y = coordinate_Y + cell_rect * (i // 2)
                if maze_size == 6 or maze_size == 8:
                    wall_x -= 6
                    wall_y -= 12
                elif maze_size == 10:
                    wall_x -= 3
                    wall_y -= 9
                if (input_maze[i+1][j+1] == "%"):
                    wall.draw_right_wall(screen, wall_x, wall_y)
                    redraw_x = coordinate_X + cell_rect * ((j+1) // 2)
                    redraw_y = coordinate_Y + cell_rect * ((i+1) // 2)
                    if maze_size == 6 or maze_size == 8:
                        redraw_x -= 6
                        redraw_y -= 12
                    if maze_size == 10:
                        redraw_x -= 3
                        redraw_y -= 9
                    if (i + 1 < maze_size * 2 and j + 1 < maze_size * 2):
                        wall.draw_up_wall_no_shadow(screen, redraw_x, redraw_y)
                else:
                    wall.draw_left_wall(screen, wall_x, wall_y)

def gate_animation(screen, game, backdrop, floor, stair, stair_position, trap, trap_position,
                key, key_position, gate_sheet, gate, wall, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red):
    if gate["isClosed"]:
        for i in range(8):
            gate["cellIndex"] = -(i+1)
            draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect, stair, stair_position,
                             trap, trap_position, key, key_position, gate_sheet, gate, wall,
                             explorer, mummy_white, mummy_red, scorpion_white, scorpion_red)
            pygame.time.delay(100)
            pygame.display.update()
    else:
        for i in range(8):
            gate["cellIndex"] = i
            draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect, stair, stair_position,
                        trap, trap_position, key, key_position, gate_sheet, gate, wall,
                        explorer, mummy_white, mummy_red, scorpion_white, scorpion_red)
            pygame.time.delay(100)
            pygame.display.update()

def determine_moving_direction(past_position, new_position):
    if past_position[0] == new_position[0] + 2:  # Move UP
        return "UP"
    if past_position[0] == new_position[0] - 2:  # Move Down
        return "DOWN"
    if past_position[1] == new_position[1] + 2:  # Move Left
        return "LEFT"
    if past_position[1] == new_position[1] - 2:  # Move Right
        return "RIGHT"

def enemy_move_animation(mw_past_position, mw_new_position, mr_past_position, mr_new_position, sw_past_position,
                         sw_new_position, sr_past_position, sr_new_position, screen, game, backdrop, floor, stair, stair_position, trap, trap_position,
                key, key_position, gate_sheet, gate, wall, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red):
    mw_check_movement = [False for _ in range(len(mw_past_position))]
    mr_check_movement = [False for _ in range(len(mr_past_position))]
    sw_check_movement = [False for _ in range(len(sw_past_position))]
    sr_check_movement = [False for _ in range(len(sr_past_position))]
    # Mummy white
    mummy_white_start_coordinate = []
    for i in range(len(mw_past_position)):
        mummy_white_start_x = game.coordinate_screen_x + game.cell_rect * (mw_past_position[i][1] // 2)
        mummy_white_start_y = game.coordinate_screen_y + game.cell_rect * (mw_past_position[i][0] // 2)
        if game.maze[mw_new_position[i][0] - 1][mw_new_position[i][1]] == "%" or game.maze[mw_new_position[i][0] - 1][mw_new_position[i][1]] == "G":
            mummy_white_start_y += 3
        mummy_white_start_coordinate.append([mummy_white_start_x, mummy_white_start_y])
        if mw_past_position[i][0] != mw_new_position[i][0] or mw_past_position[i][1] != mw_new_position[i][1]:
            mw_check_movement[i] = True
        if mw_check_movement[i]:
            mummy_white[i]["direction"] = determine_moving_direction(mw_past_position[i], mw_new_position[i])

    # Mummy red
    mummy_red_start_coordinate = []
    for i in range(len(mr_past_position)):
        mummy_red_start_x = game.coordinate_screen_x + game.cell_rect * (mr_past_position[i][1] // 2)
        mummy_red_start_y = game.coordinate_screen_y + game.cell_rect * (mr_past_position[i][0] // 2)
        if game.maze[mr_new_position[i][0] - 1][mr_new_position[i][1]] == "%" or game.maze[mr_new_position[i][0] - 1][mr_new_position[i][1]] == "G":
            mummy_red_start_y += 3
        mummy_red_start_coordinate.append([mummy_red_start_x, mummy_red_start_y])
        if mr_past_position[i][0] != mr_new_position[i][0] or mr_past_position[i][1] != mr_new_position[i][1]:
            mr_check_movement[i] = True
        if mr_check_movement[i]:
            mummy_red[i]["direction"] = determine_moving_direction(mr_past_position[i], mr_new_position[i])

    # Scorpion white
    scorpion_white_start_coordinate = []
    for i in range(len(sw_past_position)):
        scorpion_white_start_x = game.coordinate_screen_x + game.cell_rect * (sw_past_position[i][1] // 2)
        scorpion_white_start_y = game.coordinate_screen_y + game.cell_rect * (sw_past_position[i][0] // 2)
        if game.maze[sw_new_position[i][0] - 1][sw_new_position[i][1]] == "%" or game.maze[sw_new_position[i][0] - 1][sw_new_position[i][1]] == "G":
            scorpion_white_start_y += 3
        scorpion_white_start_coordinate.append([scorpion_white_start_x, scorpion_white_start_y])
        if sw_past_position[i][0] != sw_new_position[i][0] or sw_past_position[i][1] != sw_new_position[i][1]:
            sw_check_movement[i] = True
        if sw_check_movement[i]:
            scorpion_white[i]["direction"] = determine_moving_direction(sw_past_position[i], sw_new_position[i])

    # Scorpion Red
    scorpion_red_start_coordinate = []
    for i in range(len(sr_past_position)):
        scorpion_red_start_x = game.coordinate_screen_x + game.cell_rect * (sr_past_position[i][1] // 2)
        scorpion_red_start_y = game.coordinate_screen_y + game.cell_rect * (sr_past_position[i][0] // 2)
        if game.maze[sr_new_position[i][0] - 1][sr_new_position[i][1]] == "%" or game.maze[sr_new_position[i][0] - 1][sr_new_position[i][1]] == "G":
            scorpion_red_start_y += 3
        scorpion_red_start_coordinate.append([scorpion_red_start_x, scorpion_red_start_y])
        if sr_past_position[i][0] != sr_new_position[i][0] or sr_past_position[i][1] != sr_new_position[i][1]:
            sr_check_movement[i] = True
        if sr_check_movement[i]:
            scorpion_red[i]["direction"] = determine_moving_direction(sr_past_position[i], sr_new_position[i])

    step_stride = game.cell_rect // 5
    for i in range(len(mummy_white)):
        mummy_white[i]["coordinates"] = mummy_white_start_coordinate[i]
    for i in range(len(mummy_red)):
        mummy_red[i]["coordinates"] = mummy_red_start_coordinate[i]
    for i in range(len(scorpion_white)):
        scorpion_white[i]["coordinates"] = scorpion_white_start_coordinate[i]
    for i in range(len(scorpion_red)):
        scorpion_red[i]["coordinates"] = scorpion_red_start_coordinate[i]

    for i in range(6):
        for j in range(len(mummy_white)):
            if i < 5:
                if mummy_white[j]["direction"] == "UP" and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][1] -= step_stride
                if mummy_white[j]["direction"] == "DOWN" and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][1] += step_stride
                if mummy_white[j]["direction"] == "LEFT" and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][0] -= step_stride
                if mummy_white[j]["direction"] == "RIGHT" and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][0] += step_stride
            if mw_check_movement[j]:
                mummy_white[j]["cellIndex"] = i % 5

        for j in range(len(mummy_red)):
            if i < 5:
                if mummy_red[j]["direction"] == "UP" and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][1] -= step_stride
                if mummy_red[j]["direction"] == "DOWN" and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][1] += step_stride
                if mummy_red[j]["direction"] == "LEFT" and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][0] -= step_stride
                if mummy_red[j]["direction"] == "RIGHT" and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][0] += step_stride
            if mr_check_movement[j]:
                mummy_red[j]["cellIndex"] = i % 5

        for j in range(len(scorpion_white)):
            if i < 5:
                if scorpion_white[j]["direction"] == "UP" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][1] -= step_stride
                if scorpion_white[j]["direction"] == "DOWN" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][1] += step_stride
                if scorpion_white[j]["direction"] == "LEFT" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][0] -= step_stride
                if scorpion_white[j]["direction"] == "RIGHT" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][0] += step_stride
            if sw_check_movement[j]:
                scorpion_white[j]["cellIndex"] = i % 5

        for j in range(len(scorpion_red)):
            if i < 5:
                if scorpion_red[j]["direction"] == "UP" and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][1] -= step_stride
                if scorpion_red[j]["direction"] == "DOWN" and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][1] += step_stride
                if scorpion_red[j]["direction"] == "LEFT" and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][0] -= step_stride
                if scorpion_red[j]["direction"] == "RIGHT" and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][0] += step_stride
            if sr_check_movement[j]:
                scorpion_red[j]["cellIndex"] = i % 5

        draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect, stair, stair_position,
                    trap, trap_position, key, key_position, gate_sheet, gate, wall,
                    explorer, mummy_white, mummy_red, scorpion_white, scorpion_red)
        pygame.time.delay(100)
        pygame.display.update()
