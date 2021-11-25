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


