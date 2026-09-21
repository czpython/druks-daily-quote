import sqlalchemy as sa
from alembic import op

revision = "daily_quote_0002"
down_revision = "daily_quote_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("daily_quote_quotes_day_key", "daily_quote_quotes", type_="unique")
    op.alter_column(
        "daily_quote_quotes",
        "day",
        new_column_name="picked_at",
        type_=sa.DateTime(timezone=True),
        postgresql_using="day::timestamptz",
    )


def downgrade() -> None:
    op.alter_column(
        "daily_quote_quotes",
        "picked_at",
        new_column_name="day",
        type_=sa.Date(),
        postgresql_using="picked_at::date",
    )
    op.create_unique_constraint("daily_quote_quotes_day_key", "daily_quote_quotes", ["day"])
