"""Initial Migration.

Revision ID: 7599a54a0f41
Revises: 
Create Date: 2024-10-24 07:28:55.343808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7599a54a0f41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cpf', sa.String(length=45), nullable=True),
    sa.Column('name', sa.String(length=45), nullable=True),
    sa.Column('email', sa.String(length=45), nullable=True),
    sa.Column('birthDate', sa.Date(), nullable=True),
    sa.Column('gender', sa.String(length=1), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('password', sa.String(length=45), nullable=True),
    sa.Column('type', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pathological_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('diff_diag', sa.String(length=45), nullable=True),
    sa.Column('encephalopathy', sa.String(length=45), nullable=True),
    sa.Column('ascites', sa.String(length=45), nullable=True),
    sa.Column('inr', sa.Float(), nullable=True),
    sa.Column('total_bilirubin', sa.Float(), nullable=True),
    sa.Column('albumin', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pathological_data')
    op.drop_table('user')
    # ### end Alembic commands ###