'''
    author: Pham Manh Tien
    created: 06.07.2020
'''
import characters

class Queue:
    default_capacity = 100000000
    def __init__(self):
        self._data = [None] * Queue.default_capacity
        self._trace = [None]* Queue.default_capacity
        self._size = 0
        self._front = 0

    def __len__(self):
        # Return number element in the Queue
        return self._size

    def is_empty(self):
        return self._size == 0

    def pop(self):
        if self.is_empty():
            print("Queue is empty!")
        else:
            ans = self._data[self._front]
            self._front += 1
            self._size -= 1
        return ans

    def push(self, element):
        position = self._front + self._size
        self._data[position] = element
        self._size += 1
        self._trace[position] = self._front - 1
    def trace_back(self):
        print("NUMBER NODE HAVE EXPANDED: {}".format(self._front + self._size))
        ans = []
        p = self._front - 1
        while p != self._trace[0]:
            ans.append([self._data[p][0].get_x(), self._data[p][0].get_y()])
            p = self._trace[p]
        return ans

    def chech_exists_element_in_queue(self, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red, gate):
        is_exists = False
        for i in range(self._front + self._size):
            if self._data[i][0].get_x() != explorer.get_x() or self._data[i][0].get_y() != explorer.get_y():
                continue
            if len(self._data[i][1]) != len(mummy_white):
                continue
            else:
                next = False
                for j in range(len(mummy_white)):
                    if self._data[i][1][j].get_x() != mummy_white[j].get_x() or self._data[i][1][j].get_y() != mummy_white[j].get_y():
                        next = True
                        break
                if next:
                    continue
            if len(self._data[i][2]) != len(mummy_red):
                continue
            else:
                next = False
                for j in range(len(mummy_red)):
                    if self._data[i][2][j].get_x() != mummy_red[j].get_x() or self._data[i][2][j].get_y() != mummy_red[j].get_y():
                        next = True
                        break
                if next:
                    continue
            if len(self._data[i][3]) != len(scorpion_white):
                continue
            else:
                next = False
                for j in range(len(scorpion_white)):
                    if self._data[i][3][j].get_x() != scorpion_white[j].get_x() or self._data[i][3][j].get_y() != scorpion_white[j].get_y():
                        next = True
                        break
                if next:
                    continue
            if len(self._data[i][4]) != len(scorpion_red):
                continue
            else:
                next = False
                for j in range(len(scorpion_red)):
                    if self._data[i][4][j].get_x() != scorpion_red[j].get_x() or self._data[i][4][j].get_y() != scorpion_red[j].get_y():
                        next = True
                        break
                if next:
                    continue
            if self._data[i][5] and self._data[i][5]["isClosed"] != gate["isClosed"]:
                continue
            is_exists = True
            break
        return is_exists

def check_key_position(character, gate, key_position):
    if key_position and character.get_x() == key_position[0] and character.get_y() == key_position[1]:
        if gate["isClosed"]:
            gate["isClosed"] = False
        else:
            gate["isClosed"] = True
    return gate

def update_list_character(list_character):
    i = 0
    while i < len(list_character):
        j = 0
        while j < len(list_character):
            if j != i and list_character[i].check_same_position(list_character[j]):
                del list_character[j]
            j += 1
        i += 1
    return list_character

def update_lists_character(list_strong_scharacter, list_week_scharacter):
    for i in range(len(list_strong_scharacter)):
        j = 0
        while j < len(list_week_scharacter):
            if list_strong_scharacter[i].check_same_position(list_week_scharacter[j]):
                del list_week_scharacter[j]
            j += 1
    return list_week_scharacter

def check_explorer_is_killed(explorer_character, mummy_white_character, mummy_red_character, scorpion_white_character,
                            scorpion_red_character, trap_position):
    if trap_position and explorer_character.get_x() == trap_position[0] and explorer_character.get_y() == trap_position[1]:
        return True
    if mummy_white_character:
        for i in range(len(mummy_white_character)):
            if explorer_character.get_x() == mummy_white_character[i].get_x() and explorer_character.get_y() == mummy_white_character[i].get_y():
                return True
    if mummy_red_character:
        for i in range(len(mummy_red_character)):
            if explorer_character.get_x() == mummy_red_character[i].get_x() and explorer_character.get_y() == mummy_red_character[i].get_y():
                return True
    if scorpion_white_character:
        for i in range(len(scorpion_white_character)):
            if explorer_character.get_x() == scorpion_white_character[i].get_x() and explorer_character.get_y() == scorpion_white_character[i].get_y():
                return True
    if scorpion_red_character:
        for i in range(len(scorpion_red_character)):
            if explorer_character.get_x() == scorpion_red_character[i].get_x() and explorer_character.get_y() == scorpion_red_character[i].get_y():
                return True
    return False

def attempt_move(explorer_x, explorer_y, explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp,
                 current_gate_tmp, key_position, trap_position, maze):
    explorer_is_killed = False
    explorer_tmp.move_xy(explorer_x, explorer_y)
    if key_position:
        current_gate_tmp = check_key_position(explorer_tmp, current_gate_tmp, key_position)
    # FIRST MOVE
    # Mummy White
    for i in range(len(mummy_white_tmp)):
        mummy_white_tmp[i] = mummy_white_tmp[i].white_move(maze, current_gate_tmp, explorer_tmp)
    if key_position:
        for i in range(len(mummy_white_tmp)):
            current_gate_tmp = check_key_position(mummy_white_tmp[i], current_gate_tmp, key_position)
    # Mummy Red
    for i in range(len(mummy_red_tmp)):
        mummy_red_tmp[i] = mummy_red_tmp[i].red_move(maze, current_gate_tmp, explorer_tmp)
    if key_position:
        for i in range(len(mummy_red_tmp)):
            current_gate_tmp = check_key_position(mummy_red_tmp[i], current_gate_tmp, key_position)
    # Scorpion White
    for i in range(len(scorpion_white_tmp)):
        scorpion_white_tmp[i] = scorpion_white_tmp[i].white_move(maze, current_gate_tmp, explorer_tmp)
    if key_position:
        for i in range(len(scorpion_white_tmp)):
            current_gate_tmp = check_key_position(scorpion_white_tmp[i], current_gate_tmp, key_position)
    # Scorpion Red
    for i in range(len(scorpion_red_tmp)):
        scorpion_red_tmp[i] = scorpion_red_tmp[i].red_move(maze, current_gate_tmp, explorer_tmp)
    if key_position:
        for i in range(len(scorpion_red_tmp)):
            current_gate_tmp = check_key_position(scorpion_red_tmp[i], current_gate_tmp, key_position)

    explorer_is_killed = check_explorer_is_killed(explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp,
                                                  scorpion_red_tmp, trap_position)

    if not explorer_is_killed:
        # Delete mummy white have same position
        mummy_white_tmp = update_list_character(mummy_white_tmp)
        # Delete mummy red have same position
        mummy_red_tmp = update_list_character(mummy_red_tmp)
        # Delete scorpion white have same position
        scorpion_white_tmp = update_list_character(scorpion_white_tmp)
        # Delete scorpion red have same position
        scorpion_red_tmp = update_list_character(scorpion_red_tmp)
        # Delete mummy red, scropion white, scorpion red if mummy white have the same position
        if mummy_red_tmp:
            mummy_red_tmp = update_lists_character(mummy_white_tmp, mummy_red_tmp)
        if scorpion_white_tmp:
            scorpion_white_tmp = update_lists_character(mummy_white_tmp, scorpion_white_tmp)
        if scorpion_red_tmp:
            scorpion_red_tmp = update_lists_character(mummy_white_tmp, scorpion_red_tmp)
        # Delete scropion white, scorpion red if mummy red have the same position
        if scorpion_white_tmp:
            scorpion_white_tmp = update_lists_character(mummy_red_tmp, scorpion_white_tmp)
        if scorpion_red_tmp:
            scorpion_red_tmp = update_lists_character(mummy_red_tmp, scorpion_red_tmp)
        # Delete scorpion red if scorpion white have the same position
        if scorpion_red_tmp:
            scorpion_red_tmp = update_lists_character(scorpion_white_tmp, scorpion_red_tmp)

    # SECOND MOVE
        # Mummy White
        for i in range(len(mummy_white_tmp)):
            mummy_white_tmp[i] = mummy_white_tmp[i].white_move(maze, current_gate_tmp, explorer_tmp)
        if key_position:
            for i in range(len(mummy_white_tmp)):
                current_gate_tmp = check_key_position(mummy_white_tmp[i], current_gate_tmp, key_position)
        # Mummy Red
        for i in range(len(mummy_red_tmp)):
            mummy_red_tmp[i] = mummy_red_tmp[i].red_move(maze, current_gate_tmp, explorer_tmp)
        if key_position:
            for i in range(len(mummy_red_tmp)):
                current_gate_tmp = check_key_position(mummy_red_tmp[i], current_gate_tmp, key_position)
        # Delete mummy white have same position
        mummy_white_tmp = update_list_character(mummy_white_tmp)
        # Delete mummy red have same position
        mummy_red_tmp = update_list_character(mummy_red_tmp)
        # Delete mummy red, scropion white, scorpion red if mummy white have the same position
        if mummy_red_tmp:
            mummy_red_tmp = update_lists_character(mummy_white_tmp, mummy_red_tmp)
        if scorpion_white_tmp:
            scorpion_white_tmp = update_lists_character(mummy_white_tmp, scorpion_white_tmp)
        if scorpion_red_tmp:
            scorpion_red_tmp = update_lists_character(mummy_white_tmp, scorpion_red_tmp)
        # Delete scropion white, scorpion red if mummy red have the same position
        if scorpion_white_tmp:
            scorpion_white_tmp = update_lists_character(mummy_red_tmp, scorpion_white_tmp)
        if scorpion_red_tmp:
            scorpion_red_tmp = update_lists_character(mummy_red_tmp, scorpion_red_tmp)
        explorer_is_killed = check_explorer_is_killed(explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp,
                                                      scorpion_red_tmp, trap_position)

    return explorer_is_killed

def BFS(explorer_character, mw_character, mr_character, sw_character, sr_character, gate, trap_position, key_position, maze):
    queue = Queue()
    queue.push([explorer_character, mw_character, mr_character, sw_character, sr_character, gate])
    while not queue.is_empty():
        character = queue.pop()
        explorer = character[0]
        mummy_white = character[1]
        mummy_red = character[2]
        scorpion_white = character[3]
        scorpion_red = character[4]
        current_gate = character[5]

        explorer_x = explorer.get_x()
        explorer_y = explorer.get_y()
        if maze[explorer_x - 1][explorer_y] == "S" or maze[explorer_x + 1][explorer_y] == "S" or \
                maze[explorer_x][explorer_y - 1] == "S" or maze[explorer_x][explorer_y + 1] == "S":
            return queue.trace_back()
            break
        # if explorer Move Up
        explorer_tmp = characters.Explorer(explorer_x, explorer_y)
        mummy_white_tmp = []
        for i in range(len(mummy_white)):
            mummy_white_tmp.append(characters.mummy_white(mummy_white[i].get_x(), mummy_white[i].get_y()))
        mummy_red_tmp = []
        for i in range(len(mummy_red)):
            mummy_red_tmp.append(characters.mummy_red(mummy_red[i].get_x(), mummy_red[i].get_y()))
        scorpion_white_tmp = []
        for i in range(len(scorpion_white)):
            scorpion_white_tmp.append(characters.scorpion_white(scorpion_white[i].get_x(), scorpion_white[i].get_y()))
        scorpion_red_tmp = []
        for i in range(len(scorpion_red)):
            scorpion_red_tmp.append(characters.scorpion_red(scorpion_red[i].get_x(), scorpion_red[i].get_y()))
        current_gate_tmp = current_gate.copy()
        if explorer_tmp.eligible_character_move(maze, current_gate_tmp, explorer_x, explorer_y, explorer_x - 2, explorer_y):
            if not attempt_move(explorer_x - 2, explorer_y, explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp,
                 current_gate_tmp, key_position, trap_position, maze):
                if not queue.chech_exists_element_in_queue(explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp,
                                                         scorpion_red_tmp, current_gate_tmp):
                    queue.push([explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp, current_gate_tmp])

        # if explorer Move Down
        explorer_tmp = characters.Explorer(explorer_x, explorer_y)
        mummy_white_tmp = []
        for i in range(len(mummy_white)):
            mummy_white_tmp.append(characters.mummy_white(mummy_white[i].get_x(), mummy_white[i].get_y()))
        mummy_red_tmp = []
        for i in range(len(mummy_red)):
            mummy_red_tmp.append(characters.mummy_red(mummy_red[i].get_x(), mummy_red[i].get_y()))
        scorpion_white_tmp = []
        for i in range(len(scorpion_white)):
            scorpion_white_tmp.append(characters.scorpion_white(scorpion_white[i].get_x(), scorpion_white[i].get_y()))
        scorpion_red_tmp = []
        for i in range(len(scorpion_red)):
            scorpion_red_tmp.append(characters.scorpion_red(scorpion_red[i].get_x(), scorpion_red[i].get_y()))
        current_gate_tmp = current_gate.copy()
        if explorer_tmp.eligible_character_move(maze, current_gate_tmp, explorer_x, explorer_y, explorer_x + 2, explorer_y):
            if not attempt_move(explorer_x + 2, explorer_y, explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp,
                 current_gate_tmp, key_position, trap_position, maze):
                if not queue.chech_exists_element_in_queue(explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp,
                                                         scorpion_red_tmp, current_gate_tmp):
                    queue.push([explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp, current_gate_tmp])

        # if explorer Move Left
        explorer_tmp = characters.Explorer(explorer_x, explorer_y)
        mummy_white_tmp = []
        for i in range(len(mummy_white)):
            mummy_white_tmp.append(characters.mummy_white(mummy_white[i].get_x(), mummy_white[i].get_y()))
        mummy_red_tmp = []
        for i in range(len(mummy_red)):
            mummy_red_tmp.append(characters.mummy_red(mummy_red[i].get_x(), mummy_red[i].get_y()))
        scorpion_white_tmp = []
        for i in range(len(scorpion_white)):
            scorpion_white_tmp.append(characters.scorpion_white(scorpion_white[i].get_x(), scorpion_white[i].get_y()))
        scorpion_red_tmp = []
        for i in range(len(scorpion_red)):
            scorpion_red_tmp.append(characters.scorpion_red(scorpion_red[i].get_x(), scorpion_red[i].get_y()))
        current_gate_tmp = current_gate.copy()
        if explorer_tmp.eligible_character_move(maze, current_gate_tmp, explorer_x, explorer_y, explorer_x, explorer_y - 2):
            if not attempt_move(explorer_x, explorer_y - 2, explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp,
                 current_gate_tmp, key_position, trap_position, maze):
                if not queue.chech_exists_element_in_queue(explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp,
                                                     scorpion_red_tmp, current_gate_tmp):
                    queue.push([explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp, current_gate_tmp])

        # if explorer Move Right
        explorer_tmp = characters.Explorer(explorer_x, explorer_y)
        mummy_white_tmp = []
        for i in range(len(mummy_white)):
            mummy_white_tmp.append(characters.mummy_white(mummy_white[i].get_x(), mummy_white[i].get_y()))
        mummy_red_tmp = []
        for i in range(len(mummy_red)):
            mummy_red_tmp.append(characters.mummy_red(mummy_red[i].get_x(), mummy_red[i].get_y()))
        scorpion_white_tmp = []
        for i in range(len(scorpion_white)):
            scorpion_white_tmp.append(characters.scorpion_white(scorpion_white[i].get_x(), scorpion_white[i].get_y()))
        scorpion_red_tmp = []
        for i in range(len(scorpion_red)):
            scorpion_red_tmp.append(characters.scorpion_red(scorpion_red[i].get_x(), scorpion_red[i].get_y()))
        current_gate_tmp = current_gate.copy()
        if explorer_tmp.eligible_character_move(maze, current_gate_tmp, explorer_x, explorer_y, explorer_x, explorer_y + 2):
            if not attempt_move(explorer_x, explorer_y + 2, explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp,
                 current_gate_tmp, key_position, trap_position, maze):
                 if not queue.chech_exists_element_in_queue(explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp,
                                                      scorpion_red_tmp, current_gate_tmp):
                    queue.push([explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp, current_gate_tmp])

        # if explorer still standing
        explorer_tmp = characters.Explorer(explorer_x, explorer_y)
        mummy_white_tmp = []
        for i in range(len(mummy_white)):
            mummy_white_tmp.append(characters.mummy_white(mummy_white[i].get_x(), mummy_white[i].get_y()))
        mummy_red_tmp = []
        for i in range(len(mummy_red)):
            mummy_red_tmp.append(characters.mummy_red(mummy_red[i].get_x(), mummy_red[i].get_y()))
        scorpion_white_tmp = []
        for i in range(len(scorpion_white)):
            scorpion_white_tmp.append(characters.scorpion_white(scorpion_white[i].get_x(), scorpion_white[i].get_y()))
        scorpion_red_tmp = []
        for i in range(len(scorpion_red)):
            scorpion_red_tmp.append(characters.scorpion_red(scorpion_red[i].get_x(), scorpion_red[i].get_y()))
        current_gate_tmp = current_gate.copy()
        if not attempt_move(explorer_x, explorer_y, explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp,
                        scorpion_red_tmp,
                        current_gate_tmp, key_position, trap_position, maze):
            is_the_same_state = True
            if len(mummy_white) != len(mummy_white_tmp):
                is_the_same_state = False
            else:
                for i in range(len(mummy_white_tmp)):
                    if not mummy_white[i].check_same_position(mummy_white_tmp[i]):
                        is_the_same_state = False
                        break
            if is_the_same_state:
                if len(mummy_red) != len(mummy_red_tmp):
                    is_the_same_state = False
                else:
                    for i in range(len(mummy_red_tmp)):
                        if not mummy_red[i].check_same_position(mummy_red_tmp[i]):
                            is_the_same_state = False
                            break

            if is_the_same_state:
                if len(scorpion_white) != len(scorpion_white_tmp):
                    is_the_same_state = False
                else:
                    for i in range(len(scorpion_white_tmp)):
                        if not scorpion_white[i].check_same_position(scorpion_white_tmp[i]):
                            is_the_same_state = False
                            break

            if is_the_same_state:
                if len(scorpion_red) != len(scorpion_red_tmp):
                    is_the_same_state = False
                else:
                    for i in range(len(scorpion_red_tmp)):
                        if not scorpion_red[i].check_same_position(scorpion_red_tmp[i]):
                            is_the_same_state = False
                            break
            if is_the_same_state:
                if current_gate and current_gate["isClosed"] != current_gate_tmp["isClosed"]:
                    is_the_same_state = False
            if not is_the_same_state:
                queue.push([explorer_tmp, mummy_white_tmp, mummy_red_tmp, scorpion_white_tmp, scorpion_red_tmp, current_gate_tmp])