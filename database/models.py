import json

from sqlalchemy import String, Integer, DateTime, Boolean, Text, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
import datetime

from database.database import Base


class Users(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_user_id: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, nullable=True)
    about_yourself: Mapped[str] = mapped_column(String, nullable=True)
    age: Mapped[str] = mapped_column(String, nullable=True)
    sex: Mapped[str] = mapped_column(String, nullable=True)
    preference: Mapped[str] = mapped_column(String, nullable=True)
    range_age: Mapped[str] = mapped_column(String, nullable=True, default='16-45')
    media: Mapped[JSONB] = mapped_column(JSONB, nullable=True, default=json.dumps({'media': []}))
    address: Mapped[str] = mapped_column(String, nullable=True)
    postal_code: Mapped[BigInteger] = mapped_column(BigInteger, nullable=True)
    country: Mapped[str] = mapped_column(String, nullable=True)
    federal_district: Mapped[str] = mapped_column(String, nullable=True)
    region_type: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    area_type: Mapped[str] = mapped_column(String, nullable=True)
    area: Mapped[str] = mapped_column(String, nullable=True)
    city_type: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)
    is_admin: Mapped[Boolean] = mapped_column(Boolean, default=False)
    done_questionnaire: Mapped[Boolean] = mapped_column(Boolean, default=False)
    date_create: Mapped[DateTime] = mapped_column(DateTime,
                                      default=datetime.datetime.now(datetime.UTC).replace(microsecond=0, tzinfo=None))
    def __str__(self):
        return (f"{self.__class__.__name__}(tg_user_id={self.tg_user_id},"
                f"username={self.username}")

    def __repr__(self):
        return str(self)


class BotReplicas(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    replica: Mapped[Text] = mapped_column(Text)
    unique_name: Mapped[str] = mapped_column(String)


class BotButtons(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    button: Mapped[Text] = mapped_column(Text)
    unique_name: Mapped[str] = mapped_column(String)


class Cities(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String)
    postal_code: Mapped[BigInteger] = mapped_column(BigInteger)
    country: Mapped[str] = mapped_column(String)
    federal_district: Mapped[str] = mapped_column(String)
    region_type: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(String)
    area_type: Mapped[str] = mapped_column(String, nullable=True)
    area: Mapped[str] = mapped_column(String, nullable=True)
    city_type: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    geo_lat: Mapped[str] = mapped_column(String)
    geo_lon: Mapped[str] = mapped_column(String)


class Matches(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id_one: Mapped[str] = mapped_column(String)
    user_reaction_one: Mapped[Boolean] = mapped_column(Boolean, default=None, nullable=True)
    user_id_two: Mapped[str] = mapped_column(String)
    user_reaction_two: Mapped[Boolean] = mapped_column(Boolean, default=None, nullable=True)
    is_send: Mapped[Boolean] = mapped_column(Boolean, default=False)
