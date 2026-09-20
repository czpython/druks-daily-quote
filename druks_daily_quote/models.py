from datetime import date

from druks.db import Base, db_session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Mapped, mapped_column


class Quote(Base):
    __tablename__ = "daily_quote_quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[date] = mapped_column(unique=True)
    text: Mapped[str]
    author: Mapped[str]
    reason: Mapped[str]

    @classmethod
    async def record(cls, *, day: date, text: str, author: str, reason: str) -> None:
        # One quote a day: a second run today replaces the first.
        values = {"day": day, "text": text, "author": author, "reason": reason}
        await db_session().execute(
            insert(cls)
            .values(**values)
            .on_conflict_do_update(index_elements=[cls.day], set_=values)
        )

    @classmethod
    async def list_newest_first(cls) -> list["Quote"]:
        return list(await db_session().scalars(select(cls).order_by(cls.day.desc())))
