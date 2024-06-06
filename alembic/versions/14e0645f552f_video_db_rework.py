"""video db rework

Revision ID: 14e0645f552f
Revises: 8f533df7c6cb
Create Date: 2024-05-30 01:22:46.251854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14e0645f552f'
down_revision: Union[str, None] = '8f533df7c6cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('caseScripts',
    sa.Column('case_scripts_id', sa.Integer(), nullable=False),
    sa.Column('scripts_id', sa.Integer(), nullable=True),
    sa.Column('content_1', sa.String(), nullable=True),
    sa.Column('content_2', sa.String(), nullable=True),
    sa.Column('content_3', sa.String(), nullable=True),
    sa.Column('content_4', sa.String(), nullable=True),
    sa.Column('content_5', sa.String(), nullable=True),
    sa.Column('content_6', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['scripts_id'], ['scripts.scripts_id'], ),
    sa.PrimaryKeyConstraint('case_scripts_id')
    )
    op.create_index(op.f('ix_caseScripts_case_scripts_id'), 'caseScripts', ['case_scripts_id'], unique=False)
    op.add_column('shortform', sa.Column('case_scripts_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'shortform', 'caseScripts', ['case_scripts_id'], ['case_scripts_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shortform', type_='foreignkey')
    op.drop_column('shortform', 'case_scripts_id')
    op.drop_index(op.f('ix_caseScripts_case_scripts_id'), table_name='caseScripts')
    op.drop_table('caseScripts')
    # ### end Alembic commands ###
