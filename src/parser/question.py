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

QUESTIONS = [
    # What Is Questions
    ('What is ([A-Z].*)\?', 'WHAT_IS'),
    # Simple Relation Questions
    ('What is the relation between ([A-Z].*) and ([A-Z].*)\?', 'SIMPLE_RELATION'),
    ('How are ([A-Z].*) and ([A-Z].*) related\?', 'SIMPLE_RELATION'),
    ('Is ([A-Z].*) related to ([A-Z].*)\?', 'SIMPLE_RELATION')
]