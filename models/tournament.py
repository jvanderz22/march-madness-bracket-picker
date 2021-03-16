import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id = sa.Column(
        UUID(),
        nullable=False,
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
    year = sa.Column(sa.Integer, nullable=False)
    tournament_name = sa.Column(sa.String(100), nullable=False)
