"""empty message

Revision ID: 84d3b779f0c3
Revises: 06b40ebb0af8
Create Date: 2023-08-02 15:25:52.821598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84d3b779f0c3'
down_revision = '06b40ebb0af8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friendship',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('friend_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['friend_id'], ['users.id'], name=op.f('fk_friendship_friend_id_users')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_friendship_user_id_users')),
    sa.PrimaryKeyConstraint('id', 'user_id', 'friend_id', name=op.f('pk_friendship'))
    )
    op.drop_table('friends')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friends',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('friend_id', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['friend_id'], ['users.id'], name='fk_friends_friend_id_users'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_friends_user_id_users'),
    sa.PrimaryKeyConstraint('user_id', 'friend_id', name='pk_friends')
    )
    op.drop_table('friendship')
    # ### end Alembic commands ###
