"""Rename examples table to notes

Revision ID: bc155b33fec1
Revises: b978e95351e3
Create Date: 2025-07-05 01:13:28.650746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc155b33fec1'
down_revision: Union[str, Sequence[str], None] = 'b978e95351e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('examples', 'notes')


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table('notes', 'examples')
