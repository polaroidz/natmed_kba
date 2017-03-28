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

            if entity1['class'] == 'Medicine' or entity2['class'] == 'Medicine':
                if entity1['class'] == 'Disease' or entity2['class'] == 'Disease':
                    medicine = entity1['entity'] if entity1['class'] == 'Medicine' else entity2['entity']
                    disease = entity1['entity'] if entity1['class'] == 'Disease' else entity2['entity']
                    
                    self.get_relation_medicine_to_disease(medicine, disease)
                
                if entity1['class'] == 'Drug' or entity2['class'] == 'Drug':
                    medicine = entity1['entity'] if entity1['class'] == 'Medicine' else entity2['entity']
                    drug = entity1['entity'] if entity1['class'] == 'Drug' else entity2['entity']
                    
                    self.get_relation_medicine_to_drug(medicine, drug)
    
    def get_relation_medicine_to_drug(self, medicine, drug):
        pass

    def get_relation_medicine_to_disease(self, medicine, disease):
        query = kgraph.run("""MATCH (a:Medicine {name:"%s"})
                              MATCH (b:Disease {id:"%s"})
                              MATCH (a)-[r1]->(i)-[r2]->(b)
                              MATCH (i)<-[]-(ref:Reference)
                              OPTIONAL MATCH (i)-[]->(ctx:Context)
                              RETURN a, i, b, collect(ref), ctx.id, labels(i), type(r1), type(r2)""" % (medicine, disease))
        relations = []

        for row in query:
            values = row.values()
            relation = {
                'info': dict(values[1].items()),
                'info_label': values[5][0],
                'references': [dict(e.items()) for e in values[3]],
                'context': values[4],
                'relation_labels': [
                    values[6],
                    values[7]
                ]}

            relations.append(relation)

        self.answer['relation_type'] = 'MEDICINE_TO_DISEASE'
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
