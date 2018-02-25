from inputs import get_gamepad
import os
import hy
import json
import re
import asyncio
import datetime
import random
import websockets

import MapInput
import DanceTyper
import PredictiveCode

def get_current_word(line, position):
    try:
        if line[position] in "() ": return ""
        first = re.findall(r"[\w]+",line[:position])
        second = re.findall(r"[\w]+",line[position:])
        if first == []: first = line[:position]
        if second == []: second = line[postion:]
        return first[-1]+second[0]
    except:
        return ""

class DanceMat:
    def __init__(self):
        self.line = 0
        self.typer = DanceTyper.DanceTyper()
        self.mode = "INSERT"
        self.predictor = PredictiveCode.Predictor()
        self.predictions_found = []
        self.curr_pred = 0
        self.last_returned = ""

    def predictions(self):
        self.curr = (get_current_word(self.typer.display_line(self.line),
                             self.typer.pos(self.line)-1))
        self.predictions_found = self.predictor.predict(self.curr)
        self.curr_pred = 0
        if self.predictions_found == []:
            print("unable to predict. non found")
            self.mode = "INSERT"

    async def _process_event(self, event, websocket):
        details = MapInput.map_input(event)
        await self.event_handler(details, websocket)

    # start the event loop
    def run(self):
        start_server = websockets.serve(self.websocket_server, '127.0.0.1', 5678)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def websocket_server(self, websocket, path):
        while True:
            events = get_gamepad()
            for event in events:
                await self._process_event(event, websocket)

    async def event_handler(self, details, websocket):
        if details == None:
            return None
        if details[1] == 0: return False # was just unpressed
        # Check if
        if details[0] in ['start', 'select']:
            # our control actions.
            if details[0] == "start":
                print("> Executing")
                try:
                    expression = hy.read_str(self.typer.display_line(self.line))
                    print("Result:",hy.eval(expression))
                    self.last_returned = hy.eval(expression)
                except Exception as e:
                    print("Exception:",e.__str__())
            elif details[0] == "select":
                self.typer.remove_line(self.line)
        else:
            # Are we in prediction mode or not
            if self.mode == "PREDICT":
                result = self.typer.predict_handler(details[0], self.line)
                if (result != None):
                    if result == "next_prediction":
                        self.curr_pred = (self.curr_pred + 1) \
                            % len(self.predictions_found)
                    elif result == "prev_prediction":
                        self.curr_pred = (self.curr_pred - 1) \
                            % len(self.predictions_found)
                    elif result == "select_prediction":
                        self.typer.append_to_pos(self.line,
                                (self.predictions_found[self.curr_pred]+" ")[len(self.curr):])
                        self.mode = "INSERT"
                        self.predictions_found = []
                        self.curr_pred = []
                    elif result == "exit_prediction_mode":
                        self.mode = "INSERT"
                        self.predictions_found = []
                        self.curr_pred = []
            elif self.mode == "INSERT":
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
                    elif result == 'predictive_mode':
                        self.mode = "PREDICT"
                        self.predictions()
        # Get word we are working on
        # Stupid prompt.
        prompt = "dp {} {} {} {}> ".format(self.mode,self.line, \
                                    self.typer.pos(self.line), \
                                    self.typer.inprogress(self.line))
        print("{} {}".format(prompt, self.typer.display_line(self.line)))
        print("{} ^".format(" "*(len(prompt)+self.typer.pos(self.line))))

        if self.mode == "PREDICT":
            print("Prediction:")
            i = 0
            for pred in self.predictions_found:
                print("{} {}".format([" ","*"][i==self.curr_pred], pred))
                i += 1
        everything = {
            "mode":self.mode,
            "line":self.line,
            "pos":self.typer.pos(self.line),
            "progress":self.typer.inprogress(self.line),
            "line_text":self.typer.display_line(self.line),
            "predictions":self.predictions_found,
            "current_prediction":self.curr_pred,
            "last_output":""
        }
        await websocket.send(json.dumps(everything))

if __name__ == "__main__":
    dance = DanceMat()
    dance.run()
