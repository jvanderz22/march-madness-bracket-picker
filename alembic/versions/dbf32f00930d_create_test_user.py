"""Create test user

Revision ID: dbf32f00930d
Revises: bc7df2ca36e9
Create Date: 2021-03-15 22:08:13.671574

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision = "dbf32f00930d"
down_revision = "bc7df2ca36e9"
branch_labels = None
depends_on = None


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = sa.Column(
        UUID(),
        nullable=False,
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
    email = sa.Column(sa.String(), nullable=False)


def upgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    user = User(email="test@test.com")
    session.add(user)
    session.commit()


def downgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    session.query(User).filter(User.email == "test@test.com").delete()
    session.commit()
