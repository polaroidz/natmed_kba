from src.agent.action import AnswerAction
from src.parser import question

def perceive(stimuli):
    """ The sensor function of the agent, he will
        receive an stimuli and return the best
        Action to be taken in accordance to its
        utility function.
    """
    if stimuli.get('type') == 'QUESTION':
        compiled_question = question.compile(stimuli['data'].get('question'))
        action = AnswerAction(compiled_question)
        action.act()

    return action

def utility(stimuli, action):
    """ Returns how the action would perform based
        on the given stimuli and its knowledge of
        the world.
    """
    pass