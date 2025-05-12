"""update products table

Revision ID: update_products
Revises: add_is_seller
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_products'
down_revision = 'add_is_seller'
branch_labels = None
depends_on = None

def upgrade():
    # Drop existing table if it exists
    op.drop_table('products')
    
    # Create new products table with updated schema
    op.create_table('products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('img', sa.String(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products') 