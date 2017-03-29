import json
from src.natmed import kgraph
import src.kbase as kbase

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
        self.follow_up = {}

    def act(self):
        if self.question['type'] == 'WHAT_IS':
            self.what_is()
        elif self.question['type'] == 'SIMPLE_RELATION':
            self.simple_relation()

    def what_is(self):
        entity = self.question['entities'][0]['scored'][0]

        self.answer['entity'] = entity['entity']
        self.answer['class'] = entity['class']

        if entity['class'] == 'Medicine':
            self.what_is_medicine(entity['entity'])

        if self.is_synonymous(entity['class']):
            self.what_is_synonymous(entity['entity'])
    
    def simple_relation(self):
        entity1 = self.question['entities'][0]['scored'][0]
        entity2 = self.question['entities'][1]['scored'][0]

        self.answer['entity1'] = entity1
        self.answer['entity2'] = entity2

        if self.some_class(entity1, entity1, 'Medicine'):
            if self.some_class(entity1, entity2, 'Disease'):
                medicine = self.which_class(entity1, entity2, 'Medicine')
                disease = self.which_class(entity1, entity2, 'Disease')

                relations = kbase.medicine.relation_disease(medicine, disease)

                self.answer.update(relations)

    def some_class(self, e1, e2, _class):
        return e1['class'] == _class or e2['class'] == _class

    def which_class(self, e1, e2, _class):
        if e1['class'] == _class:
            return e1['entity']
        else:
            return e2['entity']

    def what_is_medicine(self, medicine):
        info = kbase.medicine.info(medicine)

        self.answer['description'] = info.get('description')
        self.answer['family_name'] = info.get('family_name')
        self.answer['used_for'] = info.get('used_for')
        self.answer['history'] = info.get('history')

        self.answer['synonymous'] = kbase.medicine.synonymous(medicine)
        self.answer['scientific_names'] = kbase.medicine.scientific_names(medicine)

    def what_is_synonymous(self, name):
        medicine = kbase.medicine.from_other_name(name)
        self.answer['medicine'] = medicine.get('name')
    
    def is_synonymous(self, _class):
        return _class == 'Synonymous' or _class == 'ScientificName'

    def to_json(self):
        obj = { 
            'question': self.question, 
            'answer': self.answer,
            'follow_up': self.follow_up }

        return json.dumps(obj)
