"""1 migrations

Revision ID: cdadc51a4c6d
Revises: 7b24b0bb7387
Create Date: 2024-06-20 19:02:59.708572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdadc51a4c6d'
down_revision: Union[str, None] = '7b24b0bb7387'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('store_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'cart', 'stories', ['store_id'], ['id'], ondelete='CASCADE')
    op.add_column('deliveries', sa.Column('store_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'deliveries', 'stories', ['store_id'], ['id'], ondelete='CASCADE')
    op.add_column('order_messages_id', sa.Column('store_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order_messages_id', 'stories', ['store_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order_messages_id', type_='foreignkey')
    op.drop_column('order_messages_id', 'store_id')
    op.drop_constraint(None, 'deliveries', type_='foreignkey')
    op.drop_column('deliveries', 'store_id')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_column('cart', 'store_id')
    # ### end Alembic commands ###
