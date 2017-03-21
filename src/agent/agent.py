from src.agent.action import Action
from src.parser import parser

def perceive(stimuli):
    """ The sensor function of the agent, he will
        receive an stimuli and return the best
        Action to be taken in accordance to its
        utility function.
    """
    if stimuli.get('type') == 'QUESTION':
        question = parser.compile(stimuli.get('data.question'))
        action = Action(question)

    return action

def utility(stimuli, action):
    """ Returns how the action would perform based
        on the given stimuli and its knowledge of
        the world.
    """
    pass