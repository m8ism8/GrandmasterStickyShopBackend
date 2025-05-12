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
    # The column already exists, so do nothing or use a try/except if you want to be safe
    pass

def downgrade():
    # Only drop if it exists
    pass