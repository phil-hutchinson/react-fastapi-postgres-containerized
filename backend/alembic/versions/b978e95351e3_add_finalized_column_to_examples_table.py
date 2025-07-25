"""Add finalized column to examples table

Revision ID: b978e95351e3
Revises: 5b1be900971b
Create Date: 2025-06-26 05:15:39.464621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b978e95351e3'
down_revision: Union[str, Sequence[str], None] = '5b1be900971b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('examples', sa.Column('finalized', sa.Boolean(), nullable=False, server_default=sa.false()))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('examples', 'finalized')
    # ### end Alembic commands ###
