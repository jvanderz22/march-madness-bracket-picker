import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from .base import Base


class TournamentAverage(Base):
    __tablename__ = "tournament_averages"

    id = sa.Column(
        UUID(),
        nullable=False,
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
    tournament_id = sa.Column(UUID(), sa.ForeignKey("tournaments.id"), nullable=False)
    stats = sa.Column("stats", JSONB)

    tournament = relationship("Tournament", foreign_keys=[tournament_id])
