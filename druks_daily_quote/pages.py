from druks import ui

from druks_daily_quote.models import Quote


def quote_cards(quotes: list[Quote]) -> ui.Cards:
    return ui.Cards(
        cards=[
            ui.Card(title=quote.text, description=f"{quote.author} · {quote.picked_at:%d %b %Y}")
            for quote in quotes
        ],
        empty=ui.EmptyState("No quotes yet"),
    )


@ui.page("/")
async def overview():
    quotes = await Quote.list_newest_first()
    if not quotes:
        return ui.Page(
            "No quote yet",
            blocks=[ui.EmptyState("Nothing picked", description="The next run picks one.")],
        )
    latest, *earlier = quotes
    blocks = [ui.Section(blocks=[quote_cards(earlier[:3])], title="Earlier")] if earlier else []
    return ui.Page(
        latest.text,
        description=f"{latest.author} · {latest.picked_at:%d %B %Y}",
        blocks=blocks,
    )


@ui.page("/history")
async def history():
    return ui.Page(
        "History",
        description="Every quote this app has picked.",
        blocks=[quote_cards(await Quote.list_newest_first())],
    )
