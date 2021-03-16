import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Game(Base):
    __tablename__ = "games"

    id = sa.Column(
        UUID(),
        nullable=False,
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
    tournament_id = sa.Column(UUID(), sa.ForeignKey("tournaments.id"), nullable=False)
    team1_id = sa.Column(UUID(), sa.ForeignKey("teams.id"))
    team2_id = sa.Column(UUID(), sa.ForeignKey("teams.id"))
    round_number = sa.Column(sa.Integer, nullable=False)
    game_number = sa.Column(sa.Integer, nullable=False)
    region = sa.Column(sa.String(50), nullable=False)
    exists_in_bracket = sa.Column(sa.Boolean, default=True)

    tournament = relationship("Tournament", foreign_keys=[tournament_id])
    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])
