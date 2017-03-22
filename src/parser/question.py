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
    return "Compiled Question"


def match(string):
    """ Compiles a question and returns a list of the entities matched on it.
    """
    for question in QUESTIONS:
        matching = re.match(question[0], string) 
        if matching:
            return { 
                'type': question[1],
                'question': string,
                'entities': list(matching.groups()) }
    return None

def compare(arr, string):
    """ Compare the matching from 0 to 1 between two strings
    """
    sm = difflib.SequenceMatcher(None)
    
    for el in arr:
        sm.set_seq1(str(el))
        sm.set_seq2(string)
        
        yield sm.ratio()

QUESTIONS = [
    # What Is Questions
    ('What is ([A-Z].*)\?', 'WHAT_IS'),
    # Simple Relation Questions
    ('What is the relation between ([A-Z].*) and ([A-Z].*)\?', 'SIMPLE_RELATION'),
    ('How are ([A-Z].*) and ([A-Z].*) related\?', 'SIMPLE_RELATION'),
    ('Is ([A-Z].*) related to ([A-Z].*)\?', 'SIMPLE_RELATION')
]