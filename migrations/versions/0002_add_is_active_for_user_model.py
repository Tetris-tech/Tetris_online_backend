"""Add is_active for User model

Revision ID: 0002
Revises: 0001
Create Date: 2025-02-25 22:07:40.700902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_table('friend')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend',
    sa.Column('sender_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.CheckConstraint('sender_id <> recipient_id', name='user_cannot_add_itself'),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], name='friend_recipient_id_fkey'),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], name='friend_sender_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='friend_pkey'),
    sa.UniqueConstraint('sender_id', 'recipient_id', name='friend_sender_id_recipient_id_key')
    )
    op.create_table('users',
    sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    # ### end Alembic commands ###
