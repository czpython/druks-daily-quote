from druks import ui

from druks_daily_quote.models import Quote


@ui.page("/")
async def overview():
    quotes = await Quote.list_newest_first()
    if not quotes:
        return ui.Page(
            "Today",
            blocks=[ui.EmptyState("Nothing picked", description="The next run picks one.")],
        )
    latest, *earlier = quotes
    blocks = [ui.Card(title=latest.text, description=f"— {latest.author}")]
    if earlier:
        cards = ui.Cards(
            cards=[
                ui.Card(
                    title=quote.text,
                    description=f"{quote.author} · {quote.picked_at:%d %b %Y}",
                )
                for quote in earlier
            ]
        )
        blocks.append(ui.Section(blocks=[cards], title="Earlier"))
    return ui.Page("Today", description=f"{latest.picked_at:%d %B %Y}", blocks=blocks)
