from datetime import datetime

from druks.db import Model
from sqlalchemy.orm import Mapped, mapped_column


class Quote(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    picked_at: Mapped[datetime] = mapped_column(default=Model.utc_now)
    text: Mapped[str]
    author: Mapped[str]
