"""empty message

Revision ID: 9573403a4ab1
Revises: b0dc334ea9fd
Create Date: 2020-10-30 19:45:07.036237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9573403a4ab1'
down_revision = 'b0dc334ea9fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('club', sa.Column('join_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('club', 'join_time')
    # ### end Alembic commands ###
