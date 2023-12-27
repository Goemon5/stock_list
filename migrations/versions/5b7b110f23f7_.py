"""empty message

Revision ID: 5b7b110f23f7
Revises: 
Create Date: 2023-12-13 13:58:09.044870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b7b110f23f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('title', sa.VARCHAR(length=140), nullable=True),
    sa.Column('text', sa.TEXT(), nullable=True),
    sa.Column('summary', sa.VARCHAR(length=140), nullable=True),
    sa.Column('featured_image', sa.VARCHAR(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
