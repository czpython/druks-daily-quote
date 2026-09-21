from druks.browser import BrowserSessionSignedOutError
from druks.workflows import Workflow, step

from druks_daily_quote.app import DailyQuote
from druks_daily_quote.contracts import QuoteChoice
from druks_daily_quote.models import Quote


class PickQuote(Workflow):
    every = "0 9 * * *"

    @classmethod
    async def dispatch(cls) -> str:
        return await cls.start(subject=None)

    async def run_multistep(self) -> None:
        quotes = await self.read_quotes()
        choice = await DailyQuote.pick(quotes=quotes)
        await self.record(choice)

    @step
    async def read_quotes(self) -> list[dict[str, str]]:
        settings = await DailyQuote.settings()
        picked = {quote.text for quote in await Quote.list_newest_first()}

        async with DailyQuote.toscrape.playwright() as browser:
            page = await browser.new_page()
            await page.goto("https://quotes.toscrape.com/", wait_until="domcontentloaded")
            if not await page.locator('a[href="/logout"]').count():
                raise BrowserSessionSignedOutError("Sign in to Quotes to Scrape again.")
            quotes = page.locator(".quote")
            found = [
                {
                    "text": await quotes.nth(index).locator(".text").inner_text(),
                    "author": await quotes.nth(index).locator(".author").inner_text(),
                }
                for index in range(await quotes.count())
            ]

        # Page one holds ten quotes, so it starts repeating once they are all picked.
        fresh = [quote for quote in found if quote["text"] not in picked]
        return (fresh or found)[: settings.quote_count]

    @step
    async def record(self, choice: QuoteChoice) -> None:
        await Quote.record(text=choice.text, author=choice.author)
