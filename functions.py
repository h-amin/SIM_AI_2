"""
-------------------------------------------------[GENERAL FLOW]---------------------------------------------------------

1. mob is in IDLE state / mob is in w_route (walking route) state
2. system recognizes player within 15m LoS distance
3. mob approaches player
4. mob enters 5m i_range (interactive range) for evaluation
5. system evaluates player level in correspondence to mob level
6. system establishes mob lvl >= player lvl
7. mob approaches player to initiate combat
8. OPTION 1: player out of reach for 8 seconds, enter Regen state
   OPTION 2: player in 3m combative reach (cmb_reach), enter Combat state
9. mob attacks player, vice versa
10. OPTION 1: mob hp down to 0, enter Defeat state
    OPTION 2: player hp down to 0, enter Victory state
    OPTION 3: player out of reach for 8 seconds, enter Victory state
    OPTION 4: combat state reaches 600 seconds, enter Victory state

-------------------------------------------------[COMBAT STATE]---------------------------------------------------------

max_distance    = 30   # meters
i_range         = 5    # meters
cmb_time        = 600  # seconds
cmb_reach       = 3    # meters
m_hp            = 100
p_hp            = 100
dps             = (0,11) # random

Player needs to be within 5m interactive range for the Combat state to uphold.
Should this not be the case, then the mob will enter the Victory state.

If the player is within the 3m cmb_reach, mob will attack it until player HP drops to 0 then proceed unto Victory state.
Should the player reduce mob HP to 0, then the Defeat state will be enabled.

If the player is NOT within 3m cmb_reach, mob will follow the player until it reaches a max distance
of 30m. With 30m being the distance delta between the original spot of combat initiation and max distance.
After reaching the 30m mark, mob will enter Victory state.

If the combat state takes longer than 600 seconds, the Victory state will be entered.

The damage of mob and player is a random integer between 0 and 11.
"""

import math

def calc_distance(pos1, pos2):
    dx = (pos1[0] - pos2[0]) ** 2
    dy = (pos1[1] - pos2[1]) ** 2
    distance = math.sqrt(dx + dy)
    return int(distance)


def summary(self, player):
    print("VARIABLES", end='\n')
    print(f"start_distance = {calc_distance(self.position, player.position)}")
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


def simulate(mob, player):
    state_transition = mob.states_transitions[mob.current_state]
    while True:
        player.turn(mob)
        mob.current_state = state_transition(mob, player)
        state_transition = mob.states_transitions[mob.current_state]