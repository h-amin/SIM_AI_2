import math
import random
import threading
import time
import functions

MAX_DISTANCE = 30
I_RANGE = 5
CMB_TIME = 600
CMB_REACH = 3
M_HP = 100
P_HP = 100
DPS = random.randrange(11)


def calc_distance(pos1, pos2):
    dx = (pos1[0] - pos2[0]) ** 2
    dy = (pos1[1] - pos2[1]) ** 2
    distance = math.sqrt(dx + dy)
    return int(distance)


class Clock:
    def __init__(self):
        self.current_time = 0

    def background(self):
        while True:
            time.sleep(1)
            self.current_time += 2

    def run(self):
        background_task = threading.Thread(target=self.background)
        background_task.start()


class Player:
    def __init__(self, lvl):
        self.hp = 100
        self.lvl = lvl
        self.position = [15, 15]

    def turn(self, mob):
        distance = calc_distance(self.position, mob.position)
        print(f"\nPlayer position {self.position}, mob position {mob.position}, "
              f"distance: {distance}")
        # move = int(input("type 0 to move towards mob, type 1 to stay idle, type 2 to run:\n"))
        move = 0
        if move == 0:
            # 1 stap van een speler is 1 meter, dus 1 meter richting mob
            time.sleep(3)
            dx, dy = (mob.position[0] - self.position[0], mob.position[1] - self.position[1])
            # unit vector van de directional vector
            udx, udy = (dx / distance, dy / distance)
            self.position[0] = self.position[0] + udx
            self.position[1] = self.position[1] + udy

        if move == 1:
            pass
        if move == 2:
            pass

    def respawn(self, mob):
        self.hp = 100
        self.lvl += 3
        self.position = [mob.position[0] + 10, mob.position[1] + 10]


class MobStateMachine:
    def __init__(self, hp, lvl):
        self.clock = Clock()
        self.clock.run()
        self.start_idle_time = self.clock.current_time
        self.hp = hp
        self.lvl = lvl
        self.victory_time = None
        self.start_state = "IDLE"
        self.end_state = None
        self.position = [0, 0]
        self.states_transitions = {
            "IDLE": functions.idle_transitions,
            "PLAYER_APPROACH": functions.player_approach_transitions,
            "COMBAT": functions.combat_transitions,
            "WALK": functions.walk_transitions,
            "RESPAWN": functions.respawn_transitions,
            "DEFEAT": functions.defeat_transitions,
            "VICTORY": functions.victory_transitions,
            "AGGRO": functions.aggro_transitions,
            "EVAL": functions.eval_transitions,
            "BACKONTRACK": functions.bot_transitions,
            "REGEN": functions.regen_transitions
        }
        self.current_state = self.start_state


mob = MobStateMachine(hp=100, lvl=100)
functions.simulate()
