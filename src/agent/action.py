import json
import random
from src.natmed import kgraph
import src.kbase as kbase
import src.parser.summary as summary

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
        self.metadata = {}
        self.answer = {}
        self.follow_up = []

    def act(self):
        if self.question['type'] == 'WHAT_IS':
            self.what_is()
        elif self.question['type'] == 'SIMPLE_RELATION':
            self.simple_relation()

    def what_is(self):
        entity = self.question['entities'][0]['scored'][0]

        self.metadata['entity'] = entity['entity']
        self.metadata['class'] = entity['class']

        if entity['class'] == 'Medicine':
            self.what_is_medicine(entity['entity'])

        if self.is_synonymous(entity['class']):
            self.what_is_synonymous(entity['entity'])
    
    def simple_relation(self):
        entity1 = self.question['entities'][0]['scored'][0]
        entity2 = self.question['entities'][1]['scored'][0]

        self.metadata['entity1'] = entity1
        self.metadata['entity2'] = entity2

        if self.some_class(entity1, entity1, 'Medicine'):
            if self.some_class(entity1, entity2, 'Disease'):
                medicine = self.which_class(entity1, entity2, 'Medicine')
                disease = self.which_class(entity1, entity2, 'Disease')

                relations = kbase.medicine.relation_disease(medicine, disease)

                if len(relations) > 0:
                    self.metadata['relation_type'] = 'MEDICINE_TO_DISEASE'
                    self.metadata['groups'] = self.group_relations(relations)

                    sl_group = random.choice(self.metadata['groups'])

                    self.answer['type'] = 'SIMPLE_RELATION'
                    self.answer['text'] = sl_group['summary']
                else:
                    self.answer['type'] = 'NO_SIMPLE_RELATION'
                    self.answer['text'] = self.no_relation(medicine, disease)
                
                self.similar_medicines_followup(medicine)
                self.medicine_diseases_followup(medicine)
                self.disease_medicines_followup(disease)

    def no_relation(self, entity1, entity2):
        return "There aren't any relations on my knowledge base between {} and {}.".format(entity1, entity2)

    def group_relations(self, relations):
        infos = []
        dosings = []

        for relation in relations:
            if relation['info_label'] == 'DosingInfo':
                dosings.append(relation)
            else:
                infos.append(relation)
        
        groups = []

        for info in infos:
            group = { 
                'summary': summary.summarize(info['info']['text']),
                'content': info, 
                'dosage': self.closest_info(info, dosings) }
            
            groups.append(group)
        
        return groups

    def closest_info(self, info, others):
        max_match = 0
        s_info = None

        for other_info in others:
            matched = 0

            for ref1 in info['references']:
                for ref2 in other_info['references']:
                    if ref1['id'] == ref2['id']:
                        matched += 1
            
            if matched > max_match:
                s_info = other_info
                max_match = matched
        
        return s_info

    def some_class(self, e1, e2, _class):
        return e1['class'] == _class or e2['class'] == _class

    def which_class(self, e1, e2, _class):
        if e1['class'] == _class:
            return e1['entity']
        else:
            return e2['entity']

    def what_is_medicine(self, medicine):
        info = kbase.medicine.info(medicine)

        self.metadata['description'] = info.get('description')
        self.metadata['family_name'] = info.get('family_name')
        self.metadata['used_for'] = info.get('used_for')
        self.metadata['history'] = info.get('history')

        self.metadata['synonymous'] = kbase.medicine.synonymous(medicine)
        self.metadata['scientific_names'] = kbase.medicine.scientific_names(medicine)

        self.answer['type'] = 'WHAT_IS_MEDICINE'
        self.answer['text'] = summary.first_sentence(info.get('description'))

        self.similar_medicines_followup(info.get('name'))
        self.medicine_diseases_followup(info.get('name'))

    def what_is_synonymous(self, name):
        medicine = kbase.medicine.from_other_name(name)
        self.metadata['medicine'] = medicine.get('name')
        
        self.answer['type'] = 'WHAT_IS_SYNONYMOUS'
        self.answer['answer'] = "{} is a synonymous of {}.".format(name, medicine.get('name'))
    
        self.similar_medicines_followup(medicine.get('name'))
        self.medicine_diseases_followup(medicine.get('name'))

    def similar_medicines_followup(self, medicine, k=5):
        similars = kbase.medicine.similar_medicines(medicine, k*2)
        
        random.shuffle(similars)

        for e in similars[:k]:
            self.follow_up.append({
                'type': 'WHAT_IS',
                'entities': [
                    { 'type': 'Medicine', 'id': e['medicine'] }
                ],
                'question': "What is {}?".format(e['medicine'])
            })
    
    def medicine_diseases_followup(self, medicine, k=5):
        diseases = kbase.medicine.medicine_diseases(medicine)

        random.shuffle(diseases)

        for disease in diseases[:k]:
            self.follow_up.append({
                'type': 'SIMPLE_RELATION',
                'entities': [
                    { 'type': 'Medicine', 'id': medicine },
                    { 'type': 'Disease', 'id': disease }
                ],
                'question': "What is the relation between {} and {}?".format(medicine, disease)
            })
    
    def disease_medicines_followup(self, disease, k=5):
        medicines = kbase.medicine.disease_medicines(disease)

        random.shuffle(medicines)

        for medicine in medicines[:k]:
            self.follow_up.append({
                'type': 'SIMPLE_RELATION',
                'entities': [
                    { 'type': 'Medicine', 'id': medicine },
                    { 'type': 'Disease', 'id': disease }
                ],
                'question': "How are {} and {} related?".format(medicine, disease)
            })

    def is_synonymous(self, _class):
        return _class == 'Synonymous' or _class == 'ScientificName'

    def to_json(self):
        obj = { 
            'answer': self.answer,
            'question': self.question, 
            'metadata': self.metadata,
            'follow_up': self.follow_up }

        return json.dumps(obj)
