"""Removed password

Revision ID: 8a9317952f2d
Revises: d7aa9f623d4c
Create Date: 2024-11-12 12:07:13.856392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a9317952f2d'
down_revision = 'd7aa9f623d4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=45), nullable=True))

    # ### end Alembic commands ###