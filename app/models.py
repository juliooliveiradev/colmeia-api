from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hives: Mapped[list["Hive"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Hive(Base):
    __tablename__ = "hives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    species: Mapped[str] = mapped_column(String(80), default="Apis mellifera")
    neighborhood: Mapped[str] = mapped_column(String(120), default="")
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30), default="ativa", index=True)
    installed_at: Mapped[date] = mapped_column(Date)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner: Mapped["User"] = relationship(back_populates="hives")
    inspections: Mapped[list["Inspection"]] = relationship(
        back_populates="hive", cascade="all, delete-orphan"
    )
    harvests: Mapped[list["Harvest"]] = relationship(
        back_populates="hive", cascade="all, delete-orphan"
    )


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hive_id: Mapped[int] = mapped_column(ForeignKey("hives.id"), index=True)
    inspected_at: Mapped[date] = mapped_column(Date)
    queen_seen: Mapped[bool] = mapped_column(Boolean, default=False)
    brood_pattern: Mapped[str] = mapped_column(String(20), default="regular")
    pest_signs: Mapped[bool] = mapped_column(Boolean, default=False)
    temperament: Mapped[str] = mapped_column(String(20), default="calmo")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hive: Mapped["Hive"] = relationship(back_populates="inspections")


class Harvest(Base):
    __tablename__ = "harvests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hive_id: Mapped[int] = mapped_column(ForeignKey("hives.id"), index=True)
    harvested_at: Mapped[date] = mapped_column(Date)
    honey_kg: Mapped[float] = mapped_column(Float, default=0)
    wax_g: Mapped[float] = mapped_column(Float, default=0)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hive: Mapped["Hive"] = relationship(back_populates="harvests")
