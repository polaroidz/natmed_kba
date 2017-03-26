import atexit
from flask import Flask, request, Response
from flask_cors import CORS
from neo4j.v1 import GraphDatabase, basic_auth

kgraph_driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "naturalmed"))
kgraph = kgraph_driver.session()

app = Flask(__name__)
CORS(app)

from src.agent import agent

@app.route("/")
def index():
    return "Natmed Knowledge Based Agent API v1.0.0"

@app.route("/perceive", methods=['POST'])
def perceive():
    """ The Agent's reaction API to external enviromental stimuli.
    """
    stimuli = request.json
    action = agent.perceive(stimuli)
    return Response(action.to_json(), mimetype='application/json')

def close_connections():
    kgraph.close()

atexit.register(close_connections)