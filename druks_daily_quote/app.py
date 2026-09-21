from druks.agents import Agent
from druks.apps import App, AppSettings
from druks.browser import BrowserSession
from pydantic import Field

from druks_daily_quote.contracts import QuoteChoice


class DailyQuote(App):
    name = "daily_quote"
    icon = "quote"
    description = "A quote a day, read from a browser you signed into."
    navigation = ["overview"]

    toscrape = BrowserSession(site="quotes.toscrape.com", persist=True)

    class Settings(AppSettings):
        quote_count: int = Field(default=5, ge=1, le=10, title="Quotes to consider")

    pick = Agent(
        prompt="daily_quote/pick.md",
        contract=QuoteChoice,
        description="Choose one quote from the page.",
        include_plugins=False,
    )
