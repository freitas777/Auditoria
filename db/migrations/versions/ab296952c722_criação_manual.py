"""criação manual

Revision ID: ab296952c722
Revises: 5b7872de0d31
Create Date: 2025-08-10 19:39:10.554862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab296952c722'
down_revision: Union[str, Sequence[str], None] = '5b7872de0d31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
