"""change field hashed_password in users table to not null and set default value

Revision ID: e6f7703027c7
Revises: a07b79109fbd
Create Date: 2025-01-02 18:24:32.702869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6f7703027c7'
down_revision: Union[str, None] = 'a07b79109fbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE categories ALTER COLUMN name TYPE categoryenum USING name::categoryenum"
    )

    op.execute(
        "UPDATE users SET hashed_password = '$2y$10$R2xOC21i0MRovHXvuGd18.M4OLhbZ5JC/KT3SvOJ.K1itFJJPv/TC'"
        " WHERE hashed_password = ''"
    )

    op.alter_column(
        table_name='users',
        column_name='hashed_password',
        existing_type=sa.VARCHAR(),
        nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        table_name='users',
        column_name='hashed_password',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.alter_column(
        table_name='categories',
        column_name='name',
        existing_type=sa.Enum('second', 'first', 'highest', name='categoryenum'),
        type_=sa.VARCHAR(length=7),
        existing_nullable=False
    )
