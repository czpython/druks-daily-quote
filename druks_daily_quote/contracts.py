from druks.agents import AgentOutput


class QuoteChoice(AgentOutput):
    text: str
    author: str
    reason: str
