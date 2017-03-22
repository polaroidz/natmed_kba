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
    entities['confidence'] = compare(entities['entity'], entity.title())
    return entities.sort_values(by='confidence', ascending=False).head(n=5)

def compare(arr, string):
    """ Compare the matching from 0 to 1 between one string
        and all other strings containing on the array provided.
        Returning a panda.Series with all respective ratios.
    """
    ratios = []
    sm = difflib.SequenceMatcher(None)
    
    for el in arr:
        sm.set_seq1(str(el))
        sm.set_seq2(string)
        
        ratios.append(sm.ratio())
    
    return pd.Series(ratios)

QUESTIONS = [
    # Simple Relation Questions
    ('What is the relation between (.*) and (.*)\?', 'SIMPLE_RELATION'),
    ('How are (.*) and (.*) related\?', 'SIMPLE_RELATION'),
    ('Is (.*) related to (.*)\?', 'SIMPLE_RELATION'),
    # What Is Questions
    ('What is (.*)\?', 'WHAT_IS')
]