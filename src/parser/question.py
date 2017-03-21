import pandas as pd
import numpy as np
import os.path as path
import pickle
import re
import difflib

if not path.isfile('./assets/dumps/entities.pickle'):
    raise Exception("Entities pickle file not found!")

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