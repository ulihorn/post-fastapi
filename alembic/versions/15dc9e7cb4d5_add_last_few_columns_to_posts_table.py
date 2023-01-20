"""add last few columns to posts table

Revision ID: 15dc9e7cb4d5
Revises: e53d3a7b5ac8
Create Date: 2023-01-19 02:52:14.095070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15dc9e7cb4d5'
down_revision = 'e53d3a7b5ac8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
