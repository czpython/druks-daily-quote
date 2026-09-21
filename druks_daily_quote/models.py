from datetime import datetime

from druks.db import Base, db_session
from sqlalchemy import insert, select
from sqlalchemy.orm import Mapped, mapped_column


class Quote(Base):
    __tablename__ = "daily_quote_quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    picked_at: Mapped[datetime] = mapped_column(default=Base.utc_now)
    text: Mapped[str]
    author: Mapped[str]

    @classmethod
    async def record(cls, *, text: str, author: str) -> None:
        await db_session().execute(insert(cls).values(text=text, author=author))

    @classmethod
    async def list_newest_first(cls) -> list["Quote"]:
        return list(await db_session().scalars(select(cls).order_by(cls.picked_at.desc())))
