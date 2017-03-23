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
        self.answer = {}

    def act(self):
        if self.question['type'] == 'WHAT_IS':
            entity = self.question['entities'][0]['scored'][0]

            self.answer['entity'] = entity['entity']
            self.answer['class'] = entity['class']

            if entity['class'] == 'Medicine':
                query = kgraph.run("MATCH (n:Medicine {name: {med}}) RETURN n", med=entity['entity'])
                node = query.single().values()[0]

                self.answer['description'] = node.get('description')
                self.answer['family_name'] = node.get('family_name')
                self.answer['used_for'] = node.get('used_for')
                self.answer['history'] = node.get('history')

                query = kgraph.run("""MATCH (n:Medicine {name: {med}})-->(syn:Synonymous) 
                                      RETURN syn""", med=entity['entity'])

                self.answer['synonymous'] = [e['syn']['id'] for e in query]

        elif self.question['type'] == 'SIMPLE_RELATION':
            pass

    def to_json(self):
        obj = { 'question': self.question, 'answer': self.answer }
        return json.dumps(obj, indent=True)
