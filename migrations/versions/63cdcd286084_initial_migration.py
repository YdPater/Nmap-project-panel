"""initial migration

Revision ID: 63cdcd286084
Revises: 
Create Date: 2019-02-06 19:35:00.677704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63cdcd286084'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('naam', sa.String(length=30), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('creator', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_naam'), 'projects', ['naam'], unique=False)
    op.create_table('invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scandata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('target', sa.String(length=16), nullable=True),
    sa.Column('state', sa.String(length=10), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('service', sa.String(length=30), nullable=True),
    sa.Column('product', sa.String(length=30), nullable=True),
    sa.Column('version', sa.String(length=20), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('notes', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scandata')
    op.drop_table('invites')
    op.drop_index(op.f('ix_projects_naam'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
