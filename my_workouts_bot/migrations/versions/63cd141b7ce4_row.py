"""'row'

Revision ID: 63cd141b7ce4
Revises: 8a563b80228f
Create Date: 2023-05-14 16:34:45.256810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63cd141b7ce4'
down_revision = '8a563b80228f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise_user_workouts', sa.Column('number', sa.Integer(), nullable=True))
    op.alter_column('exercise_user_workouts', 'values',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('exercise_user_workouts', 'relax_time',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('exercise_user_workouts', 'relax_time',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('exercise_user_workouts', 'values',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_column('exercise_user_workouts', 'number')
    # ### end Alembic commands ###