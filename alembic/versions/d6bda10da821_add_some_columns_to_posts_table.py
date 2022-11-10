"""add some columns to posts table

Revision ID: d6bda10da821
Revises: 3d147a0582bf
Create Date: 2022-11-05 21:13:09.860361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d6bda10da821"
down_revision = "3d147a0582bf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    ),
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    ),


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
