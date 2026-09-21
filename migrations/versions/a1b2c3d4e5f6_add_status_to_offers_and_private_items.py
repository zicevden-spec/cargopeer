"""add_status_to_offers_and_private_items

Revision ID: a1b2c3d4e5f6
Revises: ebe5afb6b6c8
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'ebe5afb6b6c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add status column to offers table
    op.add_column('offers', sa.Column('status', sa.String(50), nullable=False, server_default='pending'))
    
    # Add is_private and private_token columns to items table
    op.add_column('items', sa.Column('is_private', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('items', sa.Column('private_token', sa.String(255), nullable=True))


def downgrade() -> None:
    # Remove columns from items table
    op.drop_column('items', 'private_token')
    op.drop_column('items', 'is_private')
    
    # Remove status column from offers table
    op.drop_column('offers', 'status')
