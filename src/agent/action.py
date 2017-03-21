import json

class Action(object):
    def __init__(self, question):
        self.question = question
    
    def to_json(self):
        return json.dumps(self.question)