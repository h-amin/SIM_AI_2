import math
import random
import threading
import time
import functions

# Clock is used to track the time. CLOCK_SPEED is the amount of time th simulation has passed in 1 second of the
# real world time
CLOCK_SPEED = 2


class Clock:
    def __init__(self):
        self.current_time = 0

    def background(self):
        while True:
            time.sleep(1)
            self.current_time += CLOCK_SPEED

    def run(self):
        background_task = threading.Thread(target=self.background)
        background_task.start()

# Player plays an important role in the simulation, because we need to know the lvl and distance of the player in
# certain states to determine what the next state of the mob should be. In the mob simulation we also needed to simulate
# the player behaviour, because it is unrealistic to have a player idle all the time, for simulating the players
# there are 2 options, one is to handle the player behaviour by ourself by providing input, the other is to hardcode
# behaviour of the player. To keep it simple at every turn, the player moves 1 unit vector towards the mob.


class Player:
    def __init__(self, lvl):
        self.hp = 100
        self.lvl = lvl
        self.position = [15, 15]

    def turn(self, mob):
        distance = functions.calc_distance(self.position, mob.position)
        print(f"\nPlayer position: {int(self.position[0])} X, {int(self.position[1])} Y coordinates, mob position: {int(mob.position[0])} X, {int(mob.position[1])} Y."
              f"distance: {distance} meters")
        # move = int(input("type 0 to move towards mob, type 1 to stay idle, type 2 to run:\n"))
        move = 0
        if move == 0:
            # 1 stap van een speler is 1 meter, dus 1 meter richting mob
            time.sleep(1)
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

# Mob is the FSM we wanted to simulate in this project. the mob has an clock, which keeps track of the time the moment
# when the mob is instantiated. The time is necessary to get out of the Idle, Victory and Defeat state.
# The start state of the FSM is the Idle state, there is no end state. The simulation will end in 100 seconds
# (in clock time of the mob, not real world) after the player has a higher lvl then the mob


class MobStateMachine:
    def summary(self, player):
        # print("VARIABLES", end='\n')
        print(f"start_distance = {functions.calc_distance(self.position, player.position)}")
        print(f"mob_lvl = {self.lvl}")
        print(f"player_lvl = {player.lvl}")
        print(f"current_state: {self.current_state}")
        print(f"clock {self.clock.current_time}")

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
player = Player(lvl=random.randint(70, 90))
functions.simulate(mob, player)

