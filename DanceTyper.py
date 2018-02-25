import copy

import PredictiveCode

letters = {
    ('circle', 'circle'): ')',
    ('circle', 'cross'): '(',
    ('circle', 'down'): '\n',
    ('circle', 'left'): '-',
    ('circle', 'right'): '+',
    ('circle', 'triangle'): '*',
    ('circle', 'up'): '0',
    ('cross', 'circle'): '8',
    ('cross', 'cross'): '7',
    ('cross', 'down'): '4',
    ('cross', 'left'): '5',
    ('cross', 'right'): '6',
    ('cross', 'triangle'): '9',
    ('cross', 'up'): '3',
    ('down', 'circle'): 'd',
    ('down', 'cross'): 's',
    ('down', 'down'): 'o',
    ('down', 'left'): 'p',
    ('down', 'right'): 'a',
    ('down', 'triangle'): 'f',
    ('down', 'up'): 'i',
    ('left', 'circle'): 'z',
    ('left', 'cross'): 'l',
    ('left', 'down'): 'h',
    ('left', 'left'): 'j',
    ('left', 'right'): 'k',
    ('left', 'triangle'): 'x',
    ('left', 'up'): 'g',
    ('right', 'circle'): '1',
    ('right', 'cross'): 'm',
    ('right', 'down'): 'v',
    ('right', 'left'): 'b',
    ('right', 'right'): 'n',
    ('right', 'triangle'): '2',
    ('right', 'up'): 'c',
    ('triangle', 'triangle'): ' ',
    ('triangle', 'circle'): '"',
    ('up', 'circle'): 'y',
    ('up', 'cross'): 't',
    ('up', 'down'): 'w',
    ('up', 'left'): 'e',
    ('up', 'right'): 'r',
    ('up', 'triangle'): 'u',
    ('up', 'up'): 'q'
}

special = {
    ('triangle', 'up'): 'up_line',
    ('triangle', 'down'): 'down_line',
    ('triangle', 'left'): 'pos_left',
    ('triangle', 'right'): 'pos_right',
    ('square', 'square'): 'remove_current',
    ('square', 'cross'): 'predictive_mode'
}

special_prediction = {
    ('left', 'left'): "prev_prediction",
    ('right', 'right'): "next_prediction",
    ('square', 'square'): "exit_prediction_mode",
    ('cross','cross'): "select_prediction"
}

# Handles our Code buffer objects.
class DanceTyper:
    def __init__(self):
        self.previous_actions = []
        self.predict_actions = []
        self.document = []
        self.document_pos = []
        self.new_line()
    # basically, convert the line into human readable form.
    @staticmethod
    def parse(line):
        return "".join(line)
    # Add a button press to the object.
    def add_key(self, key, line):
        if len(self.previous_actions) >= 0:
            self.previous_actions[line].append(key)
            if len(self.previous_actions[line]) < 2 or \
                    len(self.previous_actions[line]) % 2 != 0:
                return
            try:
                lookup = letters[(self.previous_actions[line][-2],
                          self.previous_actions[line][-1])]
                self.document[line].insert(self.document_pos[line], lookup)
                self.document_pos[line] += 1
            except KeyError:
                # check if it's a special combo
                lookup = (self.previous_actions[line][-2],
                          self.previous_actions[line][-1])
                if lookup in special:
                    return special[lookup]
                self.previous_actions[line] = self.previous_actions[line][:-2]

    def remove_key(self, line, pos=-1):
        if len(self.previous_actions) > line and self.document[line] != []:
            if len(self.previous_actions[line]) % 2 == 0 and \
                    len(self.previous_actions) > 0:
                self.previous_actions[line].pop(pos)
                self.previous_actions[line].pop(pos)
            elif len(self.previous_actions[line]) == 1:
                self.previous_actions[line].pop(pos)
            else:
                for i in range(0, 3):
                    self.previous_actions[line].pop(pos)

            self.document[line].pop(pos)
            if self.document_pos[line] > 0:
                self.document_pos[line] -= 1
    # Display it.
    def display_line(self, number):
        if len(self.document) < number:
            return None
        line = self.document[number]
        return self.parse(line)

    # Add a new line at a certain line position. Default is the end.
    def new_line(self, location=-1):
        if location == -1:
            self.document.append([])
            self.previous_actions.append([])
            self.predict_actions.append([])
            self.document_pos.append(0)
        else:
            self.document = self.document[:location] + copy.deepcopy([[]]) + \
                self.document[location:]
            self.previous_actions = self.previous_actions[:location] + \
                copy.deepcopy([[]]) + self.previous_actions[location:]
            self.predict_actions = self.predict_actions[:location] + \
                copy.deepcopy([[]]) + self.predict_actions[location:]
            self.document_pos = self.document_pos[:location] + [0]  + \
                self.document_pos[location:]

    def remove_line(self, location=-1):
        self.previous_actions.pop(location)
        self.document.pop(location)
        self.document_pos.pop(location)
        # Both get removed at the same time, so just check one.
        if self.previous_actions == []:
            self.new_line()

    def lines(self):
        return len(self.document)

    def pos(self, line):
        try:
            return self.document_pos[line]
        except:
            return 0

    def inprogress(self, line):
        if (len(self.previous_actions[line])%2==0 and \
                len(self.previous_actions[line]) != 0):
            return "n"
        return "y"

    def changepos(self, line, new_pos):
        if new_pos < 0 or new_pos > len(self.document[line]): return
        self.document_pos[line] = new_pos

    def append_to_pos(self, line, value):
        self.document[line] = self.document[line][:self.document_pos[line]] + \
            list(value) + self.document[line][self.document_pos[line]:]
        self.document_pos[line] += len(value)

    def predict_handler(self, key, line):
        if (len(self.predict_actions) >= 0):
            self.predict_actions[line].append(key)
            if len(self.predict_actions[line]) < 2 or \
                    len(self.predict_actions[line]) % 2 != 0:
                return

            try:
                lookup = (self.predict_actions[line][-2],
                        self.predict_actions[line][-1])
                if lookup in special_prediction:
                    return special_prediction[lookup]
                self.previous_actions[line] = self.previous_actions[line][:-2]
            except:
                pass
