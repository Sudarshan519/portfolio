"""upgrade attendance model

Revision ID: 77b6ba4a3b4c
Revises: 9e15fce8e9cd
Create Date: 2023-07-02 21:45:29.301190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77b6ba4a3b4c'
down_revision = '9e15fce8e9cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'attendancemodel', type_='foreignkey')
    op.drop_column('attendancemodel', 'breaks')
    op.add_column('breakmodel', sa.Column('attendance', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'breakmodel', 'attendancemodel', ['attendance'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'breakmodel', type_='foreignkey')
    op.drop_column('breakmodel', 'attendance')
    op.add_column('attendancemodel', sa.Column('breaks', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'attendancemodel', 'breakmodel', ['breaks'], ['id'])
    # ### end Alembic commands ###
