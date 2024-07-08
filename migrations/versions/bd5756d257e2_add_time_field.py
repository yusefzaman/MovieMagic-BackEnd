"""add time field

Revision ID: bd5756d257e2
Revises: c4cfa436cd9a
Create Date: 2024-07-08 13:46:30.758591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd5756d257e2'
down_revision = 'c4cfa436cd9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theatres', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theatres', schema=None) as batch_op:
        batch_op.drop_column('time')

    # ### end Alembic commands ###
