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


def idle_transitions(mob, player):
    mob.current_state = "IDLE"
    mob.summary(player)
    if player_in_range(mob, player.position):
        return player_approach_transitions(mob, player)
    if mob.clock.current_time - mob.start_idle_time < 60:
        return "IDLE"
    else:
        return walk_transitions(mob, player)


def player_in_range(mob, player_pos):
    if calc_distance(mob.position, player_pos) < 15:
        return True
    else:
        return False


def combat_transitions(mob, player):
    mob.current_state = "COMBAT"
    mob.summary(player)
    if mob.lvl > player.lvl:
        mob.victory_time = mob.clock.current_time
        print("player got killed")
        player.respawn(mob)
        return victory_transitions(mob, player)
    else:
        mob.hp = 0
        return defeat_transitions(mob, player)


def walk_transitions(mob, player):
    mob.current_state = "WALK"
    mob.summary(player)
    if calc_distance(mob.position, player.position) <= 15:
        return player_approach_transitions(mob, player)
    else:
        return "WALK"


def respawn_transitions(mob, player):
    mob.current_state = "RESPAWN"
    mob.summary(player)
    mob.hp = 100
    mob.position = [0, 0]
    return idle_transitions(mob, player)


def defeat_transitions(mob, player):
    mob.current_state = "DEFEAT"
    mob.summary(player)
    return respawn_transitions(mob, player)


def regen_transitions(mob, player):
    mob.current_state = "REGEN"
    mob.summary(player)
    return bot_transitions(mob, player)


def victory_transitions(mob, player):
    mob.current_state = "VICTORY"
    mob.summary(player)
    if mob.clock.current_time - mob.victory_time >= 3:
        return regen_transitions(mob, player)
    else:
        return "VICTORY"


def aggro_transitions(mob, player):
    mob.current_state = "AGGRO"
    mob.summary(player)
    if calc_distance(mob.position, player.position) <= 2:
        return combat_transitions(mob, player)
    else:
        move_towards_player(mob, player)
        return "AGGRO"


def eval_transitions(mob, player):
    mob.current_state = "EVAL"
    mob.summary(player)
    if mob.lvl > player.lvl:
        return aggro_transitions(mob, player)
    else:
        return bot_transitions(mob, player)


def bot_transitions(mob, player):
    mob.current_state = "BOT"
    mob.summary(player)
    return walk_transitions(mob, player)


def player_approach_transitions(mob, player):
    mob.current_state = "PLAYER_APPROACH"
    mob.summary(player)
    distance = calc_distance(mob.position, player.position)
    if distance > 15:
        return bot_transitions(mob, player)
    elif distance <= 5:
        return eval_transitions(mob, player)
    else:
        move_towards_player(mob, player)

    new_distance = calc_distance(mob.position, player.position)
    if new_distance <= 5:
        return eval_transitions(mob, player)
    else:
        return "PLAYER_APPROACH"


def move_towards_player(mob, player):
    distance = calc_distance(mob.position, player.position)
    dx, dy = (player.position[0] - mob.position[0], player.position[1] - mob.position[1])
    # unit vector van de directional vector
    udx, udy = (dx / distance, dy / distance)
    mob.position[0] = mob.position[0] + 0.9 * udx
    mob.position[1] = mob.position[1] + 0.9 * udy


def simulate(mob, player):
    state_transition = mob.states_transitions[mob.current_state]
    while True:
        player.turn(mob)
        mob.current_state = state_transition(mob, player)
        state_transition = mob.states_transitions[mob.current_state]