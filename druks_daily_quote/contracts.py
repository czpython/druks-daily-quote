from druks.agents import AgentOutput


class QuoteChoice(AgentOutput):
    """Which quote the agent chose, as its number in the list it was given.
    The app keeps the site's own wording, so the agent never retypes a quote."""

    number: int
