from src.agent.action import Action
from src.parser import question

def perceive(stimuli):
    """ The sensor function of the agent, he will
        receive an stimuli and return the best
        Action to be taken in accordance to its
        utility function.
    """
    if stimuli.get('type') == 'QUESTION':
        compiled_question = question.compile(stimuli.get('data.question'))
        action = Action(compiled_question)

    return action

def utility(stimuli, action):
    """ Returns how the action would perform based
        on the given stimuli and its knowledge of
        the world.
    """
    pass