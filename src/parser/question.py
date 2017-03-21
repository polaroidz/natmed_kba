import pandas as pd
import numpy as np
import pickle
import re
import difflib

def compile(question):
    return "Compiled Question"

ENTITY_LIST = [
    'Medicine',
    'Disease',
    'Food',
    'Context',
    'HerbSuplement',
    'LaboratoryTest',
    'Pharmacokinetics',
    'ScientificName',
    'Synonymous'
]

QUESTIONS = [
    # What Is Question
    ('What is ([A-Z].*)\?', 'WHAT_IS'),
    # Simple Relation Question
    ('What is the relation between ([A-Z].*) and ([A-Z].*)\?', 'SIMPLE_RELATION'),
    ('How are ([A-Z].*) and ([A-Z].*) related\?', 'SIMPLE_RELATION'),
    ('Is ([A-Z].*) related to ([A-Z].*)\?', 'SIMPLE_RELATION')
]