import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from .base import Base


class TournamentTeam(Base):
    __tablename__ = "tournament_teams"

    id = sa.Column(
        UUID(),
        nullable=False,
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
    team_id = sa.Column(UUID(), sa.ForeignKey("teams.id"), nullable=False)
    tournament_id = sa.Column(UUID(), sa.ForeignKey("tournaments.id"), nullable=False)
    seed = sa.Column("seed", sa.Integer, nullable=False)
    region = sa.Column("region", sa.String(50), nullable=False)
    stats = sa.Column("stats", JSONB)

    tournament = relationship("Tournament", foreign_keys=[tournament_id])
    team = relationship("Team", foreign_keys=[team_id])
