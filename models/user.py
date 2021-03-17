import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(
        UUID(),
        nullable=False,
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
    email = sa.Column(sa.String(50), nullable=False)

    def to_dict(self):
        return {"id": self.id, "email": self.email}
