'''
    author: Pham Manh Tien
    created: 10.06.2020
'''
import pygame
import os
import graphics
import characters
from search import BFS

class GameState:
    def __init__(self, file_name):
        self.screen_size_x = 494
        self.screen_size_y = 480
        self.maze_rect = 360
        self.coordinate_screen_x = 67
        self.coordinate_screen_y = 80
        self.get_input_maze(file_name)
        self.get_input_object(file_name)
        self.gate = dict()
        if self.gate_position:
            self.gate = {
                "gate_position": self.gate_position,
                "isClosed": True,
                "cellIndex": 0
            }
        # Set initial explorer direction
        if self.explorer_position[1] // 2 <= self.maze_size // 2:
            self.explorer_direction = "RIGHT"
        else:
            self.explorer_direction = "LEFT"
        self.mummy_white_direction = []
        self.mummy_red_direction = []
        self.scorpion_white_direction = []
        self.scorpion_red_direction = []
        if self.mummy_white_position:
            for i in range(len(self.mummy_white_position)):
                self.mummy_white_direction.append("DOWN")
        if self.mummy_red_position:
            for i in range(len(self.mummy_red_position)):
                self.mummy_red_direction.append("DOWN")
        if self.scorpion_white_position:
            for i in range(len(self.scorpion_white_position)):
                self.scorpion_white_direction.append("DOWN")
        if self.scorpion_red_position:
            for i in range(len(self.scorpion_red_position)):
                self.scorpion_red_direction.append("DOWN")

    def get_input_maze(self, name):
        self.maze = []
        self.stair_position = ()
        self.trap_position = ()
        self.key_position = ()
        self.gate_position = ()
        with open(os.path.join(maze_path, name),"r") as file:
            for line in file:
                row = []
                for chr in line:
                    if chr != '\n': row.append(chr)
                self.maze.append(row)

        self.maze_size = len(self.maze) // 2
        self.cell_rect = self.maze_rect // self.maze_size

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 'S':
                    self.stair_position = (i, j)
                if self.maze[i][j] == 'T':
                    self.trap_position = (i, j)
                if self.maze[i][j] == 'K':
                    self.key_position = (i, j)
                if self.maze[i][j] == 'G':
                    self.gate_position = (i, j)

    def get_input_object(self, name):
        self.mummy_white_position = []
        self.mummy_red_position = []
        self.scorpion_white_position = []
        self.scorpion_red_position = []
        with open(os.path.join(object_path, name), "r") as file:
            for line in file:
                x = line.split()
                if x[0] == 'E':     # Get explorer posititon
                    self.explorer_position = [int(x[1]), int(x[2])]
                elif x[0] == 'MW':  # Get list mummy white position
                    white_position = [int(x[1]), int(x[2])]
                    self.mummy_white_position.append(white_position)
                elif x[0] == 'MR': # Get list mummy red position
                    red_position = [int(x[1]), int(x[2])]
                    self.mummy_red_position.append(red_position)
                elif x[0] == 'SW': # Get list scorpion white position
                    scor_white_position = [int(x[1]), int(x[2])]
                    self.scorpion_white_position.append(scor_white_position)
                elif x[0] == 'SR': # Get list scorpion red position
                    scor_red_position = [int(x[1]), int(x[2])]
                    self.scorpion_red_position.append(scor_red_position)

    def show_information(self):
        print("Maze: ")
        for i in range(len(self.maze)):
            print(self.maze[i])
        print("Stair position: {}".format(self.stair_position))
        if self.trap_position:
            print("Trap position: {}".format(self.trap_position))
        else: print("Trap does'nt exist in this map")
        if self.key_position:
            print("Key position: {}".format(self.key_position))
            print("Gate position: {}".format(self.gate["gate_position"]))
        else:
            print("Key and gate don't exist in this map")
        print("Explorer position: {}".format(self.explorer_position))
        for i in range(len(self.mummy_white_position)):
            print("Mummy white number {}: {}".format(i+1, self.mummy_white_position[i]))
        for i in range(len(self.mummy_red_position)):
            print("Mummy red number {}: {}".format(i+1, self.mummy_red_position[i]))
        for i in range(len(self.scorpion_white_position)):
            print("Scorpion white number {}: {}".format(i+1, self.scorpion_white_position[i]))
        for i in range(len(self.scorpion_red_position)):
            print("Scorpion red number {}: {}".format(i+1, self.scorpion_red_position[i]))

    def explorer_escape(self):
        x = self.explorer_position[0]
        y = self.explorer_position[1]
        explorer_exit = False
        if ((x - 1 == self.stair_position[0] and y == self.stair_position[1])
                or (x + 1 == self.stair_position[0] and y == self.stair_position[1])
                or (x == self.stair_position[0] and y - 1 == self.stair_position[1])
                or (x == self.stair_position[0] and y + 1 == self.stair_position[1])):
            explorer_exit = True

        return explorer_exit

def load_image_path(size):
    image_path = os.path.join(project_path, "image")
    backdrop_path = os.path.join(image_path, "backdrop.png")
    filename_floor = "floor" + str(size) + ".jpg"
    filename_wall = "walls" + str(size) + ".png"
    filename_key = "key" + str(size) + ".png"
    filename_gate = "gate" + str(size) + ".png"
    filename_trap = "trap" + str(size) + ".png"
    filename_stair = "stairs" + str(size) + ".png"
    filename_explorer = "explorer" + str(size) + ".png"
    filename_mummy_white = "mummy_white" + str(size) + ".png"
    filename_mummy_red = "redmummy" + str(size) + ".png"
    filename_scorpion_white = "white_scorpion" + str(size) + ".png"
    filename_scorpion_red = "red_scorpion" + str(size) + ".png"
    filename_white_fight = "whitefight" + str(size) + ".png"
    filename_red_fight = "redfight" + str(size) + ".png"
    floor_path = os.path.join(image_path, filename_floor)
    wall_path = os.path.join(image_path, filename_wall)
    key_path = os.path.join(image_path, filename_key)
    gate_path = os.path.join(image_path, filename_gate)
    trap_path = os.path.join(image_path, filename_trap)
    stair_path = os.path.join(image_path, filename_stair)
    explorer_path = os.path.join(image_path, filename_explorer)
    mummy_white_path = os.path.join(image_path, filename_mummy_white)
    mummy_red_path = os.path.join(image_path, filename_mummy_red)
    scorpion_white_path = os.path.join(image_path, filename_scorpion_white)
    scorpion_red_path = os.path.join(image_path, filename_scorpion_red)
    white_fight_path = os.path.join(image_path, filename_white_fight)
    red_fight_path = os.path.join(image_path, filename_red_fight)
    return backdrop_path, floor_path, wall_path, key_path, gate_path, trap_path, stair_path, explorer_path, \
           mummy_white_path, mummy_red_path, scorpion_white_path, scorpion_red_path, white_fight_path, red_fight_path

def make_dict_to_draw_object(explorer_sheet, explorer_coordinates, explorer_direction, explorer_cellIndex,
                             mummy_white_sheet, mummy_white_coordinates, mummy_white_direction, mummy_white_cellIndex,
                             mummy_red_sheet, mummy_red_coordinates, mummy_red_direction, mummy_red_cellIndex,
                             scorpion_white_sheet, scorpion_white_coordinates, scorpion_white_direction, scorpion_white_cellIndex,
                             scorpion_red_sheet, scorpion_red_coordinates, scorpion_red_direction, scorpion_red_cellIndex):
    explorer = {
        "sprite_sheet": explorer_sheet,
        "coordinates": explorer_coordinates,
        "direction": explorer_direction,
        "cellIndex": explorer_cellIndex
    }
    mummy_white = {
        "sprite_sheet": mummy_white_sheet,
        "coordinates": mummy_white_coordinates,
        "direction": mummy_white_direction,
        "cellIndex": mummy_white_cellIndex
    }
    mummy_red = {
        "sprite_sheet": mummy_red_sheet,
        "coordinates": mummy_red_coordinates,
        "direction": mummy_red_direction,
        "cellIndex": mummy_red_cellIndex
    }
    scorpion_white = {
        "sprite_sheet": scorpion_white_sheet,
        "coordinates": scorpion_white_coordinates,
        "direction": scorpion_white_direction,
        "cellIndex": scorpion_white_cellIndex
    }
    scorpion_red = {
        "sprite_sheet": scorpion_red_sheet,
        "coordinates": scorpion_red_coordinates,
        "direction": scorpion_red_direction,
        "cellIndex": scorpion_red_cellIndex
    }
    return explorer, mummy_white, mummy_red, scorpion_white, scorpion_red

def Cal_coordinates(game, position_x, position_y):
    coordinate_x = game.coordinate_screen_x + game.cell_rect * (position_y // 2)
    coordinate_y = game.coordinate_screen_y + game.cell_rect * (position_x // 2)
    if game.maze[position_x - 1][position_y] == "%" or game.maze[position_x - 1][position_y] == "G":
        coordinate_y += 3
    return [coordinate_x, coordinate_y]

def character_same_place_with_key(character, key_position, gate, render, screen, game, backdrop, floor, stair, stair_position, trap, trap_position,
                key, gate_sheet, wall, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red):
    if key_position and character.get_x() == key_position[0] and character.get_y() == key_position[1]:
        if gate["isClosed"]:
            gate["isClosed"] = False
        else:
            gate["isClosed"] = True
        print("gate is closed: {}".format(gate["isClosed"]))
        if render:
            graphics.gate_animation(screen, game, backdrop, floor, stair, stair_position, trap, trap_position,
                           key, key_position, gate_sheet, gate, wall, explorer, mummy_white, mummy_red, scorpion_white,
                           scorpion_red)
        if gate["isClosed"]:
            gate["cellIndex"] = 0
        else:
            gate["cellIndex"] = -1
    return gate

def update_list_character(list_character, list_sprite_sheet_character):
    i = 0
    while i < len(list_character):
        j = 0
        while j < len(list_character):
            if j != i and list_character[i].check_same_position(list_character[j]):
                del list_character[j]
                del list_sprite_sheet_character[j]
            j += 1
        i += 1
    return list_character, list_sprite_sheet_character

def update_lists_character(list_strong_scharacter, list_week_scharacter, list_sprite_sheet_week_character):
    for i in range(len(list_strong_scharacter)):
        j = 0
        while j < len(list_week_scharacter):
            if list_strong_scharacter[i].check_same_position(list_week_scharacter[j]):
                del list_week_scharacter[j]
                del list_sprite_sheet_week_character[j]
            j += 1
    return list_week_scharacter, list_sprite_sheet_week_character

def check_explorer_is_killed(explorer_character, mummy_white_character, mummy_red_character, scorpion_white_character,
                            scorpion_red_character, trap_position):
    if trap_position and explorer_character.get_x() == trap_position[0] and explorer_character.get_y() == trap_position[1]:
        print("YOU HAVE BEEN TRAPPED")
        return True
    if mummy_white_character:
        for i in range(len(mummy_white_character)):
            if explorer_character.get_x() == mummy_white_character[i].get_x() and explorer_character.get_y() == mummy_white_character[i].get_y():
                print("YOU HAVE BEEN ATTACKED BY MUMMY WHITE")
                return True
    if mummy_red_character:
        for i in range(len(mummy_red_character)):
            if explorer_character.get_x() == mummy_red_character[i].get_x() and explorer_character.get_y() == mummy_red_character[i].get_y():
                print("YOU HAVE BEEN ATTACKED BY MUMMY RED")
                return True
    if scorpion_white_character:
        for i in range(len(scorpion_white_character)):
            if explorer_character.get_x() == scorpion_white_character[i].get_x() and explorer_character.get_y() == scorpion_white_character[i].get_y():
                print("YOU HAVE BEEN ATTACKED BY SCORPION WHITE")
                return True
    if scorpion_red_character:
        for i in range(len(scorpion_red_character)):
            if explorer_character.get_x() == scorpion_red_character[i].get_x() and explorer_character.get_y() == scorpion_red_character[i].get_y():
                print("YOU HAVE BEEN ATTACKED BY SCORPION RED")
                return True
    return False

def update_enemy_position(window, render, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character,mummy_white_character,
                        mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                         list_mummy_red, list_scorpion_white, list_scorpion_red):
    game.gate = character_same_place_with_key(explorer_character, game.key_position, game.gate, render, window, game,
                                              backdrop, floor,
                                              stair, game.stair_position, trap, game.trap_position,
                                              key, gate, wall, explorer, list_mummy_white, list_mummy_red,
                                              list_scorpion_white,
                                              list_scorpion_red)
    if check_explorer_is_killed(explorer_character, mummy_white_character, mummy_red_character,
                                scorpion_white_character, scorpion_red_character, game.trap_position):
        print("=== YOU LOSE ===")
        return True

    # --------------------------- MUMMY WHITE FIRST MOVE ----------------------------
    mw_past_position = []
    mw_new_position = []
    for i in range(len(mummy_white_character)):
        mw_past_position.append([mummy_white_character[i].get_x(), mummy_white_character[i].get_y()])
        print("MUMMY WHITE {}".format(i + 1))
        mummy_white_character[i] = mummy_white_character[i].white_move(game.maze, game.gate, explorer_character)
        print("First move: {} {}".format(mummy_white_character[i].get_x(), mummy_white_character[i].get_y()))
        mw_new_position.append([mummy_white_character[i].get_x(), mummy_white_character[i].get_y()])

    for i in range(len(mummy_white_character)):
        game.gate = character_same_place_with_key(mummy_white_character[i], game.key_position, game.gate,
                                                  render,
                                                  window, game, backdrop, floor,
                                                  stair, game.stair_position, trap, game.trap_position,
                                                  key, gate, wall, explorer, list_mummy_white,
                                                  list_mummy_red, list_scorpion_white,
                                                  list_scorpion_red)

    # ------------------------- MUMMY RED FIRST MOVE--------------------------
    mr_past_position = []
    mr_new_position = []
    for i in range(len(mummy_red_character)):
        mr_past_position.append([mummy_red_character[i].get_x(), mummy_red_character[i].get_y()])
        print("MUMMY RED {}".format(i + 1))
        mummy_red_character[i] = mummy_red_character[i].red_move(game.maze, game.gate, explorer_character)
        print("First move: {} {}".format(mummy_red_character[i].get_x(), mummy_red_character[i].get_y()))
        mr_new_position.append([mummy_red_character[i].get_x(), mummy_red_character[i].get_y()])

    for i in range(len(mummy_red_character)):
        game.gate = character_same_place_with_key(mummy_red_character[i], game.key_position, game.gate,
                                                  render,
                                                  window, game, backdrop, floor,
                                                  stair, game.stair_position, trap, game.trap_position,
                                                  key, gate, wall, explorer, list_mummy_white,
                                                  list_mummy_red, list_scorpion_white,
                                                  list_scorpion_red)

    # ------------------------- SCORPION WHITE MOVE ---------------------------------
    sw_past_position = []
    sw_new_position = []
    for i in range(len(scorpion_white_character)):
        sw_past_position.append([scorpion_white_character[i].get_x(), scorpion_white_character[i].get_y()])
        print("SCORPION WHITE {}".format(i + 1))
        scorpion_white_character[i] = scorpion_white_character[i].white_move(game.maze, game.gate,
                                                                             explorer_character)
        print("First move: {} {}".format(scorpion_white_character[i].get_x(), scorpion_white_character[i].get_y()))
        sw_new_position.append([scorpion_white_character[i].get_x(), scorpion_white_character[i].get_y()])

    for i in range(len(scorpion_white_character)):
        game.gate = character_same_place_with_key(scorpion_white_character[i], game.key_position, game.gate,
                                                  render,
                                                  window, game, backdrop, floor,
                                                  stair, game.stair_position, trap, game.trap_position,
                                                  key, gate, wall, explorer, list_mummy_white,
                                                  list_mummy_red, list_scorpion_white,
                                                  list_scorpion_red)

    # ------------------------- SCORPION RED MOVE ---------------------------------
    sr_past_position = []
    sr_new_position = []
    for i in range(len(scorpion_red_character)):
        sr_past_position.append([scorpion_red_character[i].get_x(), scorpion_red_character[i].get_y()])
        print("SCORPION RED {}".format(i + 1))
        scorpion_red_character[i] = scorpion_red_character[i].red_move(game.maze, game.gate,
                                                                       explorer_character)
        print("First move: {} {}".format(scorpion_red_character[i].get_x(),
                                         scorpion_red_character[i].get_y()))
        sr_new_position.append([scorpion_red_character[i].get_x(), scorpion_red_character[i].get_y()])

    for i in range(len(scorpion_red_character)):
        game.gate = character_same_place_with_key(scorpion_red_character[i], game.key_position, game.gate,
                                                  render,
                                                  window, game, backdrop, floor,
                                                  stair, game.stair_position, trap, game.trap_position,
                                                  key, gate, wall, explorer, list_mummy_white,
                                                  list_mummy_red, list_scorpion_white,
                                                  list_scorpion_red)

    if render:
        graphics.enemy_move_animation(mw_past_position, mw_new_position, mr_past_position, mr_new_position,
                                      sw_past_position, sw_new_position, sr_past_position, sr_new_position,
                                      window, game, backdrop, floor, stair, game.stair_position, trap,
                                      game.trap_position, key, game.key_position, gate, game.gate, wall,
                                      explorer, list_mummy_white, list_mummy_red, list_scorpion_white,
                                      list_scorpion_red)

    if check_explorer_is_killed(explorer_character, mummy_white_character, mummy_red_character,
                                scorpion_white_character, scorpion_red_character, game.trap_position):
        print("=== YOU LOSE ===")
        return True

    # Delete mummy white have same position
    mummy_white_character, list_mummy_white = update_list_character(mummy_white_character, list_mummy_white)
    # Delte same mummy red have same position
    mummy_red_character, list_mummy_red = update_list_character(mummy_red_character, list_mummy_red)
    # Delete same scorpion white have same position
    scorpion_white_character, list_scorpion_white = update_list_character(scorpion_white_character, list_scorpion_white)
    # Delete same scorpion white have same position
    scorpion_red_character, list_scorpion_red = update_list_character(scorpion_red_character, list_scorpion_red)

    # Delete mummy red, scropion white, scorpion red if mummy white have the same position
    if mummy_red_character:
        mummy_red_character, list_mummy_red = update_lists_character(mummy_white_character, mummy_red_character,
                                                                     list_mummy_red)
    if scorpion_white_character:
        scorpion_white_character, list_scorpion_white = update_lists_character(mummy_white_character,
                                                                               scorpion_white_character,
                                                                               list_scorpion_white)
    if scorpion_red_character:
        scorpion_red_character, list_scorpion_red = update_lists_character(mummy_white_character,
                                                                           scorpion_red_character, list_scorpion_red)
    # Delete scropion white, scorpion red if mummy red have the same position
    if scorpion_white_character:
        scorpion_white_character, list_scorpion_white = update_lists_character(mummy_red_character,
                                                                               scorpion_white_character,
                                                                               list_scorpion_white)
    if scorpion_red_character:
        scorpion_red_character, list_scorpion_red = update_lists_character(mummy_red_character,
                                                                           scorpion_red_character,
                                                                           list_scorpion_red)
    # Delete scorpion red if scorpion white have the same position
    if scorpion_red_character:
        scorpion_red_character, list_scorpion_red = update_lists_character(scorpion_white_character,
                                                                           scorpion_red_character,
                                                                           list_scorpion_red)
    sw_past_position = sw_new_position.copy()
    sr_past_position = sr_new_position.copy()

    # ----------------------------- MUMMY WHITE SECOND MOVE -----------------------
    mw_past_position = []
    mw_new_position = []
    for i in range(len(mummy_white_character)):
        print("MUMMY WHITE {}".format(i + 1))
        mw_past_position.append([mummy_white_character[i].get_x(), mummy_white_character[i].get_y()])
        mummy_white_character[i] = mummy_white_character[i].white_move(game.maze, game.gate,
                                                                       explorer_character)
        print("Second Move: {} {}".format(mummy_white_character[i].get_x(), mummy_white_character[i].get_y()))
        mw_new_position.append([mummy_white_character[i].get_x(), mummy_white_character[i].get_y()])

    for i in range(len(mummy_white_character)):
        game.gate = character_same_place_with_key(mummy_white_character[i], game.key_position, game.gate,
                                                  render,
                                                  window, game, backdrop, floor,
                                                  stair, game.stair_position, trap, game.trap_position,
                                                  key, gate, wall, explorer, list_mummy_white,
                                                  list_mummy_red, list_scorpion_white,
                                                  list_scorpion_red)

    # -------------------------- MUMMY RED SECOND MOVE -------------------------
    mr_past_position = []
    mr_new_position = []
    for i in range(len(mummy_red_character)):
        print("MUMMY RED {}".format(i + 1))
        mr_past_position.append([mummy_red_character[i].get_x(), mummy_red_character[i].get_y()])
        mummy_red_character[i] = mummy_red_character[i].red_move(game.maze, game.gate, explorer_character)
        print("Second Move: {} {}".format(mummy_red_character[i].get_x(), mummy_red_character[i].get_y()))
        mr_new_position.append([mummy_red_character[i].get_x(), mummy_red_character[i].get_y()])

    for i in range(len(mummy_red_character)):
        game.gate = character_same_place_with_key(mummy_red_character[i], game.key_position, game.gate,
                                                  render,
                                                  window, game, backdrop, floor,
                                                  stair, game.stair_position, trap, game.trap_position,
                                                  key, gate, wall, explorer, list_mummy_white,
                                                  list_mummy_red, list_scorpion_white,
                                                  list_scorpion_red)

    if render:
        graphics.enemy_move_animation(mw_past_position, mw_new_position, mr_past_position, mr_new_position,
                                      sw_past_position, sw_new_position, sr_past_position, sr_new_position,
                                      window, game, backdrop, floor, stair, game.stair_position, trap,
                                      game.trap_position, key, game.key_position, gate, game.gate, wall,
                                      explorer, list_mummy_white, list_mummy_red, list_scorpion_white,
                                      list_scorpion_red)
    if check_explorer_is_killed(explorer_character, mummy_white_character, mummy_red_character,
                                scorpion_white_character, scorpion_red_character, game.trap_position):
        print("=== YOU LOSE ===")
        return True

    # Delete mummy white have same position
    mummy_white_character, list_mummy_white = update_list_character(mummy_white_character, list_mummy_white)
    # Delete mummy red have same position
    mummy_red_character, list_mummy_red = update_list_character(mummy_red_character, list_mummy_red)

    # Delete mummy red, scropion white, scorpion red if mummy white have the same position
    if mummy_red_character:
        mummy_red_character, list_mummy_red = update_lists_character(mummy_white_character,
                                                                     mummy_red_character, list_mummy_red)
    if scorpion_white_character:
        scorpion_white_character, list_scorpion_white = update_lists_character(mummy_white_character,
                                                                               scorpion_white_character,
                                                                               list_scorpion_white)
    if scorpion_red_character:
        scorpion_red_character, list_scorpion_red = update_lists_character(mummy_white_character,
                                                                           scorpion_red_character,
                                                                           list_scorpion_red)
    # Delete scropion white, scorpion red if mummy red have the same position and be attacked from mummy white
    if scorpion_white_character:
        scorpion_white_character, list_scorpion_white = update_lists_character(mummy_red_character,
                                                                               scorpion_white_character,
                                                                               list_scorpion_white)
    if scorpion_red_character:
        scorpion_red_character, list_scorpion_red = update_lists_character(mummy_red_character,
                                                                           scorpion_red_character,
                                                                           list_scorpion_red)

    if game.maze[explorer_character.get_x() - 1][explorer_character.get_y()] == "S" or \
            game.maze[explorer_character.get_x() + 1][explorer_character.get_y()] == "S" or \
            game.maze[explorer_character.get_x()][explorer_character.get_y() - 1] == "S" or \
            game.maze[explorer_character.get_x()][explorer_character.get_y() + 1] == "S":
        print("=== YOU HAVE ESCAPED MAZE SUCCESSFULLY ===")
        print("=== YOU WIN ===")
        return True


def rungame(layout, agent, render):
    game = GameState(layout)
    print("INITIAL INFORMATION OF MAZE")
    game.show_information()
    
    # LOAD IMAGE PATH
    backdrop_path, floor_path, wall_path, key_path, gate_path, trap_path, stair_path, explorer_path, \
    mummy_white_path, mummy_red_path, scorpion_white_path, scorpion_red_path, white_fight_path, \
    red_fight_path = load_image_path(game.maze_size)

    # LOAD IMAGE
    backdrop = pygame.image.load(backdrop_path)
    floor = pygame.image.load(floor_path)
    stair = graphics.stairs_spritesheet(stair_path)
    trap = graphics.trap_spritesheet(trap_path)
    key = graphics.key_spritesheet(key_path)
    gate = graphics.gate_spritesheet(gate_path)
    wall = graphics.wall_spritesheet(wall_path, game.maze_size)
    explorer_sheet = graphics.character_spritesheet(explorer_path)
    mummy_white_sheet = graphics.character_spritesheet(mummy_white_path)
    mummy_red_sheet = graphics.character_spritesheet(mummy_red_path)
    scorpion_white_sheet = graphics.character_spritesheet(scorpion_white_path)
    scorpion_red_sheet = graphics.character_spritesheet(scorpion_red_path)
    # GAME
    explorer = {
        "sprite_sheet": explorer_sheet,
        "coordinates": Cal_coordinates(game, game.explorer_position[0], game.explorer_position[1]),
        "direction": game.explorer_direction,
        "cellIndex": 0
    }
    list_mummy_white = []
    for i in range(len(game.mummy_white_position)):
         mummy_white = {
             "sprite_sheet": mummy_white_sheet,
             "coordinates": Cal_coordinates(game, game.mummy_white_position[i][0], game.mummy_white_position[i][1]),
             "direction": game.mummy_white_direction[i],
             "cellIndex": 0
         }
         list_mummy_white.append(mummy_white)

    list_mummy_red = []
    for i in range(len(game.mummy_red_position)):
        mummy_red = {
            "sprite_sheet": mummy_red_sheet,
            "coordinates": Cal_coordinates(game, game.mummy_red_position[i][0], game.mummy_red_position[i][1]),
            "direction": game.mummy_red_direction[i],
            "cellIndex": 0
        }
        list_mummy_red.append(mummy_red)

    list_scorpion_white = []
    for i in range(len(game.scorpion_white_position)):
        scorpion_white = {
            "sprite_sheet": scorpion_white_sheet,
            "coordinates": Cal_coordinates(game, game.scorpion_white_position[i][0], game.scorpion_white_position[i][1]),
            "direction": game.scorpion_white_direction[i],
            "cellIndex": 0
        }
        list_scorpion_white.append(scorpion_white)

    list_scorpion_red = []
    for i in range(len(game.scorpion_red_position)):
        scorpion_red = {
            "sprite_sheet": scorpion_red_sheet,
            "coordinates": Cal_coordinates(game, game.scorpion_red_position[i][0], game.scorpion_red_position[i][1]),
            "direction": game.scorpion_red_direction[i],
            "cellIndex": 0
        }
        list_scorpion_red.append(scorpion_red)

    if render:
        # SET SCREEN
        pygame.init()
        window = pygame.display.set_mode((game.screen_size_x, game.screen_size_y))
        pygame.display.set_caption("Mummy Maze")
        # SET FPS
        FPS = 30
        clock = pygame.time.Clock()
        graphics.draw_screen(window, game.maze, backdrop, floor, game.maze_size, game.cell_rect, stair, game.stair_position,
                          trap, game.trap_position, key, game.key_position, gate, game.gate, wall, explorer, list_mummy_white,
                         list_mummy_red, list_scorpion_white, list_scorpion_red)
        pygame.display.update()

    explorer_character = characters.Explorer(game.explorer_position[0], game.explorer_position[1])
    mummy_white_character = []
    if game.mummy_white_position:
        for i in range(len(game.mummy_white_position)):
            mummy_white_character.append(characters.mummy_white(game.mummy_white_position[i][0], game.mummy_white_position[i][1]))
    mummy_red_character = []
    if game.mummy_red_position:
        for i in range(len(game.mummy_red_position)):
            mummy_red_character.append(characters.mummy_red(game.mummy_red_position[i][0], game.mummy_red_position[i][1]))
    scorpion_white_character = []
    if game.scorpion_white_position:
        for i in range(len(game.scorpion_white_position)):
            scorpion_white_character.append(characters.scorpion_white(game.scorpion_white_position[i][0], game.scorpion_white_position[i][1]))
    scorpion_red_character = []
    if game.scorpion_red_position:
        for i in range(len(game.scorpion_red_position)):
            scorpion_red_character.append(characters.scorpion_red(game.scorpion_red_position[i][0], game.scorpion_red_position[i][1]))

    if agent == "SearchAgent":
        print("FINDING SOLUTION ...")
        ans = BFS(explorer_character, mummy_white_character, mummy_red_character, scorpion_white_character,
              scorpion_red_character, game.gate, game.trap_position, game.key_position, game.maze)
        for i in range(len(ans) - 2, -1, -1):
            if ans[i][0] == ans[i+1][0] - 2 and ans[i][1] == ans[i+1][1]:
                explorer["direction"] = "UP"
            if ans[i][0] == ans[i+1][0] + 2 and ans[i][1] == ans[i+1][1]:
                explorer["direction"] = "DOWN"
            if ans[i][0] == ans[i+1][0] and ans[i][1] == ans[i+1][1] - 2:
                explorer["direction"] = "LEFT"
            if ans[i][0] == ans[i+1][0] and ans[i][1] == ans[i+1][1] + 2:
                explorer["direction"] = "RIGHT"
            if ans[i][0] != ans[i+1][0] or ans[i][1] != ans[i+1][1]:
                explorer_character.move(ans[i][0], ans[i][1], render, window, game, backdrop, floor,
                                        stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                        gate, game.gate, wall, explorer,
                                        list_mummy_white, list_mummy_red, list_scorpion_white, list_scorpion_red)
            print("Explorer position: {} {}".format(explorer_character.get_x(), explorer_character.get_y()))
            isEnd = update_enemy_position(window, render, game, backdrop, floor, stair, trap, key, gate, wall, explorer,
                                          explorer_character, mummy_white_character,
                                          mummy_red_character, scorpion_white_character, scorpion_red_character,
                                          list_mummy_white,
                                          list_mummy_red, list_scorpion_white, list_scorpion_red)
            if isEnd:
                print("NUMBER STEP: {}".format(len(ans)-1))
                break

    isEnd = False
    render = True
    while agent == "KeyboardAgent" and not isEnd:
        explorer_x = explorer_character.get_x()
        explorer_y = explorer_character.get_y()
        explorer_new_x = explorer_x
        explorer_new_y = explorer_y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isEnd = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if explorer_character.eligible_character_move(game.maze, game.gate, explorer_x, explorer_y, explorer_x - 2, explorer_y):
                        explorer_new_x -= 2
                        explorer["direction"] = "UP"
                if event.key == pygame.K_DOWN:
                    if explorer_character.eligible_character_move(game.maze, game.gate, explorer_x, explorer_y, explorer_x + 2, explorer_y):
                        explorer_new_x += 2
                        explorer["direction"] = "DOWN"
                if event.key == pygame.K_LEFT:
                    if explorer_character.eligible_character_move(game.maze, game.gate, explorer_x, explorer_y, explorer_x, explorer_y - 2):
                        explorer_new_y -= 2
                        explorer["direction"] = "LEFT"
                if event.key == pygame.K_RIGHT:
                    if explorer_character.eligible_character_move(game.maze, game.gate, explorer_x, explorer_y, explorer_x, explorer_y + 2):
                        explorer_new_y += 2
                        explorer["direction"] = "RIGHT"
                if event.key == pygame.K_SPACE:
                    pass

                if explorer_x != explorer_new_x or explorer_y != explorer_new_y:
                    explorer_character.move(explorer_new_x, explorer_new_y, render, window, game, backdrop, floor,
                                             stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                             gate, game.gate, wall, explorer,
                                             list_mummy_white, list_mummy_red, list_scorpion_white, list_scorpion_red)
                print("Explorer position: {} {}".format(explorer_character.get_x(), explorer_character.get_y()))
                isEnd = update_enemy_position(window, render, game, backdrop, floor, stair, trap, key, gate, wall, explorer,
                                      explorer_character, mummy_white_character,
                                      mummy_red_character, scorpion_white_character, scorpion_red_character,
                                      list_mummy_white,
                                      list_mummy_red, list_scorpion_white, list_scorpion_red)
                if isEnd:
                    break

if __name__ == '__main__':
    project_path = os.getcwd()
    # Get map directory path
    map_path = os.path.join(project_path, "map")
    # Get maze directory path
    maze_path = os.path.join(map_path, "maze")
    # Get object position in maze
    object_path = os.path.join(map_path, "agents")
    print("===== CHOOSE LAYOUT ===== ")
    pre_layout = input("INPUT LAYOUT YOU WANT SOLVE: ")
    layout = pre_layout + ".txt"
    print("===== CHOOSE AGENT ===== ")
    print("1. KEYBOARD AGENT - YOU MUST FIND SOLUTION")
    print("2. SEARCH AGENT - A.I WILL FIND SOLUTION FOR YOU")
    check = False
    agent_choice = int(input("Input your choice: "))
    while not check:
        if agent_choice == 1:
            agent = "KeyboardAgent"
            check = True
        elif agent_choice == 2:
            agent = "SearchAgent"
            check = True
        else:
            check = False
        if not check:
            agent_choice = int(input("Input your choice: "))

    render = True
    rungame(layout, agent, render)