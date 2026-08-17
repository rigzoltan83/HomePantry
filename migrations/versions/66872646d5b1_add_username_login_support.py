"""Add username and measurement systems

Revision ID: 66872646d5b1
Revises: 8cad6df23e0d
Create Date: 2026-08-17 08:26:38.692435

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "66872646d5b1"
down_revision = "8cad6df23e0d"
branch_labels = None
depends_on = None


def upgrade():
    # Username is added nullable first because users may
    # already exist in an installed HomePantry database.
    with op.batch_alter_table(
        "users",
        schema=None,
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "username",
                sa.String(length=80),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "measurement_system",
                sa.String(length=20),
                nullable=False,
                server_default="metric",
            )
        )

    # Give every existing user a deterministic,
    # unique temporary username.
    op.execute(
        sa.text(
            """
            UPDATE users
            SET username = 'user_' || id::text
            WHERE username IS NULL
            """
        )
    )

    with op.batch_alter_table(
        "users",
        schema=None,
    ) as batch_op:
        batch_op.alter_column(
            "username",
            existing_type=sa.String(length=80),
            nullable=False,
        )

        batch_op.create_index(
            batch_op.f("ix_users_username"),
            ["username"],
            unique=True,
        )

        batch_op.alter_column(
            "measurement_system",
            existing_type=sa.String(length=20),
            server_default=None,
        )

    with op.batch_alter_table(
        "units",
        schema=None,
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "system",
                sa.String(length=20),
                nullable=False,
                server_default="metric",
            )
        )

        batch_op.create_index(
            batch_op.f("ix_units_system"),
            ["system"],
            unique=False,
        )

        batch_op.alter_column(
            "system",
            existing_type=sa.String(length=20),
            server_default=None,
        )


def downgrade():
    with op.batch_alter_table(
        "units",
        schema=None,
    ) as batch_op:
        batch_op.drop_index(
            batch_op.f("ix_units_system")
        )

        batch_op.drop_column(
            "system"
        )

    with op.batch_alter_table(
        "users",
        schema=None,
    ) as batch_op:
        batch_op.drop_column(
            "measurement_system"
        )

        batch_op.drop_index(
            batch_op.f("ix_users_username")
        )

        batch_op.drop_column(
            "username"
        )
