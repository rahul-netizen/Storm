"""First commit

Revision ID: d65856a44e5f
Revises: 62d273bbcb79
Create Date: 2023-09-10 16:41:25.513384

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d65856a44e5f"
down_revision: Union[str, None] = "62d273bbcb79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("file")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "file",
        sa.Column("file_id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "extension", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "upload_date",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("file_id", name="file_pkey"),
    )
    # ### end Alembic commands ###
