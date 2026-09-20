from datetime import date

from druks.db import Base, db_session
from druks.workflows import Subject, SubjectSummary
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column


class Quote(Base):
    __tablename__ = "daily_quote_quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[date] = mapped_column(unique=True)
    text: Mapped[str]
    author: Mapped[str]

    @classmethod
    async def keep(cls, *, day: date, text: str, author: str) -> None:
        db_session().add(cls(day=day, text=text, author=author))
        await db_session().flush()


class Day(Subject):
    """The morning a run is about. Its id is the date, so the run needs no row of
    its own, and a quote row exists only for a day whose quote you kept."""

    @classmethod
    async def list_summaries(cls, account_id: str | None) -> list[SubjectSummary]:
        quotes = await db_session().scalars(select(Quote).order_by(Quote.day.desc()))
        kept = {
            quote.day.isoformat(): f"{quote.text} — {quote.author}" for quote in quotes
        }
        # A day whose run still waits for you has kept nothing yet, so the board
        # needs the open runs beside the quotes.
        waiting = [day.id for day in await cls.list_open()]
        return [
            SubjectSummary(id=day, key=day, title=kept.get(day))
            for day in sorted({*kept, *waiting}, reverse=True)
        ]
