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
                self.get_medicine_info(entity['entity'])
                self.get_medicine_synonymous(entity['entity'])
                self.get_medicine_scientific_names(entity['entity'])
            
            if entity['class'] == 'Synonymous' or entity['class'] == 'ScientificName':
                medicine = self.get_medicine_from(entity)
                self.answer['medicine'] = medicine.get('name')
            
        elif self.question['type'] == 'SIMPLE_RELATION':
            entity1 = self.question['entities'][0]['scored'][0]
            entity2 = self.question['entities'][1]['scored'][0]

            self.get_relation_between(entity1, entity2)
    
    def get_relation_between(self, entity1, entity2):
        a = (entity1['class'], 'name' if entity1['class'] == 'Medicine' else 'id', entity1['entity'])
        b = (entity2['class'], 'name' if entity2['class'] == 'Medicine' else 'id', entity2['entity'])
        query = kgraph.run("""MATCH (a:%s {%s:"%s"})
                              MATCH (b:%s {%s:"%s"})
                              MATCH (a)-[]->(i)-[]->(b)
                              MATCH (i)<-[]-(r:Reference)
                              RETURN a, i, b, r""" % (a + b))
        relations = []

        for row in query:
            values = row.values()
            relation = {
                'info': dict(values[1].items()),
                'references': dict(values[3].items())
            }

            print(relation)

            relations.append(relation)

        self.answer['relations'] = relations

    def get_medicine_from(self, entity):
        query = kgraph.run("""MATCH (n:%s {id: "%s"})
                              MATCH (m:Medicine)-[:ALSO_KNOW_AS]->(n)
                              RETURN m""" % (entity['class'], entity['entity']))
        node = query.single().values()[0]
        return node

    def get_medicine_info(self, medicine):
        query = kgraph.run("MATCH (n:Medicine {name: {med}}) RETURN n", med=medicine)
        node = query.single().values()[0]

        self.answer['description'] = node.get('description')
        self.answer['family_name'] = node.get('family_name')
        self.answer['used_for'] = node.get('used_for')
        self.answer['history'] = node.get('history')

    def get_medicine_synonymous(self, medicine):
        query = kgraph.run("""MATCH (n:Medicine {name: {med}})-->(syn:Synonymous) 
                                RETURN syn.id""", med=medicine)

        self.answer['synonymous'] = [id.values()[0] for id in query]

    def get_medicine_scientific_names(self, medicine):
        query = kgraph.run("""MATCH (n:Medicine {name: {med}})-->(scy:ScientificName) 
                                RETURN scy.id""", med=medicine)

        self.answer['scientific_names'] = [id.values()[0] for id in query]

    def to_json(self):
        obj = { 'question': self.question, 'answer': self.answer }
        return json.dumps(obj)
