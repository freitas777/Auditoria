"""criação manual

Revision ID: 5b7872de0d31
Revises: 8179f46b1ed5
Create Date: 2025-07-31 21:36:32.839224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b7872de0d31'
down_revision: Union[str, Sequence[str], None] = '8179f46b1ed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
