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
        return [
            SubjectSummary(
                id=quote.day.isoformat(),
                key=quote.day.isoformat(),
                title=f"{quote.text} — {quote.author}",
            )
            for quote in quotes
        ]
