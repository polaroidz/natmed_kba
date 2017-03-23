import pandas as pd
import numpy as np
import os.path as path
import pickle
import re
import difflib

ENTITIES_PATH = './assets/dumps/entities.pickle'

if not path.isfile(ENTITIES_PATH):
    raise Exception("Entities pickle file not found!")

with open(ENTITIES_PATH, "rb") as fb:
    entities = pickle.load(fb)

def compile(question):
    return match(question)

def match(string):
    """ Compiles a question and returns a list of the entities matched on it.
    """
    for question in QUESTIONS:
        matching = re.match(question[0], string) 
        if matching:
            res = { 
                'type': question[1], 
                'question': string,
                'entities': [] }

            for entity in list(matching.groups()):
                o = { 'extracted': entity, 'scored': [] }
                score_table = score(entity)
                
                for index, row in score_table.iterrows():
                    o['scored'].append({
                        'entity': row['entity'],
                        'class': row['type'],
                        'confidence': round(row['confidence'] * 100)
                    })

                res['entities'].append(o)

            return res
    return None


def score(entity):
    """ Scores the entity in relation to the entities table
    """
    entity = entity.title()
    return entities.assign(confidence=compare(entities['entity'], entity)).sort_values(by='confidence', ascending=False).head(n=5)

def compare(this, other):
    """ Compare the matching from 0 to 1 between two strings.
    """
    sm = difflib.SequenceMatcher(None)
    
    sm.set_seq1(str(this))
    sm.set_seq2(other)

    return sm.ratio()

QUESTIONS = [
    # Simple Relation Questions
    ('What is the relation between (.*) and (.*)\?', 'SIMPLE_RELATION'),
    ('How are (.*) and (.*) related\?', 'SIMPLE_RELATION'),
    ('Is (.*) related to (.*)\?', 'SIMPLE_RELATION'),
    # What Is Questions
    ('What is (.*)\?', 'WHAT_IS')
]