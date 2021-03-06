"""company profile.

Revision ID: dc29d554e65c
Revises: 7ad5213cc3c6
Create Date: 2022-01-08 12:38:54.237063

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "dc29d554e65c"
down_revision = "7ad5213cc3c6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_companies_id"), "companies", ["id"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_companies_id"), table_name="companies")
    op.drop_table("companies")
    # ### end Alembic commands ###
