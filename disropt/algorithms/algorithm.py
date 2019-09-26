from ..agents import Agent


class Algorithm:
    """Algorithm abstract class

    Args:
        agent (Agent): agent to execute the algorithm
        enable_log (bool): True for enabling log

    Attributes:
        agent (Agent): agent to execute the algorithm
        sequence (numpy.ndarray): sequence of data generated by the algorithm
        enable_log (bool): True for enabling log
    """

    def __init__(self, agent: Agent, enable_log: bool=False, **kwargs):
        if not isinstance(agent, Agent):
            raise ValueError("agent must be an Agent object")
        if not isinstance(enable_log, bool):
            raise ValueError("enable_log must be a bool")
        self.agent = agent
        self.enable_log = enable_log
        self.sequence = None
        super().__init__(**kwargs)

    def run(self):
        """Run the algorithm
        """
        pass

    def get_result(self):
        """Return the value of the solution
        """
        pass