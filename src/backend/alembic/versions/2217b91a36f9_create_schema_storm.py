"""create schema storm

Revision ID: 2217b91a36f9
Revises: 
Create Date: 2024-08-04 00:29:41.982246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2217b91a36f9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS storm;')


def downgrade() -> None:
    op.execute('DROP SCHEMA IF EXISTS storm CASCADE;')
