class Server:
    def __init__(self):
        self.flagged = []
        self.strikes = {}
        self.flags_number = 1
        self.mod_type = {'ping':True, 'automatic':False, 'democracy':False, 'strikes':True}
        self.strike_limit = 3

    def add_flag(self, message):
        self.flagged.append(message)
        self.flags_number += 1

    def list_flags(self):
        flags = []
        for flag in self.flagged:
            flags.append([flag.number, flag.sender.name, flag.content])
        return flags

    def get_flag_number(self):
        return self.flags_number
