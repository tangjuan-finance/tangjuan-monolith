"""salary and joint table

Revision ID: 163d187d1c85
Revises: 5cdc67766842
Create Date: 2024-11-19 10:23:19.593256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '163d187d1c85'
down_revision = '5cdc67766842'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('salary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('start_year', sa.Integer(), nullable=False),
    sa.Column('end_year', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['end_year'], ['age.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['start_year'], ['age.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('salary', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_salary_owner_id'), ['owner_id'], unique=False)

    op.create_table('scenario_salary',
    sa.Column('left_id', sa.Integer(), nullable=False),
    sa.Column('right_id', sa.Integer(), nullable=False),
    sa.Column('upper_raise_rate', sa.Numeric(), nullable=False),
    sa.Column('lower_raise_rate', sa.Numeric(), nullable=False),
    sa.Column('start_year', sa.Integer(), nullable=False),
    sa.Column('end_year', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['end_year'], ['age.id'], ),
    sa.ForeignKeyConstraint(['left_id'], ['scenario.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['salary.id'], ),
    sa.ForeignKeyConstraint(['start_year'], ['age.id'], ),
    sa.PrimaryKeyConstraint('left_id', 'right_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scenario_salary')
    with op.batch_alter_table('salary', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_salary_owner_id'))

    op.drop_table('salary')
    # ### end Alembic commands ###
