from flask import Flask, request
from src.agent import agent

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