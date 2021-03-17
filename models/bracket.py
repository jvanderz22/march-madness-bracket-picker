import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Bracket(Base):
    __tablename__ = "brackets"

    id = sa.Column(
        UUID(),
        nullable=False,
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
    name = sa.Column(sa.String(50))
    tournament_id = sa.Column(UUID(), sa.ForeignKey("tournaments.id"))
    user_id = sa.Column(UUID(), sa.ForeignKey("users.id"))

    tournament = relationship("Tournament", foreign_keys=[tournament_id])
    user = relationship("User", foreign_keys=[user_id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "tournament_id": self.tournament_id,
            "user_id": self.user_id,
        }
