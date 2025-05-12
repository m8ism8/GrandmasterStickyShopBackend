"""add is_seller column

Revision ID: add_is_seller
Revises: 
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_is_seller'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add is_seller column
    op.add_column('users', sa.Column('is_seller', sa.Boolean(), nullable=False, server_default='false'))
    
    # Drop role column if it exists
    op.drop_column('users', 'role')

def downgrade():
    # Remove is_seller column
    op.drop_column('users', 'is_seller')
    
    # Add back role column
    op.add_column('users', sa.Column('role', sa.String(), nullable=True)) 