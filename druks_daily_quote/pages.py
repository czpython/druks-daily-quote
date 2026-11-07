from druks import ui

from druks_daily_quote.models import Quote


@ui.page("/")
async def overview():
    quotes = await Quote.all()
    if not quotes:
        return ui.Page(
            "Today",
            blocks=[ui.EmptyState("Nothing picked", description="The next run picks one.")],
        )
    latest, *earlier = quotes
    blocks = [ui.Card(title=latest.text, description=f"— {latest.author}")]
    if earlier:
        cards = ui.Cards(
            cards=[ui.Card(title=quote.text, description=quote.author) for quote in earlier]
        )
        blocks.append(ui.Section(blocks=[cards], title="Earlier"))
    return ui.Page("Today", blocks=blocks)
