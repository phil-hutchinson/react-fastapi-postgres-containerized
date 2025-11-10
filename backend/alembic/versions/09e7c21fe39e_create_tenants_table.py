"""create_tenants_table

Revision ID: 09e7c21fe39e
Revises: 8caf0a8eaa64
Create Date: 2025-11-10 00:01:44.902384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid


# revision identifiers, used by Alembic.
revision: str = '09e7c21fe39e'
down_revision: Union[str, Sequence[str], None] = '8caf0a8eaa64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Default tenant UUID
DEFAULT_TENANT_ID = '00000000-0000-0000-0000-000000000000'


def upgrade() -> None:
    """Upgrade schema."""
    # Create tenants table
    op.create_table(
        'tenants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    )
    
    # Create unique index on slug
    op.create_index('ix_tenants_slug', 'tenants', ['slug'], unique=True)
    
    # Create index on id
    op.create_index('ix_tenants_id', 'tenants', ['id'], unique=False)
    
    # Seed default tenant
    op.execute(
        f"""
        INSERT INTO tenants (id, slug, name, created_at, is_active)
        VALUES ('{DEFAULT_TENANT_ID}', 'default', 'Default Tenant', now(), true)
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index('ix_tenants_id', table_name='tenants')
    op.drop_index('ix_tenants_slug', table_name='tenants')
    
    # Drop table
    op.drop_table('tenants')
