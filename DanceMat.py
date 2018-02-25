from inputs import get_gamepad
import os
import hy
import json

import MapInput
import DanceTyper

class DanceMat:
    def __init__(self):
        self.line = 0
        self.typer = DanceTyper.DanceTyper()
        self.mode = "INSERT"

    def _process_event(self, event):
        details = MapInput.map_input(event)
        self.event_handler(details)
    # start the event loop
    def run(self):
        while True:
            events = get_gamepad()
            for event in events:
                self._process_event(event)
    def event_handler(self, details):
        if details == None:
            return None
        if details[1] == 0: return False # was just unpressed
        # Check if 
        if details[0] in ['start', 'select']:
            # our control actions.
            if details[0] == "start":
                print ("> Executing")
                try:
                    expression = hy.read_str(self.typer.display_line(self.line))
                    print "Result:",hy.eval(expression)
                except Exception as e:
                    print "Exception:",e.__str__()
            elif details[0] == "select":
                self.typer.remove_line(self.line)
        else:
            # Now add to this line
            result = self.typer.add_key(details[0], self.line)
            # check if the user typed a special key combo
            if (result != None):
                if result == 'up_line':
                    self.line -= 1
                    if self.line <= 0:
                        self.line = 0
                elif result == 'down_line':
                    if self.line < self.typer.lines()-1:
                        self.line += 1
                    elif self.line == self.typer.lines()-1:
                        self.line += 1
                        self.typer.new_line()
                elif result == 'pos_left':
                    self.typer.changepos(self.line, self.typer.pos(self.line)-1)
                elif result == 'pos_right':
                    self.typer.changepos(self.line, self.typer.pos(self.line)+1)
                elif result == 'remove_current':
                    self.typer.remove_key(self.line)
        # Stupid prompt.
        prompt = "dp {} {} {} {}> ".format(self.mode,self.line, \
                                    self.typer.pos(self.line), \
                                    self.typer.inprogress(self.line))
        print("{} {}".format(prompt, self.typer.display_line(self.line)))
        print("{} ^".format(" "*(len(prompt)+self.typer.pos(self.line))))


if __name__ == "__main__":
    dance = DanceMat()
    dance.run()
