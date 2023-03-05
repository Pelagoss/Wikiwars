"""empty message

Revision ID: 3b2229d2cae4
Revises: cb8ed79c7e95
Create Date: 2023-03-04 03:05:48.587035

"""
from alembic import op
from api.models import JSONEncodedDict
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '3b2229d2cae4'
down_revision = 'cb8ed79c7e95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.alter_column('clics',
               existing_type=sqlite.JSON(),
               type_= JSONEncodedDict(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.alter_column('clics',
               existing_type=api.models.JSONEncodedDict(),
               type_=sqlite.JSON(),
               existing_nullable=True)

    # ### end Alembic commands ###
