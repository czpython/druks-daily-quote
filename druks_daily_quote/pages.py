from druks import ui

from druks_daily_quote.models import Quote


@ui.page("/")
async def overview():
    quotes = await Quote.list_newest_first()
    if not quotes:
        return ui.Page(
            "Daily quote",
            blocks=[ui.EmptyState("No quote yet", description="The next run picks one.")],
        )
    today = quotes[0]
    return ui.Page(
        "Daily quote",
        description=today.day.isoformat(),
        blocks=[
            ui.Quote(text=today.text),
            ui.Text(f"— {today.author}"),
            ui.Text(today.reason),
        ],
    )


@ui.page("/history")
async def history():
    quotes = await Quote.list_newest_first()
    return ui.Page(
        "History",
        blocks=[
            ui.Cards(
                cards=[
                    ui.Card(title=quote.text, description=f"{quote.author} · {quote.day}")
                    for quote in quotes[1:]
                ],
                empty=ui.EmptyState("Nothing before today"),
                layout="stack",
            )
        ],
    )
