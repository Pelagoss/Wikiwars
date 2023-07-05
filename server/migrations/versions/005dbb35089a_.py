"""empty message

Revision ID: 005dbb35089a
Revises: 60512480e67a
Create Date: 2023-07-05 18:31:09.071779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005dbb35089a'
down_revision = '60512480e67a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('emails', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unique_token', sa.Uuid(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('emails', schema=None) as batch_op:
        batch_op.drop_column('unique_token')

    # ### end Alembic commands ###
