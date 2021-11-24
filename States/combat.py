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

import simpy
import random

MAX_DISTANCE = 30
I_RANGE = 5
CMB_TIME = 600
CMB_REACH = 3
M_HP = 100
P_HP = 100
DPS = random.randrange(11)

class Combat(object):
    def __init__(self, env, ):
        while True:
