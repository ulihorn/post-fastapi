"""add content column to posts table

Revision ID: 30edc1f4ee36
Revises: 2c336fde2bd6
Create Date: 2023-01-19 01:49:39.646078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30edc1f4ee36'
down_revision = '2c336fde2bd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
