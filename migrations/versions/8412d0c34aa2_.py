"""empty message

Revision ID: 8412d0c34aa2
Revises: 
Create Date: 2018-01-31 16:37:51.140067

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8412d0c34aa2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('treatment', sa.Text(), nullable=True))
    op.drop_column('job', 'requirement')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('requirement', mysql.TEXT(), nullable=True))
    op.drop_column('job', 'treatment')
    # ### end Alembic commands ###