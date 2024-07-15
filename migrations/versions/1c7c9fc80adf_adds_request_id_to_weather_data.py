"""Adds request_id to weather_data

Revision ID: 1c7c9fc80adf
Revises: a5a7f1a754d5
Create Date: 2024-07-09 21:33:40.944878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1c7c9fc80adf'
down_revision: Union[str, None] = 'a5a7f1a754d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('weather_data', sa.Column('request_id', sa.VARCHAR(), autoincrement=False, nullable=True, index=True))
    op.alter_column('weather_data', 'timestamp', nullable=False)
    op.alter_column('weather_data', 'city_id', nullable=False)
    op.alter_column('weather_data', 'temperature_celsius', nullable=False)
    op.alter_column('weather_data', 'humidity', nullable=False)


def downgrade() -> None:
    op.drop_column('weather_data', 'request_id')
    op.alter_column('weather_data', 'timestamp', nullable=True)
    op.alter_column('weather_data', 'city_id', nullable=True)
    op.alter_column('weather_data', 'temperature_celsius', nullable=True)
    op.alter_column('weather_data', 'humidity', nullable=True)
