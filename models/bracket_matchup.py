import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class BracketMatchup(Base):
    __tablename__ = "bracket_matchups"

    id = sa.Column(
        UUID(),
        nullable=False,
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
    game_id = sa.Column(UUID(), sa.ForeignKey("games.id"), nullable=False)
    bracket_id = sa.Column(UUID(), sa.ForeignKey("brackets.id"), nullable=False)
    team1_id = sa.Column(UUID(), sa.ForeignKey("teams.id"))
    team2_id = sa.Column(UUID(), sa.ForeignKey("teams.id"))
    winner_id = sa.Column(UUID(), sa.ForeignKey("teams.id"))
    round_number = sa.Column(sa.Integer, nullable=False)
    game_number = sa.Column(sa.Integer, nullable=False)

    notes = sa.Column(sa.String(100))
    confidence = sa.Column(sa.Integer)

    game = relationship("Game", foreign_keys=[game_id])
    bracket = relationship("Bracket", foreign_keys=[bracket_id])
    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])
    winner = relationship("Team", foreign_keys=[winner_id])

    def to_dict(self):
        return {
            "id": self.id,
            "bracket_id": self.bracket_id,
            "team1_id": self.team1_id,
            "team2_id": self.team2_id,
            "winner_id": self.winner_id,
            "round_number": self.round_number,
            "game_number": self.game_number,
            "notes": self.notes,
            "confidence": self.confidence,
        }
