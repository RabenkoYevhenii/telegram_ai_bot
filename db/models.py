from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))


class UserResponse(Base):
    __tablename__ = "user_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    location_name: Mapped[str] = mapped_column(String(30))
    question1: Mapped[str] = mapped_column(String(5))
    question2: Mapped[str] = mapped_column(String(5))
    question3: Mapped[str] = mapped_column(String(5))
    question4: Mapped[str] = mapped_column(String(5))
    question5: Mapped[str] = mapped_column(String(5))
    comment: Mapped[str] = mapped_column(String(255))
    photo_id: Mapped[str] = mapped_column(String(255))
