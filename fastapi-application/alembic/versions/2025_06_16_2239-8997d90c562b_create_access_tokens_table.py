"""create access_tokens table

Revision ID: 8997d90c562b
Revises: 71582bc2b68d
Create Date: 2025-06-16 22:39:53.474735

"""

from typing import Sequence, Union

from alembic import op

import fastapi_users_db_sqlalchemy.generics
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8997d90c562b"
down_revision: Union[str, None] = "71582bc2b68d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "access_tokens",
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_access_tokens_user_id_users"),
            ondelete="cascade",
        ),
        sa.PrimaryKeyConstraint("token", name=op.f("pk_access_tokens")),
    )
    op.create_index(
        op.f("ix_access_tokens_created_at"),
        "access_tokens",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_access_tokens_created_at"), 
        table_name="access_tokens"
    )
    op.drop_table("access_tokens")

