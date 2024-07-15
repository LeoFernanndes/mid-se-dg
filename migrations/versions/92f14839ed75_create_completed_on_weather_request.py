"""Create completed on weather_request

Revision ID: 92f14839ed75
Revises: 50dbe524e5fa
Create Date: 2024-07-10 03:23:46.435081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '92f14839ed75'
down_revision: Union[str, None] = '50dbe524e5fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('weather_request', sa.Column('completed', sa.Boolean(), nullable=False, index=True))


def downgrade() -> None:
    op.drop_column('weather_request', 'completed')
