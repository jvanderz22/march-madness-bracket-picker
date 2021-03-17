import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Team(Base):
    __tablename__ = "teams"

    id = sa.Column(
        UUID(),
        nullable=False,
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
    name = sa.Column(sa.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}
