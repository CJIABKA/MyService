"""station_and_services

Revision ID: fd4104b26842
Revises: cf3b236b6eb0
Create Date: 2020-06-02 16:33:19.263517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd4104b26842'
down_revision = 'cf3b236b6eb0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coordinates', sa.String(length=100), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('station_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['station_id'], ['stations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('services_on_stations',
    sa.Column('station_id', sa.Integer(), nullable=True),
    sa.Column('services_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['services_id'], ['services.id'], ),
    sa.ForeignKeyConstraint(['station_id'], ['stations.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services_on_stations')
    op.drop_table('photos')
    op.drop_table('stations')
    op.drop_table('services')
    # ### end Alembic commands ###
