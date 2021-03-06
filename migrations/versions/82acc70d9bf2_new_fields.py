"""new fields

Revision ID: 82acc70d9bf2
Revises: b5b0b9e7922e
Create Date: 2020-06-04 19:22:53.138959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82acc70d9bf2'
down_revision = 'b5b0b9e7922e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('image_url', sa.String(length=140), nullable=True))
    op.add_column('services', sa.Column('image_url', sa.String(length=140), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('services', 'image_url')
    op.drop_column('goods', 'image_url')
    # ### end Alembic commands ###
