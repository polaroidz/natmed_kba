import json
from src.natmed import kgraph

class Action(object):
    def __init__(self):
        pass

    def act(self):
        raise NotImplementedError("The process has not been overwriten.")
      
    def to_json(self):
        raise NotImplementedError("The to_json has not been overwriten.")

class AnswerAction(Action):
    def __init__(self, question):
        self.question = question

    def act(self):
        if self.question['type'] == 'WHAT_IS':
            pass
        elif self.question['type'] == 'SIMPLE_RELATION':
            pass

    def to_json(self):
        return json.dumps(self.question, indent=True)
