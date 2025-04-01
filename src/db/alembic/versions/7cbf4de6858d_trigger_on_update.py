"""trigger on_update

Revision ID: 7cbf4de6858d
Revises: 620c8f330349
Create Date: 2025-04-01 14:11:28.766861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cbf4de6858d'
down_revision: Union[str, None] = '620c8f330349'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION demo_model_update_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.col_updated_at = (now() AT TIME ZONE 'UTC'::text);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER demo_model_on_update
        BEFORE UPDATE ON demo_model
        FOR EACH ROW
        EXECUTE FUNCTION demo_model_update_timestamp();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER demo_model_on_update ON demo_model")
    op.execute("DROP FUNCTION demo_model_update_timestamp()")
