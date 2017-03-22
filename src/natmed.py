import atexit
from flask import Flask, request
from src.agent import agent
from neo4j.v1 import GraphDatabase, basic_auth

kgraph_driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "naturalmed"))
kgraph = kgraph_driver.session()

app = Flask(__name__)

@app.route("/")
def index():
    return "Natmed Knowledge Based Agent API v1.0.0"

@app.route("/perceive", methods=['POST'])
def perceive():
    """ The Agent's reaction API to external enviromental stimuli.
    """
    stimuli = request.json
    action = agent.perceive(stimuli)
    return action.to_json()

def close_connections():
    kgraph.close()

atexit.register(close_connections)