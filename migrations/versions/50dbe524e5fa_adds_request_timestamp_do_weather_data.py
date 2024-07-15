"""Adds request_timestamp do weather_data

Revision ID: 50dbe524e5fa
Revises: 1c7c9fc80adf
Create Date: 2024-07-10 02:54:29.142033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '50dbe524e5fa'
down_revision: Union[str, None] = '1c7c9fc80adf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('weather_data', sa.Column('ow_request_timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.alter_column('weather_data', 'timestamp', new_column_name='user_request_timestamp')


def downgrade() -> None:
    op.drop_column('weather_data', 'ow_request_timestamp')
    op.alter_column('weather_data', 'user_request_timestamp', new_column_name='timestamp')
