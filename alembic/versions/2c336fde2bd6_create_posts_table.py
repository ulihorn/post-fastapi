"""create posts table

Revision ID: 2c336fde2bd6
Revises: 
Create Date: 2023-01-18 17:15:24.743531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c336fde2bd6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass



def downgrade() -> None:
    op.drop_table('posts')
    pass
