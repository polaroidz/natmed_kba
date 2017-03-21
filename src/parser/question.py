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