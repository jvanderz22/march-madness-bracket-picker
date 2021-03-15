"""Create base tables

Revision ID: bc7df2ca36e9
Revises: 
Create Date: 2021-03-15 17:06:36.573198

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision = "bc7df2ca36e9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table(
        "tournaments",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("tournament_name", sa.String(50), nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "teams",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.UniqueConstraint("name"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "games",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("team1_id", UUID(), sa.ForeignKey("teams.id", ondelete="CASCADE")),
        sa.Column("team2_id", UUID(), sa.ForeignKey("teams.id", ondelete="CASCADE")),
        sa.Column(
            "tournament_id",
            UUID(),
            sa.ForeignKey("tournaments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("region", sa.String(50), nullable=False),
        sa.Column("round_number", sa.Integer, nullable=False),
        sa.Column("game_number", sa.Integer, nullable=False),
        sa.Column("exists_in_bracket", sa.Boolean, default=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "users",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("email", sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "tournament_teams",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column(
            "team_id",
            UUID(),
            sa.ForeignKey("teams.id"),
        ),
        sa.Column(
            "tournament_id", UUID(), sa.ForeignKey("tournaments.id", ondelete="CASCADE")
        ),
        sa.Column("seed", sa.Integer, nullable=False),
        sa.Column("region", sa.String(50), nullable=False),
        sa.Column("stats", JSONB),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "tournament_averages",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column(
            "tournament_id", UUID(), sa.ForeignKey("tournaments.id", ondelete="CASCADE")
        ),
        sa.Column("stats", JSONB),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "brackets",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column(
            "tournament_id", UUID(), sa.ForeignKey("tournaments.id", ondelete="CASCADE")
        ),
        sa.Column("user_id", UUID(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "bracket_matchups",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column(
            "game_id",
            UUID(),
            sa.ForeignKey("games.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("team1_id", UUID(), sa.ForeignKey("teams.id", ondelete="CASCADE")),
        sa.Column("team2_id", UUID(), sa.ForeignKey("teams.id", ondelete="CASCADE")),
        sa.Column("winner_id", UUID(), sa.ForeignKey("teams.id", ondelete="CASCADE")),
        sa.Column(
            "bracket_id",
            UUID(),
            sa.ForeignKey("brackets.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("game_number", sa.Integer, nullable=False),
        sa.Column("round_number", sa.Integer, nullable=False),
        sa.Column("notes", sa.String(1000)),
        sa.Column("confidence", sa.Integer),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("bracket_matchups")
    op.drop_table("brackets")
    op.drop_table("users")
    op.drop_table("tournament_teams")
    op.drop_table("tournament_averages")
    op.drop_table("games")
    op.drop_table("teams")
    op.drop_table("tournaments")
