import math
import random
import threading
import time


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
            udx, udy = (dx/distance, dy/distance)
            self.position[0] = self.position[0] + udx
            self.position[1] = self.position[1] + udy

        if move == 1:
            pass
        if move == 2:
            pass

    def respawn(self, mob):
        self.hp = 100
        self.lvl += 3
        self.position = [mob.position[0] + 10, mob.position[1]+10]


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
            "IDLE": self.idle_transitions,
            "PLAYER_APPROACH": self.player_approach_transitions,
            "COMBAT": self.combat_transitions,
            "WALK": self.walk_transitions,
            "RESPAWN": self.respawn_transitions,
            "DEFEAT": self.defeat_transitions,
            "VICTORY": self.victory_transitions,
            "AGGRO": self.aggro_transitions,
            "EVAL": self.eval_transitions,
            "BACKONTRACK": self.bot_transitions,
            "REGEN": self.regen_transitions
        }
        self.current_state = self.start_state

    def summary(self, player):
        print("VARIABLES", end='\n')
        print(f"start_distance = {calc_distance(self.position,player.position)}")
        print(f"mob_lvl = {self.lvl}")
        print(f"player_lvl = {player.lvl}")
        print(f"current_state: {self.current_state}")
        print(f"clock {self.clock.current_time}")

    def idle_transitions(self, player):
        self.current_state = "IDLE"
        self.summary(player)
        if self.player_in_range(player.position):
            return self.player_approach_transitions(player)
        if self.clock.current_time - self.start_idle_time < 60:
            return "IDLE"
        else:
            return self.walk_transitions(player)

    def player_in_range(self, player_pos):

        if calc_distance(self.position, player_pos) < 15:
            return True
        else:
            return False

    def combat_transitions(self, player):
        self.current_state = "COMBAT"
        self.summary(player)
        if self.lvl > player.lvl:
            self.victory_time = self.clock.current_time
            print("player got killed")
            player.respawn(self)
            return self.victory_transitions(player)
        else:
            self.hp = 0
            return self.defeat_transitions(player)

    def walk_transitions(self, player):
        self.current_state = "WALK"
        self.summary(player)
        if calc_distance(self.position, player.position) <= 15:
            return self.player_approach_transitions(player)
        else:
            return "WALK"

    def respawn_transitions(self, player):
        self.current_state = "RESPAWN"
        self.summary(player)
        self.hp = 100
        self.position = [0, 0]
        return self.idle_transitions(player)

    def defeat_transitions(self, player):
        self.current_state = "DEFEAT"
        self.summary(player)
        return self.respawn_transitions(player)

    def regen_transitions(self, player):
        self.current_state = "REGEN"
        self.summary(player)
        return self.bot_transitions(player)

    def victory_transitions(self, player):
        self.current_state = "VICTORY"
        self.summary(player)
        if self.clock.current_time - self.victory_time >= 3:
            return self.regen_transitions(player)
        else:
            return "VICTORY"

    def aggro_transitions(self, player):
        self.current_state = "AGGRO"
        self.summary(player)
        if calc_distance(self.position, player.position) <= 2:
            return self.combat_transitions(player)
        else:
            self.move_towards_player(player)
            return "AGGRO"

    def eval_transitions(self, player):
        self.current_state = "EVAL"
        self.summary(player)
        if self.lvl > player.lvl:
            return self.aggro_transitions(player)
        else:
            return self.bot_transitions(player)

    def bot_transitions(self, player):
        self.current_state = "BOT"
        self.summary(player)
        return self.walk_transitions(player)

    def player_approach_transitions(self, player):
        self.current_state = "PLAYER_APPROACH"
        self.summary(player)
        distance = calc_distance(self.position, player.position)
        if distance > 15:
            return self.bot_transitions(player)
        elif distance <= 5:
            return self.eval_transitions(player)
        else:
            self.move_towards_player(player)

        new_distance = calc_distance(self.position, player.position)
        if new_distance <= 5:
            return self.eval_transitions(player)
        else:
            return "PLAYER_APPROACH"

    def move_towards_player(self, player):
        distance = calc_distance(mob.position, player.position)
        dx, dy = (player.position[0] - self.position[0], player.position[1] - self.position[1])
        # unit vector van de directional vector
        udx, udy = (dx / distance, dy / distance)
        self.position[0] = self.position[0] + 0.9 * udx
        self.position[1] = self.position[1] + 0.9 * udy

    def simulate(self):
        state_transition = self.states_transitions[self.current_state]
        player = Player(lvl=80)
        while True:
            player.turn(mob=self)
            self.current_state = state_transition(player)
            state_transition = self.states_transitions[self.current_state]


mob = MobStateMachine(hp=100, lvl=100)
mob.simulate()
