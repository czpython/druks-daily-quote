from druks.agents import AgentOutput


class QuoteChoice(AgentOutput):
    text: str
    author: str
    reason: str

    def to_artifact(self) -> dict[str, str]:
        return {
            "kind": "markdown",
            "title": f"Quote by {self.author}",
            "content": f"{self.text}\n\n— {self.author}\n\n{self.reason}",
        }
