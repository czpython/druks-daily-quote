from datetime import UTC, date, datetime
from typing import Literal

from druks.browser import BrowserSessionSignedOutError
from druks.workflows import Gate, Workflow, step

from druks_daily_quote.app import DailyQuote
from druks_daily_quote.contracts import QuoteChoice
from druks_daily_quote.models import Day, Quote


class KeepQuote(Gate):
    name = "keep_quote"
    action: Literal["keep", "skip"]
    # The review box always offers a note. Declare it, or the platform drops it.
    note: str = ""


class PickQuote(Workflow):
    subject = Day
    every = "0 9 * * *"

    @classmethod
    async def dispatch(cls) -> str:
        return await cls.start(subject=Day(id=datetime.now(UTC).date().isoformat()))

    async def run_multistep(self) -> None:
        quotes = await self.read_quotes()
        choice = await DailyQuote.choose(quotes=quotes)
        reply = await KeepQuote.wait(
            input_request={
                "presentation": "in_app",
                "label": "Keep this quote?",
                "controls": ["keep", "skip"],
                "questions": [],
            }
        )

        if reply.action == "keep":
            await self.keep_quote(choice)
            await self.announce("quote.kept", note=reply.note, **choice.model_dump())

    @step
    async def read_quotes(self) -> list[dict[str, str]]:
        settings = await DailyQuote.settings()

        async with DailyQuote.quotes.playwright() as browser:
            page = await browser.new_page()
            await page.goto(
                "https://quotes.toscrape.com/", wait_until="domcontentloaded"
            )
            if not await page.locator('a[href="/logout"]').count():
                raise BrowserSessionSignedOutError("Sign in to Quotes to Scrape again.")
            quotes = page.locator(".quote")
            return [
                {
                    "text": await quotes.nth(index).locator(".text").inner_text(),
                    "author": await quotes.nth(index).locator(".author").inner_text(),
                }
                for index in range(min(settings.quote_count, await quotes.count()))
            ]

    @step
    async def keep_quote(self, choice: QuoteChoice) -> None:
        day = await self.subject
        await Quote.keep(
            day=date.fromisoformat(day.id), text=choice.text, author=choice.author
        )
