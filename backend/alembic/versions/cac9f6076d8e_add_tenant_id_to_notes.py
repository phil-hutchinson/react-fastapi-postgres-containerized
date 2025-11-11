"""add_tenant_id_to_notes

Revision ID: cac9f6076d8e
Revises: 09e7c21fe39e
Create Date: 2025-11-11 02:33:46.768030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'cac9f6076d8e'
down_revision: Union[str, Sequence[str], None] = '09e7c21fe39e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Default tenant UUID
DEFAULT_TENANT_ID = '00000000-0000-0000-0000-000000000000'


def upgrade() -> None:
    """Upgrade schema."""
    # Add tenant_id column as nullable first
    op.add_column('notes', sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Set existing rows to default tenant
    op.execute(
        f"""
        UPDATE notes
        SET tenant_id = '{DEFAULT_TENANT_ID}'
        WHERE tenant_id IS NULL
        """
    )
    
    # Now make it NOT NULL
    op.alter_column('notes', 'tenant_id', nullable=False)
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_notes_tenant_id',
        'notes', 'tenants',
        ['tenant_id'], ['id']
    )
    
    # Create index on tenant_id for query performance
    op.create_index('ix_notes_tenant_id', 'notes', ['tenant_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop index
    op.drop_index('ix_notes_tenant_id', table_name='notes')
    
    # Drop foreign key
    op.drop_constraint('fk_notes_tenant_id', 'notes', type_='foreignkey')
    
    # Drop column
    op.drop_column('notes', 'tenant_id')

