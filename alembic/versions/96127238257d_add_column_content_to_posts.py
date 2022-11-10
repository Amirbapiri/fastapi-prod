"""add column content to posts

Revision ID: 96127238257d
Revises: 88d051f292d4
Create Date: 2022-11-03 23:06:57.754633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "96127238257d"
down_revision = "88d051f292d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("posts", "content")
