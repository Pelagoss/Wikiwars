"""empty message

Revision ID: 579ea334c13c
Revises: 6310cc378d3d
Create Date: 2023-05-25 14:05:25.503492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '579ea334c13c'
down_revision = '6310cc378d3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.add_column(sa.Column('started_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.drop_column('started_at')

    # ### end Alembic commands ###