import sqlalchemy as sa
from alembic import op

revision = "daily_quote_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "daily_quote_quotes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("day", sa.Date(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("day"),
    )


def downgrade() -> None:
    op.drop_table("daily_quote_quotes")
