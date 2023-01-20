"""add user table

Revision ID: 2736d383b0d7
Revises: 30edc1f4ee36
Create Date: 2023-01-19 02:10:12.561301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2736d383b0d7'
down_revision = '30edc1f4ee36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                   )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
