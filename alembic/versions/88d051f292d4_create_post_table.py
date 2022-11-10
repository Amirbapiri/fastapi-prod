"""create post table

Revision ID: 88d051f292d4
Revises: 
Create Date: 2022-11-03 22:51:33.331737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "88d051f292d4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
