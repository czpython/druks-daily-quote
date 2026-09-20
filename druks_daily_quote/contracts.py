from druks.agents import AgentOutput


class QuoteChoice(AgentOutput):
    text: str
    author: str
    reason: str

    def to_artifact(self) -> dict[str, str]:
        # The card carries the question: an in-app gate never shows its label.
        return {
            "kind": "markdown",
            "title": "Keep this quote?",
            "content": f"> {self.text}\n>\n> — {self.author}\n\n{self.reason}",
        }
